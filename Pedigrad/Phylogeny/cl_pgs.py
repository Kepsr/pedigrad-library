from Pedigrad.PartitionCategory import Partition
from Pedigrad.AsciiTree.pet import print_evolutionary_tree
from Pedigrad.utils import is_index


class Phylogenesis:
  ''' A `Phylogenesis` is meant to be part of a `Phylogeny`.
      `taxon` is an index that allows a `Phylogenesis` to be identified in a `Phylogeny`.
      `history` records the historical record showing the relatedness of the taxon with the other taxa contained by the Phylogeny structure.
      The list of lists `history` should start with a singleton list
      and every subsequent list should contain the list that came before it.
  '''

  def __init__(self, history: list[list[int]]):
    ''' Take a list of lists whose first list is a singleton.
        `self.history` will be `history`.
        `taxon` will be the index contained in the first list `history`.
        The procedure checks whether the `history` is indeed a list of lists of indices
        and whether each list preceding another is contained in the successor list.
    '''
    #The following lines check that the lists contained in the variable
    #history is non-empty and its first list is a singleton. If this is case,
    #it allocates the value contained in the first list to the object .taxon.
    #Otherwise, the procedure returns an error message.
    assert len(history) >= 1 and len(history[0]) == 1, "Taxon is not valid"
    #The content of the first singleton list is stored in the object .taxon.
    self.taxon: int = history[0][0]
    # Check
    #- whether the values contained in the variable 'history' are all indices
    #  (i.e. non-negative integers) except for the list last (see next loop);
    #- whether each index in history[i] is contained in history[i+1].
    #If this is not the case, an error message is returned by the procedure.
    for i in range(len(history) - 1):
      for j in history[i]:
        assert j in history[i + 1] and is_index(j), "history is not valid"
    self.history: list[list[int]] = history

  def partitions(self):
    ''' Return the sequence of partitions induced by `self.history`
        over the set of indices ranging from 0 to the maximum index of the last list in `self.history`.
    '''
    # The output will be a list of lists describing the evolutionary tree 
    # associated with the label contained self.taxon.
    # The tree must be over all those individuals ranging from 0 to the
    # maximum index contained in the last 'generation' of self.history.
    max_taxon = max(self.history[-1])
    # Every partition in the output
    # contains the partitions gathering all the
    # elements of a generation and isolates all the
    # other indices that are not contained in it.
    # Returns the list of lists describing the evolutionary tree of self.taxon
    return [Partition([x], max_taxon).quotient() for x in reversed(self.history)]

  def print_tree(self):
    ''' Return the evolutionary tree described by the sequence of partitions returned by `self.partition()`.
    '''
    print_evolutionary_tree(self.partitions())
