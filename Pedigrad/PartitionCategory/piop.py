from Pedigrad.utils import nub


def partition_from_list(f: list) -> list[list[int]]:
  '''
  Given a list `f`, return the partition it induces on `range(len(f))`
  in the form of a list of equivalence classes.
  This function will preserve (modulo repetition) the order of elements in `f`.

  ```
  >>> partition_from_list('abca')
  [[0, 3], [1], [2]]
  ```

  Viewing a list `f` as a function mapping indices in its domain `range(len(f))`
  to elements (through its `__getitem__` method, a.k.a. the subscript operator),
  `f` induces a partition.

  The equivalence classes created by an equivalence relation `r`
  are exactly the fibers under `r`.
  '''
  image = nub(f)
  # Each element in image gets a fiber
  fibers = [[] for _ in image]
  # Relabeling f gives the desired indexing of the fibers.
  epimorphism = (image.index(x) for x in f)
  # Fill fibers
  for i, j in enumerate(epimorphism):
    # Append i to the fiber over j
    fibers[j].append(i)
  return fibers
  # NOTE This function is equivalent to:
  # [[i for i, y in enumerate(partition) if y == x] for x in nub(f)]
  # but in practice appears to be quite a bit faster,
  # probably because it doesn't have any nested loops.

  # FIXME
  # From the point of view of partitions,
  # the returned list is the preimage of the epimorphism associated with the partition,
  # where the preimage is defined as the indexed set of the fibers of the epimorphism.


def preimage(f, B, X):
  # Let f be a map X -> Y
  # The preimage of a subset B of Y under f is a subset of X:
  return {x for x in X if f(x) in B}


def fiber(f, y, X):
  # Let f be a map X -> Y
  # The fiber of an element y in a set Y under f is the preimage of {y} under f:
  return {x for x in X if f(x) == y}


def __test():
  xs = ['a', 'a', 2, 2, 3, 3, 'a']
  assert partition_from_list(xs) == [[0, 1, 6], [2, 3], [4, 5]]
  xs = 'abca'
  fibers = {'a': [0, 3], 'b': [1], 'c': [2]}
  assert {k: v for k, v in zip(nub(xs), partition_from_list(xs))} == fibers


__test()
