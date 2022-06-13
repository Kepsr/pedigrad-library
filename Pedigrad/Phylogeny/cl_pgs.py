#------------------------------------------------------------------------------
#Phylogenesis: .taxon, .history, .partitions, .print_tree
#------------------------------------------------------------------------------
'''
This class possesses two objects, namely
- .taxon (non-negative integer)
- .history (list of lists of indices);
and three methods, namely
- .__init__ (constructor)
- .partitions
- .print_tree

A Phylogenesis item is meant to be part of another structure called a Phylogeny. The object .taxon stores an integer that allows us to identify the Phylogenesis item with respect to other Phylogenesis items in the Phylogeny structure. For its part, the object .history is meant to store the historical record showing the relatedness of the taxon with the other taxa contained by the Phylogeny structure. The list of lists contained in the object .history should:
- contain at least one singleton list and this list should be its first one;
- be such that every list should contain its predecessor list.

The constructor .__init__ takes a non-empty list of lists whose first list is a singleton and allocate
- the index contained in the first list of the input list to the object .taxon,
- the list of list to the object .history.
Before terminating, the procedure checks whether the list of lists is made of indices and whether each list preceding another is contained in the successor list.

The method .partitions() returns the sequence of partitions induced by the list of lists contained in the object .history over the set of indices ranging from 0 to the maximum index of the last list of the object .history.

The method .print_tree() returns the evolutionary tree describing the sequence of partitions returned by .partition().

'''

from Pedigrad.PartitionCategory.cl_er import EquivalenceRelation
from Pedigrad.AsciiTree.pet import print_evolutionary_tree
from Pedigrad.utils import is_index

class Phylogenesis:
  #The objects of the class are:
  #.taxon (non-negative integer)
  #.history (list of lists of indices);
  def __init__(self, history: list[list[int]]):
    #The following lines check that the lists contained in the variable
    #history is non-empty and its first list is a singleton. If this is case,
    #it allocates the value contained in the first list to the object .taxon.
    #Otherwise, the procedure returns an error message.
    assert len(history) >= 1 and len(history[0]) == 1, "Taxon is not valid"
    #The content of the first singleton list is stored in the object .taxon.
    self.taxon = history[0][0]
    #The following lines check
    #- whether the values contained in the variable 'history' are all indices
    #  (i.e. non-negative integers) except for the list last (see next loop);
    #- whether each index in history[i] is contained in history[i+1].
    #If this is not the case, an error message is returned by the procedure.
    for i in range(len(history) - 1):
      for j in history[i]:
        assert j in history[i+1] and is_index(j), "history is not valid"
    #The content of the variable 'history' can now be allocated to
    #the object .history.
    self.history = history

  def partitions(self):
    #Allocates a space in the memory to store the output of the procedure,
    #namely a list of lists describing the evolutionary tree associated with
    #the label contained self.taxon
    partitions = []
    #The tree must be over all those individuals ranging from 0 to the
    #maximum index contained in the last 'generation' of self.history.
    max_taxon = max(self.history[-1])
    for x in reversed(self.history):
      #Below, the variable u contains the partitions gathering all the
      #elements of self.history[len(self.history)-1-i] and isolates all the
      #other indices that are not contained in it.
      u = EquivalenceRelation([x], max_taxon)
      #Every partition u is stored in 'partitions'.
      partitions.append(u.quotient())
    #Returns the list of lists describing the evolutionary tree of self.taxon
    return partitions

  def print_tree(self):
    #Returns the evolutionary tree described by the list of lists outputted by
    #the procedure partitions().
    print_evolutionary_tree(self.partitions())
