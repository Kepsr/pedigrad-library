from . import SegmentObject


class MorphismOfSegments:
  ''' This structure models the features of a morphism of segments (as defined in CTGI).
  '''

  def __init__(self, source: SegmentObject, target: SegmentObject, f1: list[int], geq):
    ''' Store the data necessary to describe a morphism of segments, namely:
        a source segment and a target segment,
        a map relating the domain of the source to the domain of the target,
        and a pre-order relation compatible with the pre-ordered sets of the two segments,
    '''
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
    or max(self.f1) >  self.target.domain - 1:
      return False

    self.target.parse = 0
    self.source.parse = 0

    # Check that the diagram commutes
    mapping = [
      (self.source.patch(i), self.target.patch(j)) for i, j in enumerate(self.f1)
    ]
    if not self._compute_f0(mapping):
      return False

    # Check that colors decrease from source to target
    return all(
      j == -1 or geq(self.source.colors[i], self.target.colors[j])
      for i, j in enumerate(self.f0)
    )

  def _compute_f0(self, mapping: list):
    ''' Check that `mapping` is a function
        and store the indexed image of the function in `self.f0`.
    '''
    self.f0 = []
    if not mapping:
      return True

    sorted_mapping = sorted(mapping)
    i = 0
    while i < len(sorted_mapping):
      x, y = sorted_mapping[i]
      i += 1
      # If x is masked, y must be masked too
      if x == -1:
        if y == -1:
          continue
        return False

      # If x is not masked, y = f(x) must be unique
      for x2, y2 in sorted_mapping[i:]:
        if x2 != x:
          break
        if y2 != y:
          return False
        i += 1
      self.f0.append(y)
      # Now go to the next pair whose x is different from the current one
    return True
