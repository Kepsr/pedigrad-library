#------------------------------------------------------------------------------
#coproduct_of_partitions(partition1,partition2): list
#------------------------------------------------------------------------------
'''
This function takes two lists of the same legnth and returns their coproduct (or join) as partitions. Specifically, the procedure outputs the quotient of the join of their preimages. If the two input lists do not have the same length, then an error message is outputted and the program is aborted.

'''
from .piop import _preimage_of_partition
from .jpop import _join_preimages_of_partitions, FAST
from .cl_er import Partition

def coproduct_of_partitions(partition1,partition2):
  #The following line checks if the coproduct is possible.
  assert len(partition1) == len(partition2), "lengths must match"

  #Returns the coproduct of two partitions as the quotient of the
  #equivalence relation induced by the join of the preimages
  #of the two partitions.
  join = Partition(_join_preimages_of_partitions(
    _preimage_of_partition(partition1),
    _preimage_of_partition(partition2),
    FAST
  ))
  return join.quotient()
