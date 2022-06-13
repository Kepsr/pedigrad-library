
# Characters that cannot be used to name an element of a pre-ordered set
heading_separators = [
  # 8-bit ASCII
  sep for sep in map(chr, range(256)) if sep not in '_@!'
    + '0123456789'
    + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    + 'abcdefghijklmnopqrstuvwxyz'
]

separators = heading_separators + ['!']

from Pedigrad.utils import read_until
from functools import reduce


class PreOrder:
  '''
  This class models the features of a pre-ordered set.
  The pre-order relations are specified through either a file [filename] 
  or another PreOrder item passed to the constructor [__init__].
  The method [closure] computes the transitive closure of the pre-order relations
  stored in the object [relations];
  the method [geq] returns a Boolean value
  specifying whether there is a pre-order relation
  between two given elements of the pre-ordered set;
  the method [inf] returns the infimum of two elements of the pre-ordered set;
  and the method __contains__ returns a Boolean value
  specifying whether an element belongs to the pre-ordered set.
  '''

  def __init__(
    self, relations: list[list[str]] = [],
    transitive: bool = False, mask: bool = False, cartesian: int = 0
  ):
    self.relations = relations
    self.transitive = transitive
    self.mask = mask
    self.cartesian = cartesian

  def copy(self, cartesian: int):
    assert cartesian > 0
    return PreOrder(self.relations, self.transitive, self.mask, cartesian)

  @staticmethod
  def from_file(filename: str):
    assert filename, "filename cannot be empty"

    relations = []
    mask = False
    with open(filename, 'r') as file:

      # Search the key words '!obj:' or 'obj:'
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
      # Search the key word 'rel:'
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

        # Construct [list_of_objects] and [relations]
        for obj in objects:
          # assert obj in list_of_objects == [obj] in relations
          if obj not in list_of_objects:
            list_of_objects.append(obj)
          if [obj] not in relations:
            relations.append([obj])

      assert found_rel  # The key word 'rel:' must have been found

      # If the key word 'rel:' was found, search the symbols '>' and ';'
      while True:

        while True:
          tokens = read_until(file, separators, ['#', '>'], inclusive=True)
          successors = []
          if tokens == ['']:
            break
          successors = tokens[:-1]
          if tokens[-1] == ">":
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

    return PreOrder(relations=relations, mask=mask)

  def closure(self):
    ''' Compute the transitive closure of the pre-order relations in the object.
    '''
    if not self.transitive:
      self.transitive = True
      for i, relation1 in enumerate(self.relations):
        keep_going = True
        while keep_going:
          keep_going = False
          for elt in relation1:
            for j, relation2 in enumerate(self.relations):
              if i != j and elt == relation2[0]:
                for new_elt in relation2:
                  if new_elt not in relation1:
                    keep_going = True
                    relation1.append(new_elt)
                  else:
                    keep_going = False

  def _geq(self, x: str, y: str) -> bool:
    ''' Is `x` greater than or equal to `y`?
    '''
    self.closure()
    return any(relation[0] == x and y in relation for relation in self.relations)

  def geq(self, x: list or str, y: list or str) -> bool:
    ''' Cartesian version of the method `_geq`
    '''
    if self.cartesian == 0:
      return self._geq(x, y)

    return all(y[i] or self._geq(x[i], y[i]) for i in range(self.cartesian))

  def max(self, x: str, y: str) -> str:
    return x if self.geq(x, y) else y

  def _inf(self, x: str, y: str) -> str:
    ''' Compute the infimum of `x` and `y`.
    '''
    self.closure()
    found_relation1 = False
    found_relation2 = False
    # In a single pass,
    # find a relation whose first element is x
    # and a relation whose first element is y
    # assert not any(x == y and i != j for i, x in enumerate(self.relations) for j, y in enumerate(self.relations))
    for relation in self.relations:
      if relation[0] == x:
        relation1 = relation
        found_relation1 = True
      if relation[0] == y:
        relation2 = relation
        found_relation2 = True
      if found_relation1 and found_relation2:
        break
    else:
      return self.mask  # XXX Why return a bool?
    intersection = set(relation1) & set(relation2)
    if not intersection:
      return self.mask  # XXX Why return a bool?

    # XXX It seems wrong to return the max of intersection, 
    # when we are calculating an infimum.
    return reduce(self.max, intersection)

  def inf(self, x: str, y: str) -> str:
    ''' Cartesian version of the method `_inf`
    '''
    if self.cartesian == 0:
      return self._inf(x, y)

    return [self._inf(a, b) for i, a, b in zip(range(self.cartesian), x, y)]

  def __contains__(self, x: str) -> bool:
    ''' Does `x` belong to this pre-ordered set?
    '''
    return any(x == relation[0] for relation in self.relations)

