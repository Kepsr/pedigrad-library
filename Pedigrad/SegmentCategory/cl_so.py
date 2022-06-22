

class SegmentObject:
  '''
  This class models the features of a segment.

  A segment over a pre-ordered set (Ω, <=) consists of
  - a pair of natural numbers (n1, n0) (where n1 >= n0),
  - an order-preserving surjection t from [n1] to [n0]
  - and a function c from [n0] to Ω.

  In this implementation,
  `domain` represents n1
  `topology` encodes the order-preserving surjection t
  `colors` encodes the function c
  A segment can be viewed as a tape with a read head.
  In this implementation, `parse` stores the position of the read head.
  '''

  def __init__(self, domain: int, topology: list[tuple[int, int]], colors: list[str]):
    assert len(colors) == len(topology), "lengths do not match"
    assert domain >= len(topology)
    self.domain = domain
    self.topology = topology
    self.colors = colors
    self.parse = 0

  def t(self, a):
    for i, (x, y) in enumerate(self.topology):
      if x <= a <= y:
        return i
    return -1

  def is_t_surjection(self):
    codomain = set(range(len(self.colors)))
    image = set(x for x in map(self.t, range(self.domain)) if x != -1)
    return codomain == image

  def _start(self):
    ''' Sets the read head to index 0 if outside the segment domain.
    '''
    if not (0 <= self.parse < len(self.topology)):
      self.parse = 0

  def patch(self, position: int, step: int = 1) -> int:
    ''' Return the index of a patch, or a node, or -1 if none is found.
        Step can any signed integer.
        Starts searching the index associated with the node
        from where the read head is
        and travels in steps of size `step`
        (positive for right and negative for left).

        Return the index of the patch (an area in brackets)
        that contains a node whose position is given as an input.
    '''
    self._start()
    if position not in range(self.domain):  # position < 0 or position >= self.domain
      return -1
    while self.parse in range(len(self.topology)):  # 0 <= self.parse < len(self.topology)
      start, stop = self.topology[self.parse]
      if start <= position <= stop:  # position in range(start, stop + 1)
        return self.parse
      if step == 0 \
      or position < start and step > 0 \
      or position > stop  and step < 0:
          return -1
      self.parse += step
    return -1

  def __repr__(self):
    ''' Display the segment.
        The read head (at position parse) is displayed as a red node.
    '''
    return ''.join(self.strings())

  def strings(self):
    if not self.topology:
      yield '()'
      return

    yield '('
    #How to display segments with a long masked start patch
    i = self.topology[0][0]
    if i < self.domain: #Should happen
      n = i - 1
      yield f'o-{n}-o' if n > 9 else 'o' * i
    else: #Special case where the whole segment is masked
      n = self.domain - 2
      yield f'o-{n}-o' if n > 9 else 'o' * self.domain
      #Bottleneck case w/t the normal case
    if 0 < i < self.domain:
      yield '|'

    #Display the inside of the segment
    self._start()
    saved_parse = self.parse
    prec_value = -1
    self.parse = 0
    n0 = self.topology[-1][1]
    while i <= min(self.domain - 1, n0):
      value = self.patch(i)
      if i == self.topology[0][0]:
        prec_value = value
      elif prec_value != value:
        prec_value = value
        yield '|'

      if value == -1:
        yield 'o'
      else:
        yield '\033[91m\033[1mo\033[0m' if self.parse == saved_parse else \
                      '\033[1mo\033[0m'
      i += 1

    #How to display segments with a long masked end patch
    yield '|'
    n = self.domain - self.topology[-1][1] - 1
    yield f'o-{n - 2}-o' if n > 11 else 'o' * n

    self.parse = saved_parse
    yield ')'

  def merge(self, folding_format: list, infimum):
    ''' Merge patches together according to a tiling structure on the segment.
        Take a tiling of the domain of the segment
        Merge groups of patches that share the same tiles.
        The tiling patterns are specified in a list of triples,
        where each triple gives a start index, a tile length, and an end index for each tiling pattern considered;
    '''
    new_topology = []
    new_colors = []
    initial = 0
    final = 0
    for j, (start, modulus, end) in enumerate(folding_format):
      initial = max(start, initial)
      new_topology.extend(self.topology[final:initial])
      new_colors.extend(self.colors[final:initial])
      if initial >= len(self.topology):
        break
      final = min(max(initial, end + 1), len(self.topology))
      saved_pos = 0
      saved_color = ''
      for i in range(initial, final):
        #Look for masked patches within the tiling
        if i + 1 < len(self.topology) \
        and self.topology[i + 1][0] - self.topology[i][1] > 1:
          saved_color = True
        #If no color has been allocated yet (first color)
        if saved_color == '':
          saved_color = self.colors[i]
        #Otherwise, take the infimum with the previous color
        else:
          saved_color = infimum(self.colors[i], saved_color)
        if i % modulus == initial % modulus:
          saved_pos = self.topology[i][0]
        if i % modulus == (initial - 1) % modulus or i == final - 1:
          if saved_color != True:
            new_topology.append((saved_pos, self.topology[i][1]))
            new_colors.append(saved_color)
          #Repeat the same process if the tiling continues
          saved_color = ''
      if j == len(folding_format) - 1:
        new_topology.extend(self.topology[final:])
        new_colors.extend(self.colors[final:])
      initial = final

    return SegmentObject(self.domain, new_topology, new_colors)

  def remove(self, patches_or_nodes: list, option='patches-given'):
    ''' Remove patches (option='patches-given') or nodes (option='nodes-given').
    '''
    removed_patches = [p for p in (
      map(self.patch, patches_or_nodes) if option == 'nodes-given' else patches_or_nodes
    ) if 0 <= p < len(self.topology)]  # Avoid p = -1
    new_topology = []
    new_colors = []
    for i, (topo, color) in enumerate(zip(self.topology, self.colors)):
      if i not in removed_patches:
        new_topology.append(topo)
        new_colors.append(color)
    return SegmentObject(self.domain, new_topology, new_colors)


def homologous(s1: SegmentObject, s2: SegmentObject):
  return s1.topology == s2.topology

def quasihomologous(s1: SegmentObject, s2: SegmentObject):
  return s1.domain == s2.domain
