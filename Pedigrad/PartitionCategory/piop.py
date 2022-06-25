from Pedigrad.utils import nub


def _preimage_of_partition(partition: list) -> list[list]:
  '''
  Given a list, return a list of lists of indices that index the same element.

  e.g. _preimage_of_partition(['a','a',2,2,3,3,'a']) = [[0,1,6],[2,3],[4,5]]

  From the point of view of partitions,
  the returned list is the preimage of the epimorphism associated with the partition,
  where the preimage is defined as the indexed set of the fibers of the epimorphism.

  The previous example:
  - the list [0, 1, 6] is the fiber of the element 'a';
  - the list [2, 3] is the fiber of the element 2;
  - the list [4, 5] is the fiber of the element 3.

  The order of fibers in `preimage` will preserve (modulo duplicates)
  the order of elements in `partition`.
  '''
  image = nub(partition)
  # preimage will store the fibers of the partition.
  # For each element in the image, there will be a fiber in the preimage.
  preimage = [[] for _ in image]
  # The relabeled list of 'partition' gives the desired indexing
  # of the fibers in the preimage.
  epimorphism = (image.index(x) for x in partition)
  # Fill the fibers
  for i, j in enumerate(epimorphism):
    # Append i to the j-th fiber of the preimage
    preimage[j].append(i)
  return preimage
  # NOTE This function is equivalent to:
  # [[i for i, y in enumerate(partition) if y == x] for x in nub(partition)]
  # but in practice appears to be quite a bit faster,
  # probably because it doesn't have any nested loops.


def __test():
  xs = ['a', 'a', 2, 2, 3, 3, 'a']
  assert _preimage_of_partition(xs) == [[0, 1, 6], [2, 3], [4, 5]]


__test()
