from . import Proset, SegmentObject, MorphismOfSegments


def assert_strictly_increasing(xs):
  assert all(
    (i1 < i2) <= (x1 < x2)
    for i1, x1 in enumerate(xs)
    for i2, x2 in enumerate(xs)
  )
  return xs


@(lambda f: lambda *args, **kwargs: assert_strictly_increasing(f(*args, **kwargs)))
def inclusions(start: int, domain: int, holes: int) -> list[list[int]]:
  ''' Return all strictly increasing `domain - holes`-length lists
      of `int`s between `start` and `start + domain`.

      The first such list will be `list(range(0, domain - holes))`
      and the last will be `list(range(start + holes, start + domain))`.
  '''
  if holes == 0:
    return [[start + i for i in range(domain)]]

  if holes > domain:
    return []

  return [[start] + xs for xs in inclusions(start + 1, domain - 1, holes)] \
                               + inclusions(start + 1, domain - 1, holes - 1)


class CategoryOfSegments:
  '''
  This class models the features of a category of segments.
  Instances are initialized by passing a `Proset`.
  and encapsulate information related to a category structure.
  '''

  def __init__(self, proset: Proset):
    self.proset = proset

  @staticmethod
  def identity(segment1: SegmentObject, segment2: SegmentObject) -> bool:
    ''' Is there an identity morphism from the first segment to the second?
    '''
    return segment1.domain   == segment2.domain \
    and    segment1.topology == segment2.topology \
    and    segment1.colors   == segment2.colors

  @staticmethod
  def initial(domain: int, color: str) -> SegmentObject:
    ''' Return a local initial object in the category
        with a uniform color equal to `color`.
        where the local aspect is determined by the colors of the segment.
    '''
    return SegmentObject(
      domain,
      topology=[(i, i) for i in range(domain)],
      colors=[color] * domain
    )

  def homset(self, source: SegmentObject, target: SegmentObject) -> list[MorphismOfSegments]:
    ''' Return the hom-set of a pair of segments.
    '''
    if target.domain < source.domain:
      return []

    return [arrow for arrow in [
        MorphismOfSegments(source, target, f1, self.proset.geq)
        for f1 in inclusions(0, target.domain, target.domain - source.domain)
        # Each list f1 is treated as a mapping from `int` to `int` (i -> f1[i])
    ] if arrow.defined]
