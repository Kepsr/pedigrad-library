from Pedigrad.utils import read_until
from functools import reduce

# Characters that cannot be used to name an element of a pre-ordered set
heading_separators = [
  # 8-bit ASCII
  sep for sep in map(chr, range(256)) if sep not in '_@!'
    + '0123456789'
    + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    + 'abcdefghijklmnopqrstuvwxyz'
]

separators = heading_separators + ['!']

class Proset:
  '''
  This class models the features of a pre-ordered set.
  The pre-order relations are specified through either a file [filename] 
  or another `Proset` item passed to the constructor [__init__].

  A preorder or quasiorder is a reflexive, transitive binary relation. 
  Preorders are a general class of relation,
  with specialisations like
  equivalence relations (preorders with symmetry),
  partial orders (preorders with antisymmetry).
  '''

  def __init__(
    self, relations: list[list[str]] = [],
    transitive: bool = False, mask: bool = False, cartesian: int = 0
  ):
    self.relations = relations
    self.transitive = transitive
    self.mask = mask
    self.cartesian = cartesian

    # `relations` (which encodes the pre-order relations) is a list containing,
    # for every element of the pre-ordered set, an internal list starting with that element.
    # Each such internal list contains all the elements
    # of which its first element is a predecessor.

  def copy(self, cartesian: int):
    assert cartesian > 0
    return Proset(self.relations, self.transitive, self.mask, cartesian)

  @staticmethod
  def from_file(filename: str):
    assert filename, "filename cannot be empty"

    relations = []
    mask = False
    with open(filename, 'r') as file:

      # Seek the tokens '!obj:' or 'obj:'
      while True:
        heading = read_until(file, heading_separators, [':'])
        if not heading:
          raise Exception(f"\'obj:\' was not found im {filename}")
        if heading[-1] == "!obj":
          mask = True
          break
        if heading[-1] == "obj":
          break

      list_of_objects = []
      # Seek the token 'rel:'
      found_rel = False
      while not found_rel:
        tokens = read_until(file, separators, ['#', ':'], inclusive=True)
        if tokens == ['']:
          break
        if tokens[-2:] == ["rel", ":"]:
          objects = tokens[:-2]
          found_rel = True
        else:
          objects = tokens[:-1]
          read_until(file, separators, ['\n'])

        # Construct list_of_objects and relations
        for obj in objects:
          # assert (obj in list_of_objects) == ([obj] in relations)
          if obj not in list_of_objects:  # == [obj] not in relations
            list_of_objects.append(obj)
            relations.append([obj])

      assert found_rel  # The key word 'rel:' must have been found

      # If the key word 'rel:' was found, search the symbols '>' and ';'
      while True:

        while True:
          tokens = read_until(file, separators, ['#', '>'], inclusive=True)
          successors = []
          if tokens == ['']:
            break
          *successors, last_token = tokens
          if last_token == ">":
            break
          read_until(file, separators, ['\n'])

        # Complete [relations] with [predecessors] for each successor
        predecessors = read_until(file, separators, [';'])
        for successor in set(successors):
          try:
            i = list_of_objects.index(successor)
            for predecessor in predecessors:
              if predecessor not in relations[i]:
                relations[i].append(predecessor)
          except ValueError:  # successor is not in list_of_objects
            print(f"Warning: in \'{filename}\': {successor} is not an object")
        if not successors or not predecessors:
          break  # EOF

    return Proset(relations=relations, mask=mask)

  def close(self):
    ''' Compute the transitive closure of this set under its pre-order.
    '''
    if not self.transitive:
      self.transitive = True
      for i, elems1 in enumerate(self.relations):
        keep_going = True
        while keep_going:
          keep_going = False
          for elt1 in elems1:
            for j, elems2 in enumerate(self.relations):
              if i != j and elt1 == elems2[0]:
                for elt2 in elems2:
                  keep_going = elt2 not in elems1
                  if keep_going:
                    elems1.append(elt2)  # XXX Modifying a list while iterating over it

  def _geq(self, x: str, y: str) -> bool:
    ''' Is `x` greater than or equal to `y`?
    '''
    self.close()  # Transitivity (x >= y && y >= z => x >= z)
    return any(elems[0] == x and y in elems for elems in self.relations)  # Reflexivity (x >= x)

  def geq(self, x: list or str, y: list or str) -> bool:
    ''' Is there a pre-order relation between these two elements of the pre-ordered set?
        Cartesian version of `_geq`.
    '''
    if self.cartesian == 0:
      return self._geq(x, y)

    return all(y[i] or self._geq(x[i], y[i]) for i in range(self.cartesian))

  def max(self, x: str, y: str) -> str:
    return x if self.geq(x, y) else y

  def _inf(self, x: str, y: str) -> str:
    ''' Compute the infimum of `x` and `y`.
    '''
    self.close()
    found_elems1 = False
    found_elems2 = False
    # In a single pass,
    # find the elements of which x is the direct predecessor
    # and the elements of which y is the direct precedessor
    # assert not any(x == y and i != j for i, x in enumerate(self.relations) for j, y in enumerate(self.relations))
    for elems in self.relations:
      if elems[0] == x:
        elems1 = elems
        found_elems1 = True
      if elems[0] == y:
        elems2 = elems
        found_elems2 = True
      if found_elems1 and found_elems2:
        break
    else:
      return self.mask  # XXX Why return a bool?
    intersection = set(elems1) & set(elems2)
    if not intersection:
      return self.mask  # XXX Why return a bool?

    # XXX It seems wrong to return the max of intersection, 
    # when we are calculating an infimum.
    return reduce(self.max, intersection)

  def inf(self, x: str, y: str) -> str:
    ''' Return the infimum of these two elements of the pre-ordered set.
        Cartesian version of `_inf`.
    '''
    if self.cartesian == 0:
      return self._inf(x, y)

    return [self._inf(a, b) for i, a, b in zip(range(self.cartesian), x, y)]

  def __contains__(self, x: str) -> bool:
    ''' Does `x` belong to this pre-ordered set?
    '''
    return any(x == elems[0] for elems in self.relations)
