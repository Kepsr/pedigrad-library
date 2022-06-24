from .jpop import _join_preimages_of_partitions, FAST

class Partition:

  def __init__(self, equivalence_classes: list[list[int]], m: int = -1):
    '''

      If `equivalence_classes` is not empty,
      `self.equivalence_classes` is set to it.
      `self.card` (the cardinality of the underlying set) will be either
      - `m` (if it is given, in which case it should be greater than
        or equal to the maximum index contained in `equivalence_relations`)
      - or the maximum index contained in the first input when no second input is given.

      e.g.
      eq1 = EquivalenceRelation([[0,1,2,9],[7,3,8,6],[4,9,5]])
      eq2 = EquivalenceRelation([[0,1,2,9],[7,3,8,7],[9,15]],18)

      If `equivalence_classes` is empty, then `m` is required.
      In this case, a simple partition is generated, 
      in which every index from 0 to `m` gets its own equivalence class.

      e.g.
      eq3 = EquivalenceRelation([], 5)
      eq3.classes = [[0], [1], [2], [3], [4], [5]]

    '''
    if equivalence_classes:
      # elements is the set underlying equivalence_classes,
      # and is got by flattening equivalence_classes.
      elements = {x for class_ in equivalence_classes for x in class_}
      assert all(x >= 0 for x in elements), "`equivalence_classes` should be a list of lists of non-negative integers."
      # The variable 'individuals' contains the number of distinct elements that
      # the first input contains.
      n = max(elements)
      if m >= 0:
        # If m is given,
        # it must be greater than or equal to the maximum of the underlying set.
        assert m >= n, "The given range is smaller than the maximum element of the given equivalence_classes."
        # Assign the value of m to .range.
        # This is done by firs passing it 'n'
        # and self.card (as shown below).
        n = m
      # self.card is the cardinality of the set underlying self.equivalence_classes
      self.card = n
      self.equivalence_classes = equivalence_classes
    else:
      assert m >= 0, "`equivalence_classes` is trivial: `m` (a non-negative integer) is required."
      self.card = m
      self.equivalence_classes = [[x] for x in range(m)]

  def close(self):
    '''
    Set `self.equivalence_classes` to its transitive closure.
    So that `self` actually partitions its underlying set.
    Singleton equivalence classes are not listed.

    ```python
    >>> eq1 = EquivalenceRelation([[0, 1, 2, 9], [7, 3, 8, 6], [4, 9, 5]])
    >>> eq1.close()
    >>> eq1.classes
    [[7, 3, 8, 6], [4, 9, 5, 0, 1, 2]]

    >>> eq2 = EquivalenceRelation([[0, 1, 2, 9], [7, 3, 8, 7], [9, 15]], 18)
    >>> eq2.close()
    >>> eq2.classes
    [[7, 3, 8], [9, 15, 0, 1, 2]]
    ```

    '''
    # (x == y && y == z) >= x == z
    self.equivalence_classes = _join_preimages_of_partitions(self.equivalence_classes, self.equivalence_classes, not FAST)

  def quotient(self) -> list[int]:
    ''' Return a list of integers of length `self.card`
        whose non-trivial fibers are those contained in `self.equivalence_classes`.

    eq1.quotient() = [1, 1, 1, 0, 1, 1, 0, 0, 0, 1]
    eq2.quotient() = [1, 1, 1, 0, 2, 3, 4, 0, 0, 1, 5, 6, 7, 8, 9, 1, 10, 11, 12]

    '''
    # Ensure that `self.equivalence_classes` actually partitions the underlying set.
    self.close()
    # q will be the partition associated with the equivalence relation
    # defined by self.equivalence_classes.
    # Construct a list of the right size,
    # whose contents we can reassign in an arbitrary order.
    q = [None] * self.card
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
