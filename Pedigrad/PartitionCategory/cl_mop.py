from . import _epi_factorize_partition
from Pedigrad.utils import nub


class MorphismOfPartitions:
  '''
      The canonical epimorphisms associated with the partitions of the first and second input lists are stored in the objects .source and .target, respectively.

      If we suppose that the two input lists are labeled in the same way as the procedure _epi_factorize_partition would (re)label them,
      then the list that is to be contained in the object .arrow is computed as the image of the product of the two lists,
      as illustrated in the following example.

      Consider the following lists:
      p1 = [0, 1, 2, 3, 3, 4, 5]
      p2 = [0, 1, 2, 3, 3, 3, 1]

      Then p3 := list(zip(p1, p2)) is [(0,0), (1,1), (2,2), (3,3), (3,3), (4,3), (5,1)]

      The image of the product (p4 := nub(p3)) is then
      [(0,0),(1,1),(2,2),(3,3),(4,3),(5,1)]

      We can see that for each pair (x, y) in p4,
      every component x is mapped to a unique image y
      so that p4 defines the morphism of partitions between p1 and p2.

      If p2 were [0, 1, 2, 3, 6, 3, 5]

      then the image of the product of p1 and p2 is as follows:
      p4 = [(0,0),(1,1),(2,2),(3,3),(3,6),(4,3),(5,1)]

      As can be seen, the argument 3 is 'mapped' to two different images, namely 3 and 6.
      In this case, p1 and p2 are incompatible.
  '''

  def __init__(self, source: list, target: list):
    ''' Set the attribute `arrow` to the list that describes, if it exists,
        the (unique) morphism of partitions
        from partition `source` to partition `target`.
        If no such morphism exists, an exception is raised.
    '''
    assert len(source) == len(target)
    # Relabeling the source and target with _epi_factorize_partition
    # makes it possible to quickly determine whether there is an arrow between the two.
    self.source = _epi_factorize_partition(source)
    self.target = _epi_factorize_partition(target)
    self.arrow = []
    # Compute the binary relation that is supposed to encode the function
    # from the codomain of the epimorphism encoding the source partition
    # to   the codomain of the epimorphism encoding the target partition.
    # Ensure that the computed binary relation is a function.
    for i, (x, y) in enumerate(nub(zip(self.source, self.target))):
      #Checking the following condition is equivalent to checking
      #whether the label i in self.source is mapped to a unique element in 
      #self.target, namely the value contained in self.arrow[i][1].
      #Note that: the mapping might not be unique when the indexing of 
      #the labels of the source partition is not compatible with that
      #of the target partition.
      assert x == i, "Source and target incompatible."
      # We are only interested in the image (not the graph) of the function.
      self.arrow.append(y)
