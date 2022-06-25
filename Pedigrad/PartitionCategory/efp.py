from Pedigrad.utils import nub


def _epi_factorize_partition(partition: list) -> list:
  '''
  Relabel the elements of a list with indices.

  Let `image` be `partition` with no duplicates.
  Then, this function will return a "factorization" of `partition`
  in which each element of `partition` is replaced by its index in `image`.
  The list returned will start with 0 and have a max of `len(image) - 1`.
  '''
  # The relabeling depends on the cardinal of the image of the partition.
  # The cardinal of the image is roughly the same as the image itself.
  image = nub(partition)
  return [image.index(x) for x in partition]


def __test():
  assert _epi_factorize_partition('A4CCaA') == [0, 1, 2, 2, 3, 0]


__test()
