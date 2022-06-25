from . import _join_preimages_of_partitions, FAST

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

  @staticmethod
  def from_int(m: int):
    ''' Create a simple partition,
        in which every index from 0 to `m` gets its own equivalence class.
    '''
    return Partition([[x] for x in range(m)])

  def close(self):
    '''
    Set `self.equivalence_classes` to its transitive closure.
    So that `self` actually partitions its underlying set.

    ```python
    >>> eq1 = Partition([[0, 1, 2, 9], [7, 3, 8, 6], [4, 9, 5]])
    >>> eq1.close()
    >>> eq1.classes
    [[7, 3, 8, 6], [4, 9, 5, 0, 1, 2]]

    >>> eq2 = Partition([[0, 1, 2, 9], [7, 3, 8, 7], [9, 15]], 18)
    >>> eq2.close()
    >>> eq2.classes
    [[7, 3, 8], [9, 15, 0, 1, 2]]
    ```

    '''
    # (x == y && y == z) >= x == z
    self.equivalence_classes = _join_preimages_of_partitions(
      self.equivalence_classes, self.equivalence_classes, not FAST
    )

  def quotient(self) -> list[int]:
    ''' Return a list of integers
        whose non-trivial fibers are those contained in `self.equivalence_classes`.
    '''
    # Ensure that `self.equivalence_classes` actually partitions the underlying set.
    self.close()
    # q will be the partition associated with the equivalence relation
    # defined by self.equivalence_classes.
    # Construct a list of the right size,
    # whose contents we can reassign in an arbitrary order.
    q = [None for class_ in self.equivalence_classes for x in class_]
    for i, js in enumerate(self.equivalence_classes):
      for j in js:
        # The partition contains i at the index j.
        q[j] = i
    # Fill in the missing images.
    # The indices of these images correspond to those indices 
    # that either do not appear in self.equivalence_classes
    # or belong to singletons.
    # The quotient should therefore give them images that are not shared with other indices.
    k = len(self.equivalence_classes)
    for j, i in enumerate(q):
      if i is None:
        q[j] = k
        k += 1
    return q


def __test():
    eq1 = Partition([[0, 1, 2, 9], [7, 3, 8, 6], [4, 9, 5]])
    eq1.close()
    assert eq1.equivalence_classes == [[7, 3, 8, 6], [4, 9, 5, 0, 1, 2]]
    assert eq1.quotient() == [1, 1, 1, 0, 1, 1, 0, 0, 0, 1]

    eq2 = Partition([[0, 1, 2, 9], [7, 3, 8, 7], [9, 15]], 18)
    eq2.close()
    assert eq2.equivalence_classes == [[7, 3, 8], [9, 15, 0, 1, 2], [4], [5], [6], [10], [11], [12], [13], [14], [16], [17]]
    assert eq2.quotient() == [1, 1, 1, 0, 2, 3, 4, 0, 0, 1, 5, 6, 7, 8, 9, 1, 10, 11]

    eq3 = Partition.from_int(5)
    assert eq3.equivalence_classes == [[0], [1], [2], [3], [4]]


__test()
