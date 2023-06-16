''' Products and coproducts in the category of partitions
'''
from .listops import parts_from_list, list_from_parts, to_indices
from .jpop import join_trans


def product_of_partitions(xs: list, ys: list) -> list[int]:
  ''' Given two lists of the same length,
      interpret them as partitions, compute their product (meet),
      and recast to a list of indices.

      According to the equivalence relation:
      ```
      (x1, y1) == (x2, y2) iff x1 == x2 and y1 == y2
      ```
  '''
  assert len(xs) == len(ys), "The lengths of `xs` and `ys` must match"
  return to_indices(list(zip(xs, ys)))


def coproduct_of_partitions(xs: list, ys: list) -> list[int]:
  ''' Given two lists of the same length,
      interpret them as partitions, compute their coproduct (join),
      and recast to a list of indices.

      According to the equivalence relation:
      ```
      (x1, y1) == (x2, y2) iff x1 == x2 or y1 == y2
      ```
  '''
  assert len(xs) == len(ys), "The lengths of `xs` and `ys` must match"
  # The i-th element indicates which part of the coproduct (join)
  # contains the i-th item.
  return list_from_parts(join_trans(
    *parts_from_list(xs),
    *parts_from_list(ys),
  ))


def __product_impl2(xs: list, ys: list) -> list[int]:
  classes = []
  idxs = []
  for x1, y1 in zip(xs, ys):
    for i, cls in enumerate(classes):
      if any(x1 == x2 and y1 == y2 for (x2, y2) in cls):
        cls.append((x1, y1))
        idxs.append(i)
        break
    else:
      idxs.append(len(classes))
      classes.append([(x1, y1)])
  return idxs

# FIXME
def __coproduct_impl2(xs: list, ys: list) -> list[int]:
  classes = []
  idxs = []
  for x1, y1 in zip(xs, ys):
    for i, cls in enumerate(classes):
      if any(x1 == x2 or y1 == y2 for (x2, y2) in cls):
        cls.append((x1, y1))
        idxs.append(i)
        break
    else:
      idxs.append(len(classes))
      classes.append([(x1, y1)])
  return idxs


def __test():
  assert   product_of_partitions('111123', 'abcccc') == [0, 1, 2, 2, 3, 4]
  assert coproduct_of_partitions('111123', 'abcccc') == [0, 0, 0, 0, 0, 0]
  assert         __product_impl2('111123', 'abcccc') == [0, 1, 2, 2, 3, 4]
  assert       __coproduct_impl2('111123', 'abcccc') == [0, 0, 0, 0, 0, 0]  


__test()
