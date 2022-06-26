from . import Partition, partition_from_list, join_partitions, FAST


def coproduct_of_partitions(partition1: list, partition2: list):
  ''' Given two lists of equal length,
      return their coproduct (or join) as partitions,
      specifically the quotient of the join of their preimages.
  '''
  assert len(partition1) == len(partition2), "lengths must match"

  # Return the coproduct of two partitions as the quotient of the
  # equivalence relation induced by the join of two partitions' preimages.
  join = Partition(join_partitions(
    partition_from_list(partition1),
    partition_from_list(partition2),
    FAST
  ))
  return join.quotient()
