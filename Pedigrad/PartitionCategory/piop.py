from .efp import _epi_factorize_partition
from .iop import _image_of_partition

def _preimage_of_partition(partition: list) -> list[list]:
  '''
  This function takes a list and returns the list of the lists of indices that index the same element.

  e.g. _preimage_of_partition(['a','a',2,2,3,3,'a']) = [[0,1,6],[2,3],[4,5]]

  From the point of view of partitions, the returned list is the preimage of the epimorphism associated with the partition, where the preimage is defined as the indexed set of the fibers of the epimorphism.

  The previous example:
  - the list [0,1,6] is the fiber of the element 'a';
  - the list [2,3] is the fiber of the element 2;
  - the list [4,5] is the fiber of the element 3.

  The preimage will always orders its fibers with respect to the order in which the elements of the input list appear.

  '''
  # Fill preimage with empty lists in order to store the fibers of the partition.
  preimage = [[] for _ in _image_of_partition(partition)]
  # The number of fibers contained by the preimage is equal to the number
  # of elements in the image of the partition.
  # The relabeled list of 'partition' gives the desired indexing
  # of the fibers contained in the preimage of partition.
  epimorphism = _epi_factorize_partition(partition)
  for i, j in enumerate(epimorphism):
    # Append i to the j-th fiber of the preimage.
    preimage[j].append(i)
  # After the loop, all the fibers are filled and the preimage is returned
  return preimage
