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
  `Proset` models pre-ordered sets.

  A pre-ordered set is a set with a reflexive, transitive binary relation
  (a preorder).
  Preorders are a general class of relation,
  with specialisations like
  equivalence relations (preorders with symmetry)
  and partial orders (preorders with antisymmetry).
  '''

  T = int

  def __init__(
    self, relations: dict[T, list[T]] = {},
    transitive: bool = False, mask: bool = False,
  ):
    self.relations = relations
    self.transitive = transitive
    self.mask = mask

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
    ''' Construct a proset from a specification written in `filename`.
    '''
    assert filename, "filename cannot be empty"

    relations = {}
    mask = False
    with open(filename, 'r') as file:

      # Seek the tokens '!obj:' or 'obj:'
      while True:
        heading = read_until(file, heading_separators, [':'])[:-1]
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
        tokens = read_until(file, separators, ['#', ':'])
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
          tokens = read_until(file, separators, ['#', '>'])
          successors = []
          if tokens == ['']:
            break
          *successors, last_token = tokens
          if last_token == ">":
            break
          read_until(file, separators, ['\n'])

        # Complete relations with predecessors for each successor
        predecessors = read_until(file, separators, [';'])[:-1]
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
        new_items = True
        while new_items:
          new_items = False
          for b in ageq:
            if b == a: continue
            cs = [c for c in self.relations[b] if c not in ageq]
            new_items |= bool(cs)
            ageq.extend(cs)  # XXX Modifying a list while iterating over it
      self.transitive = True
      assert self.istransitivelyclosed()

  def istransitivelyclosed(self):
    # Transitivity: x >= y && y >= z => x >= z
    return all(
      (self.geq(a, b) and self.geq(b, c)) <= self.geq(a, c)
      for a in self for b in self for c in self
    )

  def isreflexivelyclosed(self):
    # Reflexivity: x >= x
    return all(self.geq(a, a) for a in self)

  def geq(self, x: T, y: T) -> bool:
    ''' Is `x` greater than or equal to `y`?
    '''
    self.close()
    return x in self.relations and y in self.relations[x]

  def max(self, x: T, y: T) -> T:
    return x if self.geq(x, y) else y

  def inf(self, x: T, y: T) -> T:
    ''' The infimum of `x` and `y`.
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

  def __iter__(self):
    return iter(self.relations)

  def __contains__(self, x: T) -> bool:
    ''' Does `x` belong to this pre-ordered set?
    '''
    return x in self.relations

  def __len__(self):
    return len(self.relations)

  def __pow__(self, n: int):
    ''' The Cartesian product of this proset with itself `n` times.
    '''
    return ProductofProsets(*(self,) * n)


BoolProset = Proset({True: [True, False], False: [False]})


class ProductofProsets(Proset):
  ''' The Cartesian product of a list of prosets.
  '''

  def __init__(self, *prosets: list[Proset]):
    self.prosets = prosets

  def geq(self, xs, ys):
    return all(p.geq(x, y) for p, x, y in zip(self.prosets, xs, ys))

  def inf(self, xs, ys):
    return tuple(p.inf(x, y) for p, x, y in zip(self.prosets, xs, ys))

  @property
  def relations(self) -> dict:
    # The relations dict is hideously expensive to generate.
    # The size of the relations dict of a product of prosets
    # will be the product of the sizes of the relations dicts of the prosets.
    # In pseudocode:
    # len(product(d for d in ds)) = product(len(d) for d in ds)
    domain = tuple(product(*self.prosets))
    return {xs: [ys for ys in domain if self.geq(xs, ys)] for xs in domain}
