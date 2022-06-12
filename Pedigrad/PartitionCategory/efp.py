from .iop import _image_of_partition

def _epi_factorize_partition(partition: list) -> list:
  '''
  Relabel the elements of a list with natural numbers.

  Starting at 0, allocates a new label by increasing the previously allocated label by 1.
  The first element of the list always receives the label 0
  and the highest integer used in the relabeling
  equals the length of the 'image' of the list decreased by 1 (see iop.py).

  e.g. _epi_factorize_partition(['A',4,'C','C','a','A']) = [0, 1, 2, 2, 3, 0]

  '''
  #The relabeling depends on the cardinal of the image of the partition.
  #Computing the cardinal of the image is roughly the same as computing
  #the image itself.
  image = _image_of_partition(partition)
  #A space is allocated to contain the relabeled list.
  epimorphism = []
  #If the i-th element of the list is the j-th element of the image
  #then this element is relabelled by the integer j.
  for x in partition:
    for i, y in enumerate(image):
      if x == y:
        epimorphism.append(i)
        break
  #Returns the relabeled list.
  return epimorphism
