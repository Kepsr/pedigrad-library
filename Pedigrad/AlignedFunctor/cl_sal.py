from Pedigrad.SegmentCategory import Proset, SegmentObject, CategoryOfSegments


class SequenceAlignment:
  ''' This structure models the features of a sequence alignment functor.
      The images of the sequence alignment functor are stored in the list `database`
      and can be queried throught the method `eval`.
  '''

  def __init__(self, proset: Proset, indiv: list, base: list, database: list):
    self.indiv = indiv
    self.base = base
    self.database = database
    self.Seg = CategoryOfSegments(proset)

  def eval(self, segment: SegmentObject):
    ''' This method returns the image of the sequence alignment functor for the given segment.
    '''
    for x, y in zip(self.base, self.database):
      if self.Seg.identity(segment, x):
        return y
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
