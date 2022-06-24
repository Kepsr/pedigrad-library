from Pedigrad.SegmentCategory import Proset, SegmentObject, CategoryOfSegments


class SequenceAlignment:
  ''' `SeguenceAlignment` models sequence alignment functors.
      The images of the sequence alignment functor are stored in the list `database`
      and can be queried throught the method `eval`.
  '''

  def __init__(
    self, proset: Proset, indiv: list,
    base: list[SegmentObject], database: list[list[list[int]]]
  ):
    self.indiv = indiv
    self.base = base
    self.database = database
    self.Seg = CategoryOfSegments(proset)

  def eval(self, segment: SegmentObject):
    ''' Return the image of the sequence alignment functor for the given segment.
    '''
    for other_segment, image in zip(self.base, self.database):
      if self.Seg.identity(segment, other_segment):
        return image
    return []

  def extending_category(self, segment: SegmentObject) -> list:
    ''' Compute the objects of the extending category
        for computing the right Kan extension of the functor encoded by `self.eval()`.
    '''
    return [
      (i, m)
      for i, item in enumerate(self.base)
      for m in self.Seg.homset(segment, item)
    ]

  def ran():
      ''' Compute the images of the right Kan extension of the functor
          encoded by the method `self.eval`.
      '''
      raise NotImplementedError()
