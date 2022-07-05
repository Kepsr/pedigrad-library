from .listops import list_from_parts
from .jpop import join_trans


class Partition:

  def __init__(self, parts: list[list[int]], m: int = -1):
    '''
      `self.parts` is set to `parts`.
      The underlying set will be `range(n)` where `n` is either
      - the greatest index in `parts`
      - or `m` (if `m != -1`),
        which should be greater than or equal to
        the greatest index in `parts`

    '''
    # Get the underlying set X
    X = {x for part in parts for x in part}
    assert all(x >= 0 for x in X), "`parts` should be a list of lists of non-negative integers."
    if X:
      n = max(X)
      if m >= 0:
        # If m is given,
        # it must be greater than or equal to the size of the underlying set.
        assert m >= n, "The given range is smaller than the maximum element of the given parts."
        n = m
      parts.extend([[i] for i in range(n) if i not in X])
    self.parts = parts

  @classmethod
  def finest(cls, m: int):
    ''' Construct the finest partition of `m`.
        Each element gets its own part.
    '''
    return cls([[x] for x in range(m)])

  def close(self):
    ''' Set `self.parts` to its transitive closure.
        So that it actually partitions the set underlying `self`.
    '''
    # (x == y && y == z) >= x == z
    self.parts = join_trans(*self.parts)
    assert all(
      i1 == i2 or not set(xs1) & set(xs2)
      for i1, xs1 in enumerate(self.parts)
      for i2, xs2 in enumerate(self.parts)
    ), self.parts

  def indices(self) -> list[int]:
    ''' Return a list containing, for each element in the underlying set,
        the index of the part in which it occurs.
    '''
    self.close()
    return list_from_parts(self.parts)


def __test():
    norm = lambda xs: sorted(map(sorted, xs))

    eq1 = Partition([[0, 1, 2, 9], [7, 3, 8, 6], [4, 9, 5]])
    eq1.close()
    assert norm(eq1.parts) == [[0, 1, 2, 4, 5, 9], [3, 6, 7, 8]]
    assert eq1.indices() == [0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
    assert all(i in eq1.parts[j] for i, j in enumerate(eq1.indices()))

    eq2 = Partition([[0, 1, 2, 9], [7, 3, 8, 7], [9, 15]], 18)
    eq2.close()
    assert norm(eq2.parts) == [[0, 1, 2, 9, 15], [3, 7, 8], [4], [5], [6], [10], [11], [12], [13], [14], [16], [17]]
    assert eq2.indices() == [0, 0, 0, 1, 2, 3, 4, 1, 1, 0, 5, 6, 7, 8, 9, 0, 10, 11]
    assert all(i in eq2.parts[j] for i, j in enumerate(eq2.indices()))

    eq3 = Partition.finest(5)
    assert eq3.parts == [[0], [1], [2], [3], [4]]


__test()
