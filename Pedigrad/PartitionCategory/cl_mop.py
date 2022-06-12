#------------------------------------------------------------------------------
#MorphismOfPartitions: .arrow, .source, .target
#------------------------------------------------------------------------------
'''
This class possesses three objects, namely
- .arrow (list)
- .source (list)
- .target (list)
and a constructor .__init__. The consructor .__init__ takes two lists as well as an optional argument and stores, in the object .arrow, the list that describes, if it exists, the (unique) morphism of partitions from the first input list (seen as a partition) to the second input list (seen as a partition). If the morphism does not exist, then the method returns an error message unless the value False was given as an input in the third argument.

The canonical epimorphisms associated with the partitions of the first and second input lists are stored in the objects .source and .target, respectively.

If we suppose that the two input lists are labeled in the same way as the procedure _epi_factorize_partition would (re)label them, then the list that is to be contained in the object .arrow is computed as the image of the product of the two lists, as illustrated in the following example.

Consider the following lists.
p1 = [0, 1, 2, 3, 3, 4, 5]
p2 = [0, 1, 2, 3, 3, 3, 1]

Their zip is as follows:
p3 = zip(p1,p2) = [(0,0),(1,1),(2,2),(3,3),(3,3),(4,3),(5,1)]

The image of the product is then as follows:
p4 = _image_of_partition(p3) = [(0,0),(1,1),(2,2),(3,3),(4,3),(5,1)]

We can see that for each pair (x,y) in p4, every component x is mapped to a unique image y so that p4 defines the morphism of partitions between p1 and p2.

If there exists no morphism from the first input list to the second input list, then the function outputs an error message.

For example, if we modify p2 as follows
p2 = [0, 1, 2, 3, 6, 3, 5]

then the image of the product of p1 and p2 is as follows:
p4 = [(0,0),(1,1),(2,2),(3,3),(3,6),(4,3),(5,1)]

As can be seen, the argument 3 is 'mapped' to two different images, namely 3 and 6. In this case, the constructor .__init__ exits the program with an error message. 

'''
from Pedigrad.PartitionCategory.efp import _epi_factorize_partition
from Pedigrad.PartitionCategory.iop import _image_of_partition

class MorphismOfPartitions:
  #The objects of the class are:
  #.arrow (list);
  #.source (list);
  #.target (list).
  def __init__(self, source: list, target: list, *args):
    if len(source) == len(target):
      #Relabeling the source and target by using _epi_factorize_partition
      #will allow us to quickly know whether there is an arrow from the source
      #and the target (see below).
      self.source = _epi_factorize_partition(source)
      self.target = _epi_factorize_partition(target)
      #The following line computes the binary relation that is supposed to 
      #encode the function from the codomain of the underlying
      #epimorphism encoding the source partition to the codomain of the
      #epimorphsim encoding the target partition.
      self.arrow = _image_of_partition(zip(self.source,self.target))
    #The following loop checks if the binary relation contained 
    #in self.arrow is a function.
    for i, x in enumerate(self.arrow):
      #Checking the following condition is equivalent to checking
      #whether the label i in self.source is mapped to a unique element in 
      #self.target, namely the value contained in self.arrow[i][1].
      #Note that: the mapping might not be unique when the indexing of 
      #the labels of the source partition is not compatible with that
      #of the target partition.
      if x[0] == i:
        # We are only interested in the image (not the graph) of the function.
        x = x[1]
      else:
        if len(args) > 0 and not args[0]:
          exit()
        else:
          print("Error: in MorphismOfPartitions.__init__: source and target are not compatible.")
          exit()
