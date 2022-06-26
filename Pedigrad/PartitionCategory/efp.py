from Pedigrad.utils import nub


def _epi_factorize_partition(partition: list) -> list:
  '''
  Relabel the elements of a list with indices.

  Let `image` be `partition` with no duplicates.
  Then, this function will return a "factorization" of `partition`
  in which each element of `partition` is replaced by its index in `image`.
  The new labels will thus come from `range(len(image))`.
  '''
  # The relabeling depends on the cardinal of the image of the partition.
  # The cardinal of the image is roughly the same as the image itself.
  image = nub(partition)
  return [image.index(x) for x in partition]


# An epimorphism is a morphism f: a -> b that is right-cancellative:
# for all objects c and all morphisms g1, g2: b -> c,
# g1 . f = g2 . f => g1 = g2

# g1(f(x)) = g2(f(x)) => g1 = g2

# Epimorphisms are categorical analogues of surjective functions
# (and in the category of sets the concepts correspond exactly),
# but they may not exactly coincide in all contexts.


def __test():
  assert _epi_factorize_partition('A4CCaA') == [0, 1, 2, 2, 3, 0]
  assert _epi_factorize_partition('abc') == _epi_factorize_partition('123')  # [0, 1, 2]


__test()
