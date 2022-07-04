from Pedigrad.utils import nub


def _epi_factorize_partition(xs: list) -> list:
  '''
  Relabel the elements of a list with indices.

  Let `image` be `xs` with no duplicates.
  Then, this function will return a "factorization" of `xs`
  in which each element of `xs` is replaced by its index in `image`.
  The new labels will thus come from `range(len(image))`.
  '''
  # This factorisation establishes a connection
  # between `image` and `range(len(image))`.
  image = nub(xs)
  return [image.index(x) for x in xs]


def __test():
  assert _epi_factorize_partition('abccda') == [0, 1, 2, 2, 3, 0]
  assert _epi_factorize_partition('abc') == _epi_factorize_partition('123')  # [0, 1, 2]


__test()
