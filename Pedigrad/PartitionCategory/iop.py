
def _image_of_partition(partition: list) -> list:
  '''
  This function takes a list of elements and returns the list of its elements that occur at least once (without repetition) in the order in which they can be accessed from the left to the right.

  e.g. _image_of_partition([3,3,2,1,1,2,4,5,6,5,2,6]) = [3,2,1,4,5,6]

  '''
  image = []
  for x in partition:
    if x not in image:
      image.append(x)
  return image
