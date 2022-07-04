from Pedigrad.PartitionCategory.jpop import join_trans


class Partition:

  def __init__(self, sets: list[list[int]], m: int = -1):
    '''

      The set of all equivalence classes in a set X
      with respect to an equivalence relation R
      is called the quotient set of X by R, or X modulo R (X / R).

      `self.quotient_set` is set to `sets`.
      The underlying set will be `range(n)` where `n` is either
      - the greatest index in `equivalence_relations`
      - or `m` (if `m != -1`),
        which should be greater than or equal to
        the greatest index in `equivalence_relations`

    '''
    # Get the underlying set X
    X = {x for S in sets for x in S}
    assert all(x >= 0 for x in X), "`sets` should be a list of lists of non-negative integers."
    if X:
      n = max(X)
      if m >= 0:
        # If m is given,
        # it must be greater than or equal to the size of the underlying set.
        assert m >= n, "The given range is smaller than the maximum element of the given sets."
        n = m
      sets.extend([[i] for i in range(n) if i not in X])
    self.quotient_set = sets

  @classmethod
  def finest(cls, m: int):
    ''' Construct the finest partition of `m`.
        Each element gets its own equivalence class.
    '''
    return cls([[x] for x in range(m)])

  def close(self):
    ''' Set `self.quotient_set` to its transitive closure.
        So that it actually partitions the set underlying `self`.
    '''
    # (x == y && y == z) >= x == z
    self.quotient_set = join_trans(*self.quotient_set)
    assert all(
      i1 == i2 or not set(xs1) & set(xs2)
      for i1, xs1 in enumerate(self.quotient_set)
      for i2, xs2 in enumerate(self.quotient_set)
    ), self.quotient_set

  def indices(self) -> list[int]:
    ''' Return a list of indices mapping elements in the underlying set
        to equivalence classes in `self.quotient_set`.
    '''
    from .listops import list_from_quotient
    self.close()
    return list_from_quotient(self.quotient_set)


def __test():
    from .efp import _epi_factorize_partition
    norm = lambda xs: sorted(map(sorted, xs))

    eq1 = Partition([[0, 1, 2, 9], [7, 3, 8, 6], [4, 9, 5]])
    eq1.close()
    assert norm(eq1.quotient_set) == [[0, 1, 2, 4, 5, 9], [3, 6, 7, 8]]
    assert _epi_factorize_partition(eq1.indices()) == [0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
    assert all(i in eq1.quotient_set[j] for i, j in enumerate(eq1.indices()))

    eq2 = Partition([[0, 1, 2, 9], [7, 3, 8, 7], [9, 15]], 18)
    eq2.close()
    assert norm(eq2.quotient_set) == [[0, 1, 2, 9, 15], [3, 7, 8], [4], [5], [6], [10], [11], [12], [13], [14], [16], [17]]
    assert _epi_factorize_partition(eq2.indices()) == [0, 0, 0, 1, 2, 3, 4, 1, 1, 0, 5, 6, 7, 8, 9, 0, 10, 11]
    assert all(i in eq2.quotient_set[j] for i, j in enumerate(eq2.indices()))

    eq3 = Partition.finest(5)
    assert eq3.quotient_set == [[0], [1], [2], [3], [4]]


__test()
