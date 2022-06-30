from Pedigrad.utils import nub

FAST = True

def join_partitions(
  equivalence_classes1: list[list[int]], equivalence_classes2: list[list[int]],
  speed_mode: bool = not FAST
):
  '''
  Given two lists, each containing disjoint sets of indices in some range,
  return the list of the maximal unions of internal lists
  that intersect within the concatenation of the two input lists (see below).
  The `bool` `speed_mode` should indicate whether one of the input lists
  may contain two different sublists with the same element.

  In practice, the two input lists would be obtained as outputs of `partition_from_list`
  for two input lists of the same length.

  e.g.
  Considering the following lists of lists of indices
  ```
  p1 = [[0, 3], [1, 4], [2]]
  p2 = [[0, 1], [2], [3], [4]]
  ```
  we can notice that
  [0,3] intersects with [0,1] and [3]
  [0,1] intersects with [1,4] and [0,3]
  [1,4] intersects with [0,1] and [4]
  [2] intersects with [2]
  so that we have
  join_partitions(p1, p2, FAST) = [[1, 4, 0, 3], [2]]
  ```

  In terms of implementation, the algorithm considers each internal list
  of p1 and searches for the lists of p2 that intersect it.
  If an intersection is found between two internal lists,
  it merges the two internal lists in p1 and empties that of p2
  (the list is removed).
  The function continues until all the possible intersections have been checked.
  '''
  # Make copies so as not to modify the inputs
  # and eliminate repeats in each equivalence class:
  tmp1 = [nub(xs) for xs in equivalence_classes1]
  tmp2 = [nub(xs) for xs in equivalence_classes2]
  for xs1 in tmp1:
    # Get the union of xs1 with every equivalence class in tmp2 that intersects it
    for x1 in xs1:
      for i, xs2 in enumerate(tmp2):
        if any(x1 == x2 for x2 in xs2):
          xs1 = nub(xs1 + xs2)  # The union of xs1 and xs2
          tmp2.pop(i)
          if speed_mode == FAST:
            # Assume x1 occurs nowhere else in tmp2
            # assert x1 not in (x for xs in tmp2 for x in xs)
            break
    # Append the union to tmp2
    tmp2.append(xs1)
  return tmp2


def __test():
  p1 = [[0, 3], [1, 4], [2]]
  p2 = [[0, 1], [2], [3], [4]]
  x = join_partitions(p1, p2, FAST)
  assert (x == [[1, 4, 0, 3], [2]]), x

__test()


# Long description of what join_partitions(p1, p2, FAST) does
# for p1 = [[0, 3], [1, 4], [2]]; p2 = [[0, 1], [2], [3], [4]]

# The element 0 of [0,3] is sought in the list [0,1] of p2;
# The element 0 is found;
# The lists [0,3] and [0,1] are merged in p1 and [0,1] is emptied from p2 as follows:
# p1 = [[0, 3, 1], [1, 4], [2]]
# p2 = [[], [2], [3], [4]];
# Because the element 0 has now been found in p2 and the third input was set to FAST,
# no other sublist of p2 is supposed to contain the element 0 and the search of the element 0 stops here.
# Note that if not(FAST) were given in the third argument,
# then the earlier union operation would also be operated on the remaining sublists of p2
# (e.g. because the sublists of p2 could still contain the element 0).

# The element 3 of [0, 3] is sought in the list [] of p2;
# The element 3 is not found (continues)
# The element 3 of [0, 3] is sought in the list [2] of p2;
# The element 3 is not found (continues)
# The element 3 of [0, 3] is sought in the list [3] of p2;
# The element 3 is found;
# The lists [0,3] and [3] are merged in p1 and [3] is emptied from p2 as follows:
# p1 = [[0, 3, 1], [1, 4], [2]]
# p2 = [[], [2], [], [4]];
# The element 3 has now been found in p2 and does not need to be sought again.

# All elements of the initial list [0, 3] have been sought.
# The first lists of p1 is appended to p2 in order to ensure the transitive computation of the maximal unions through the next interations.
# The list [0, 3, 1] of p1 is emptied as follows:
# p1 = [[], [1, 4], [2]]
# p2 = [[], [2], [], [4], [0, 3, 1]];

# Repeat the previous procedure with respect to the list [1, 4] of p1.
# We obtain the following pair:
# p1 = [[], [], [2]]
# p2 = [[], [2], [], [], [], [1, 4, 0, 3]]

# Repeat the previous procedure with respect to the remaining list [2] of p1.
# We obtain the following pair:
# p1 = [[], [], []]
# p2 = [[], [], [], [], [], [1, 4, 0, 3], [2]]

# The function stops because there is no more list to process in p1.
# The output is all the non-empty lists of p2; i.e. [[1, 4, 0, 3], [2]]
