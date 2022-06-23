from Pedigrad.utils import read_until
from functools import reduce
from itertools import product

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
  equivalence relations (preorders with symmetry)
  and partial orders (preorders with antisymmetry).
  '''

  T = int

  def __init__(
    self, relations: dict[T, list[T]] = {},
    transitive: bool = False, mask: bool = False, cartesian: int = 1
  ):
    self.relations = relations
    self.transitive = transitive
    self.mask = mask
    self.cartesian = cartesian

    # Ensure all necessary keys are present
    for x in sum(relations.values(), []):
      if x not in relations:
        self.relations[x] = [x]

    # `relations` (which encodes the pre-order relations) is a dict
    # that pairs every element of the pre-ordered set
    # with a list containing all the elements of which it is a predecessor
    # (including itself, by reflexivity).

  @staticmethod
  def from_file(filename: str):
    assert filename, "filename cannot be empty"

    relations = {}
    mask = False
    with open(filename, 'r') as file:

      # Seek the tokens '!obj:' or 'obj:'
      while True:
        heading = read_until(file, heading_separators, [':'])
        if not heading:
          raise Exception(f"\'obj:\' was not found in {filename}")
        if heading[-1] == "!obj":
          mask = True
          break
        if heading[-1] == "obj":
          break

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

        # Construct relations
        for obj in objects:
          if obj not in relations:
            relations[obj] = [obj]

      assert found_rel  # The token 'rel:' must have been found

      # With the token 'rel:' found, seek the tokens '>' and ';'
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

        # Complete relations with predecessors for each successor
        predecessors = read_until(file, separators, [';'])
        for successor in set(successors):
          try:
            for predecessor in predecessors:
              if predecessor not in relations[successor]:
                relations[successor].append(predecessor)
          except KeyError:  # successor is not in relations
            print(f"Warning: in \'{filename}\': {successor} is not an object")
        if not successors or not predecessors:
          break  # EOF

    return Proset(relations=relations, mask=mask)

  def close(self):
    ''' Compute the transitive closure of this set under its pre-order.
    '''
    if not self.transitive:
      for a, ageq in self.relations.items():
        keep_going = True
        while keep_going:
          keep_going = False
          for b in ageq:
            if b == a: continue
            cs = [c for c in self.relations[b] if c not in ageq]
            keep_going = bool(cs)
            ageq.extend(cs)  # XXX Modifying a list while iterating over it
      self.transitive = True

  def istransitivelyclosed(self):
    # Transitivity: x >= y && y >= z => x >= z
    return all(
      (self.geq(a, b) and self.geq(b, c)) <= self.geq(a, c)
      for a in self for b in self for c in self
    )

  def isreflexivelyclosed(self):
    # Reflexivity: x >= x
    return all(self.geq(a, a) for a in self)

  def _geq(self, x: T, y: T) -> bool:
    ''' Is `x` greater than or equal to `y`?
    '''
    self.close()
    if isinstance(x, list):
      x = tuple(x)
    return x in self.relations and y in self.relations[x]

  def geq(self, x: T, y: T) -> bool:
    ''' Is there a pre-order relation between these two elements of the pre-ordered set?
        Cartesian version of `_geq`.
    '''
    if self.cartesian == 1:
      return self._geq(x, y)

    return all(y[i] or self._geq(x[i], y[i]) for i in range(self.cartesian))

  def max(self, x: T, y: T) -> T:
    return x if self.geq(x, y) else y

  def _inf(self, x: T, y: T) -> T:
    ''' Compute the infimum of `x` and `y`.
    '''
    self.close()
    # Find the elements of which x is the direct predecessor
    #  and the elements of which y is the direct precedessor
    elems1 = self.relations.get(x, None)
    elems2 = self.relations.get(y, None)
    if elems1 is None or elems2 is None:
      return self.mask  # XXX Why return a bool?
    intersection = set(elems1) & set(elems2)
    if not intersection:
      return self.mask  # XXX Why return a bool?

    # XXX It seems wrong to return the max of intersection,
    # when we are calculating an infimum.
    return reduce(self.max, intersection)

  def inf(self, x: T, y: T) -> T:
    ''' Return the infimum of these two elements of the pre-ordered set.
        Cartesian version of `_inf`.
    '''
    if self.cartesian == 1:
      return self._inf(x, y)

    return [self._inf(a, b) for i, a, b in zip(range(self.cartesian), x, y)]

  def __iter__(self):
    return iter(self.relations)

  def __contains__(self, x: T) -> bool:
    ''' Does `x` belong to this pre-ordered set?
    '''
    return x in self.relations

  def __len__(self):
    return len(self.relations)

  def __pow__(self, n: int):
    ''' The Cartesian product of this proset with itself n times.
    '''
    assert n > 0
    return ProductofProsets(*(self,) * n)


BoolProset = Proset({True: [True, False], False: [False]})


class ProductofProsets(Proset):

  def __init__(self, *prosets):
    self.prosets = prosets

  def geq(self, xs, ys):
    return all(p.geq(x, y) for p, x, y in zip(self.prosets, xs, ys))

  def inf(self, xs, ys):
    return tuple(p.inf(x, y) for p, x, y in zip(self.prosets, xs, ys))


# The relations dict is hideously expensive to generate.
# A proset of size m, when raised to the nth power, will give rise to one of size m ** n.
def product_of_proset(proset: Proset, n: int) -> Proset:
  elems = tuple(product(*(proset.relations,) * n))
  relations = {
    xs: [ys for ys in elems if all(proset.geq(x, y) for x, y in zip(xs, ys))]
    for xs in elems
  }
  return Proset(relations)
