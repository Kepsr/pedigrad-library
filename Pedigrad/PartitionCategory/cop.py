from . import Partition, _preimage_of_partition, _join_preimages_of_partitions, FAST


def coproduct_of_partitions(partition1: list, partition2: list):
  ''' Given two lists of equal length,
      return their coproduct (or join) as partitions,
      specifically the quotient of the join of their preimages.
  '''
  assert len(partition1) == len(partition2), "lengths must match"

  # Return the coproduct of two partitions as the quotient of the
  # equivalence relation induced by the join of two partitions' preimages.
  join = Partition(_join_preimages_of_partitions(
    _preimage_of_partition(partition1),
    _preimage_of_partition(partition2),
    FAST
  ))
  return join.quotient()
