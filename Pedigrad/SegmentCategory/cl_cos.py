#------------------------------------------------------------------------------
#CategoryOfSegments (Class) | 1 object | 4 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .proset [Type] Proset

[Methods]
  .__init__
        [Inputs: 1]
          - proset [Type] Proset
        [Outputs: 0]
  .identity
        [Inputs: 2]
          - segment1  [Type] SegmentObject
          - segment2  [Type] SegmentObject
        [Outputs: 1]
          - return    [Type] bool
  .initial
        [Inputs: 2]
          - domain  [Type] int
          - color   [Type] list('a)
        [Outputs: 1]
          - return  [Type] SegmentObject
  .homset
        [Inputs: 2]
          - source  [Type] SegmentObject
          - target  [Type] SegmentObject
        [Outputs: 1]
          - homset  [Type] list(MorphismOfSegments)

'''
#------------------------------------------------------------------------------
from .cl_pro import Proset
from .cl_so import SegmentObject
from .cl_mos import MorphismOfSegments

#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
def inclusions(start: int, domain: int, holes: int) -> list[list[int]]:
  '''
  inclusions
        [Inputs: 1]
          - start   [Type] int
          - domain  [Type] int
          - holes   [Type] int
        [Outputs: 2]
          - return  [Type] list(list(int))

  >>> Function: inclusions
  [Description]
    This function computes the list of lists f whose implicit mappings i -> f[i] represent increasing inclusions from the ordered set {0,1,...,domain-holes-1} to the ordered set {start,start+1,...,start+domain-1}
  '''
  if holes == 0:
    return [[start + i for i in range(domain)]]

  if holes > domain:
    return []

  return [
    x + i
    for i in inclusions(start + 1, domain - 1, holes)
    for x in inclusions(start, 1, 0)
  ] + inclusions(start + 1, domain - 1, holes - 1)


class CategoryOfSegments:
  '''
  This class models the features of a category of segments.
  Instances are initialized by passing a Proset.
  and encapsulates information related to a category structure.
  '''
#------------------------------------------------------------------------------
  def __init__(self, proset: Proset):
    self.proset = proset
#------------------------------------------------------------------------------
  @staticmethod
  def identity(segment1: SegmentObject, segment2: SegmentObject):
    ''' Is there an identity morphism from the first segment to the second?
    '''
    return segment1.domain   == segment2.domain \
    and    segment1.topology == segment2.topology \
    and    segment1.colors   == segment2.colors
#------------------------------------------------------------------------------
  @staticmethod
  def initial(domain: int, color: str):
    ''' Return a local initial object in the category
        with a uniform color equal to `color`.
        where the local aspect is determined by the colors of the segment.
    '''
    return SegmentObject(
      domain,
      topology=[(i, i) for i in range(domain)],
      colors=[color] * domain
    )
#------------------------------------------------------------------------------
  def homset(self, source: SegmentObject, target: SegmentObject):
    ''' Return the hom-set of a pair of segments.
    '''
    if target.domain - source.domain < 0:
      return []

    return list(filter(lambda arrow: arrow.defined, [
        MorphismOfSegments(source, target, i, self.proset.geq)
        for i in inclusions(0, target.domain, target.domain - source.domain)
    ]))
#------------------------------------------------------------------------------
