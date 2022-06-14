

class PointedSet:
  '''
  This class models a pointed set (also called a based set or rooted set),
  an ordered pair (X, x0) of a set X and an element x0 in X called the base point.
  A `PointedSet` stores a list `symbols` of the elements of the set,
  and an index `index` into `symbols` where the base point is located.
  '''

  def __init__(self, symbols: list, index: int):
    assert 0 <= index < len(symbols)
    self.symbols = symbols
    self.index = index

  def point(self):
    ''' Return the base point.
    '''
    return self.symbols[self.index]
