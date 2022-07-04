''' Lists to encode partitions

    The subscript operator of a list `xs` (i.e. its `__getitem__` method)
    maps indices in the domain `range(len(xs))` to elements of the list.
    This induces a partition of the domain
    according to the following equivalence relation:

    ```
    i == j iff xs[i] == xs[j]
    ```

    Taking the subscript operator to be a surjection,
    then its image (and codomain) is the list `xs`.

    An epimorphism is a right-cancellative morphism.
    i.e. f: a -> b such that for all objects c and all morphisms g1, g2: b -> c
    g1 . f = g2 . f => g1 = g2

    Epimorphisms are categorical analogues of surjective functions.
    In the category of sets, where morphisms are functions,
    epimorphisms are just surjective functions.

    [0, 1, 0, 1] <-> [[0, 1], [2, 3]]

'''
from Pedigrad.utils import nub


def partition_from_list(xs: list) -> list[list[int]]:
  '''
  Given a list `xs`, return the partition induced on `range(len(xs))`
  by the subscript operator of `xs`, as a list of equivalence classes.
  The equivalence classes under an equivalence relation
  such that there is a function `f` for which `x == y iff f(x) == f(y)`
  are exactly the fibers under `f`.
  Thus, this function will return for each distinct `x` in `xs`
  the fiber of `x` under `xs.__getitem__`.
  This function will preserve (modulo repetition) the order of elements in `xs`.

  ```
  >>> partition_from_list('abca')
  [[0, 3], [1], [2]]
  ```
  '''
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


def _quotient_impl1(jss):
  # Construct a list of the right size,
  # and reassign its contents in an arbitrary order.
  q = [None] * sum(len(js) for js in jss)
  for i, js in enumerate(jss):
    for j in js:
      q[j] = i
  return q


def _quotient_impl2(jss):
  # This implementation returns the same as quotient_impl1, but is a bit slower.
  # The dict to list conversion seems to be a performance bottleneck,
  # probably because of the sort.
  q = {j: i for i, js in enumerate(jss) for j in js}
  return [q[j] for j in sorted(q)]


def _quotient_impl3(jss):
  # Returns a dict rather than a list
  # Faster than implementation 1 for "sparse" quotients (many small equivalence classes)
  # Slower for "dense" quotients (few large equivalence classes)
  return {j: i for i, js in enumerate(jss) for j in js}


def __test():
  xs = 'aabbcca'
  assert partition_from_list(xs) == [[0, 1, 6], [2, 3], [4, 5]]
  xs = 'abca'
  fibers = {'a': [0, 3], 'b': [1], 'c': [2]}
  assert {k: v for k, v in zip(nub(xs), partition_from_list(xs))} == fibers
  xs = 'abcabbacabab'
  img = nub(xs)
  assert all(xs[j] == img[i] for i, fiber in enumerate(partition_from_list(xs)) for j in fiber)
  from .efp import _epi_factorize_partition
  # partition_from_list and _quotient_impl1 are (almost) each others' inverses
  assert _quotient_impl1(partition_from_list(xs)) == _epi_factorize_partition(xs)


__test()
