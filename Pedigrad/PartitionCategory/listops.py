''' Lists to encode partitions

    The subscript operator of a list `xs` (i.e. its `__getitem__` method)
    maps indices in the domain `range(len(xs))` to elements of the list.
    The equivalence kernel of the subscript operator (
    ```
    i == j iff xs[i] == xs[j]
    ```
    ) partitions the domain.

    It is sensible to treat the list as not just the image of the subscript operator,
    but also its codomain, in which case the function is a surjection.

    An epimorphism is a right-cancellative morphism.
    i.e. f: a -> b such that for all objects c and all morphisms g1, g2: b -> c
    g1 . f = g2 . f => g1 = g2

    Epimorphisms are categorical analogues of surjective functions.
    In the category of sets, where morphisms are functions,
    epimorphisms are just surjective functions.

    [0, 1, 0, 1] <-> [[0, 1], [2, 3]]

'''
from Pedigrad.utils import nub


def parts_from_list(xs: list) -> list[list[int]]:
  '''
  Given a list `xs`, return the quotient set (a partition) of `range(len(xs))`
  by the equivalence kernel of `xs`'s subscript operator.
  This function will preserve (modulo repetition) the order of elements in `xs`.

  ```
  >>> parts_from_list('abca')
  [[0, 3], [1], [2]]
  ```
  '''
  # The quotient set of a set X by an equivalence relation R
  # (X modulo R or X / R)
  # is the set of all equivalence classes in X with respect to R
  # The equivalence classes with respect to the equivalence kernel of a function `f`
  # are exactly the fibers under `f`.
  # Thus, this function will return for each distinct `x` in `xs`
  # the fiber of `x` under `xs.__getitem__`.
  image = nub(xs)
  fibers = [[] for _ in image]
  canonical = (image.index(x) for x in xs)  # Factorise xs to its canonical form
  for i, j in enumerate(canonical):
    fibers[j].append(i)  # Include i in the fiber of j
  return fibers
  # NOTE This function is equivalent to:
  # [[i for i, x in enumerate(xs) if x == y] for y in nub(xs)]
  # but is quite a bit faster,
  # because it does no filtering and has no nested loops.


def preimage(f, B, X):
  # Let f be a map X -> Y
  # The preimage of a subset B of Y under f is a subset of X:
  return {x for x in X if f(x) in B}


def fiber(f, y, X):
  # Let f be a map X -> Y
  # The fiber of an element y in a set Y under f is the preimage of {y} under f:
  return {x for x in X if f(x) == y}


def equivalence_kernel(f):
  # When f is an injection, its equivalence kernel is just the identity relation.
  return lambda x, y: f(x) == f(y)


def list_from_parts(sets):
  # Construct a list of the right size,
  # and reassign its contents in an arbitrary order.
  q = [None] * sum(len(S) for S in sets)
  for i, S in enumerate(sets):
    for j in S:
      q[j] = i
  return q


def _list_from_parts_impl2(sets):
  # This implementation is a bit slower.
  # The dict to list conversion seems to be a performance bottleneck,
  # probably because of the sort.
  q = {j: i for i, S in enumerate(sets) for j in S}
  return [q[j] for j in sorted(q)]  # What if we just sort the keys? Or do range(len(q))?


def _list_from_parts_impl3(sets):
  # Returns a dict rather than a list
  # Faster than main implementation for "sparse" partitions (many small parts)
  # Slower for "dense" partitions (few large parts)
  return {j: i for i, S in enumerate(sets) for j in S}


def to_indices(xs: list) -> list:
  '''
  Relabel the elements of a list with indices.

  Let `image` be `xs` with no duplicates.
  Then, this function will return a "factorization" of `xs`
  in which each element of `xs` is replaced by its index in `image`.
  The new labels will thus come from `range(len(image))`.
  '''
  image = nub(xs)
  return [image.index(x) for x in xs]


def __test():
  xs = 'aabbcca'
  assert parts_from_list(xs) == [[0, 1, 6], [2, 3], [4, 5]]
  xs = 'abca'
  fibers = {'a': [0, 3], 'b': [1], 'c': [2]}
  assert {k: v for k, v in zip(nub(xs), parts_from_list(xs))} == fibers
  xs = 'abcabbacabab'
  img = nub(xs)
  assert all(xs[j] == img[i] for i, fiber in enumerate(parts_from_list(xs)) for j in fiber)
  # parts_from_list and list_from_parts are (almost) each other's inverse
  assert list_from_parts(parts_from_list(xs)) == to_indices(xs)

  assert to_indices('abc') == to_indices('123') == [0, 1, 2]
  assert to_indices('abccda') == [0, 1, 2, 2, 3, 0]


__test()
