#------------------------------------------------------------------------------
#MorphismOfSegments (Class) | 3 objects | 2 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .defined  [Type] bool
  .f0       [Type] list(int)
  .f1       [Type] list(int)

[Methods]
  .__init__
        [Inputs: 4]
          - source  [Type] SegmentObject
          - target  [Type] SegmentObject
          - f1      [Type] list(int)
          - geq     [Type] fun 'a * 'a -> bool
        [Outputs: 0]
  ._compute_f0
        [Inputs: 1]
          - mapping       [Type] list(int * int)
        [Outputs: 1]
          - return        [Type] bool

[General description]
  This structure models the features of a morphism of segments (as defined in CTGI). The constructor stores the data necessary to describe a morphism of segments: it will therefore take a source segment, a target segment, a map relating the domains of the source to the domain of the target, and a pre-order relation compatible with the pre-ordered sets of two the segments.

>>> Method: .__init__
  [Actions]
    .source   <- use(source)
    .target   <- use(target)
    .defined  <- use()
    .f0       <- use(source,target,f1,self._compute_f0)
    .f1       <- use(f1)
  [Description]
    This is the constructor of the class.

>>> Method: ._compute_f0
  [Actions]
    return        <- use(mapping)
    .f0           <- use(mapping)
  [Description]
    Checks that [mapping] is a function and stores the indexed image of
  the function in the object [f0].
'''
#------------------------------------------------------------------------------
from Pedigrad.SegmentCategory.cl_so import SegmentObject
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class MorphismOfSegments:
#------------------------------------------------------------------------------
  def __init__(self, source: SegmentObject, target: SegmentObject, f1: list[int], geq):
    assert type(source) is type(target) is SegmentObject
    self.source = source
    self.target = target
    self.f0 = []
    self.f1 = f1

    if source.domain == target.domain:
      assert len(f1) == source.domain
      assert max(f1) == target.domain - 1

    self.defined = self.is_valid(geq)

  def is_valid(self, geq):
    # Is this morphism valid?
    if len(self.f1) != self.source.domain \
    or max(self.f1) > self.target.domain - 1:
      return False

    self.target.parse = 0
    self.source.parse = 0

    # Check that a commutative diagram commutes
    mapping = [
      (self.source.patch(i), self.target.patch(j))
      for i, j in enumerate(self.f1)
    ]
    if not self._compute_f0(mapping):
      return False

    # Check that colors decrease from source to target
    for i, j in enumerate(self.f0):
      if j != -1 \
      and not geq(self.source.colors[i], self.target.colors[j]):
        return False

#------------------------------------------------------------------------------
  def _compute_f0(self, mapping: list[tuple]):
    self.f0 = []
    if not mapping:
      return True

    sorted_mapping = sorted(mapping, key = lambda x: x[0])
    i = 0
    while i < len(sorted_mapping):
      x, y = sorted_mapping[i]
      i += 1
      #if x is masked, then y has to be masked
      if x == -1:
        if y != -1:
          return False
      #if x is not masked, then y = f(x) has to be unique
      else:
        # Check the uniqueness of y = f(x)
        for x2, y2 in sorted_mapping[i:]:
          if x2 != x:
            break
          if y2 != y:
            return False
          i += 1
        self.f0.append(y)
    return True
#------------------------------------------------------------------------------
