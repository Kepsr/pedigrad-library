from Pedigrad.PartitionCategory.jpop import join_trans


class Partition:

  def __init__(self, equivalence_classes: list[list[int]], m: int = -1):
    '''

      `self.equivalence_classes` is set to `equivalence_classes`.
      The underlying set will be `range(n)` where `n` is either
      - the greatest index in `equivalence_relations`
      - or `m` (if `m != -1`),
        which should be greater than or equal to
        the greatest index in `equivalence_relations`

    '''
    # elements is the set underlying equivalence_classes,
    # and is got by flattening it.
    elements = {x for class_ in equivalence_classes for x in class_}
    assert all(x >= 0 for x in elements), "`equivalence_classes` should be a list of lists of non-negative integers."
    if elements:
      n = max(elements)
      if m >= 0:
        # If m is given,
        # it must be greater than or equal to the size of the underlying set.
        assert m >= n, "The given range is smaller than the maximum element of the given equivalence_classes."
        n = m
      equivalence_classes.extend([[i] for i in range(n) if i not in elements])
    self.equivalence_classes = equivalence_classes

  @classmethod
  def from_int(cls, m: int):
    ''' Create a simple partition using a canonical surjection,
        in which every index from 0 to `m` gets its own equivalence class.
    '''
    return cls([[x] for x in range(m)])

  def close(self):
    ''' Set `self.equivalence_classes` to its transitive closure.
        So that it actually partitions the set underlying `self`.
    '''
    # (x == y && y == z) >= x == z
    self.equivalence_classes = join_trans(*self.equivalence_classes)
    assert all(
      i1 == i2 or not set(xs1) & set(xs2)
      for i1, xs1 in enumerate(self.equivalence_classes)
      for i2, xs2 in enumerate(self.equivalence_classes)
    ), self.equivalence_classes

  def quotient(self) -> list[int]:
    ''' Return a list of integers
        whose non-trivial fibers are those contained in `self.equivalence_classes`.
    '''
    from .listops import _quotient_impl1
    # Ensure that `self.equivalence_classes` actually partitions the underlying set.
    self.close()
    # Return the partition associated with the equivalence relation
    # defined by self.equivalence_classes.
    return _quotient_impl1(self.equivalence_classes)


def __test():
    from .efp import _epi_factorize_partition
    norm = lambda xs: sorted(map(sorted, xs))

    eq1 = Partition([[0, 1, 2, 9], [7, 3, 8, 6], [4, 9, 5]])
    eq1.close()
    assert norm(eq1.equivalence_classes) == [[0, 1, 2, 4, 5, 9], [3, 6, 7, 8]]
    assert _epi_factorize_partition(eq1.quotient()) == [0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
    assert all(i in eq1.equivalence_classes[j] for i, j in enumerate(eq1.quotient()))

    eq2 = Partition([[0, 1, 2, 9], [7, 3, 8, 7], [9, 15]], 18)
    eq2.close()
    assert norm(eq2.equivalence_classes) == [[0, 1, 2, 9, 15], [3, 7, 8], [4], [5], [6], [10], [11], [12], [13], [14], [16], [17]]
    assert _epi_factorize_partition(eq2.quotient()) == [0, 0, 0, 1, 2, 3, 4, 1, 1, 0, 5, 6, 7, 8, 9, 0, 10, 11]
    assert all(i in eq2.equivalence_classes[j] for i, j in enumerate(eq2.quotient()))

    eq3 = Partition.from_int(5)
    assert eq3.equivalence_classes == [[0], [1], [2], [3], [4]]


__test()
