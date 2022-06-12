#------------------------------------------------------------------------------
#SegmentObject (Sublass) | 4 objects | 6 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .domain   [Type] int
  .topology [Type] list(int * int)
  .colors   [Type] list('a)
  .parse    [Type] int

[Methods]
  .__init__
        [Inputs: 3]
          - domain    [Type] int
          - topology  [Type] list(int * int)
          - colors    [Type] list('a)
        [Outputs: 0]
  ._start
        [Inputs: 0]
        [Outputs: 0]
  .patch
        [Inputs: 2]
          - position  [Type] int
          - search    [Type] string
        [Outputs: 1]
          - return    [Type] int
  .display
        [Inputs: 0]
        [Outputs: 0]
  .merge
        [Inputs: 2]
          - folding_format  [Type] list(int * int * int)
          - infimum         [Type] fun: 'a * 'a -> 'a
        [Outputs: 1]
          - return          [Type] SegmentObject
  .remove
        [Inputs: 2]
          - a_list  [Type] list
          - option  [Type] string
        [Outputs: 1]
          - return  [Type] SegmentObject

[General description]
  This structure models the features of segments (as defined in CGTI). A segment can be seen as a tape equipped with a read head, whose position is stored in the object [parse] and is displayed through the method [display] as a red node. The method [patch] allows one to return the index of the patch (an area in brackets) that contains a node whose position is given as an input. Note that the method [patch] starts searching the index associated with the node from where the read head is and only goes in a direction (left or right) specified through its second input; the method [merge] takes a tiling of the domain of the segment and merges groups of patches that share the same tiles. The tiling patterns are specified in a list of triples, where each triple gives a start index, a tile length, and an end index for each tiling pattern considered; the method [remove] removes either a node or a patch (from the segment) at the index given in the first argument depending on whether the second argument is equal to 'nodes-given' or is not specified.

>>> Method: .__init__
  [Actions]
    .domain   <- use(domain)
    .topology <- use(topology)
    .colors   <- use(colors)
    .parse    <- use()
  [Description]
    This method is the constructor of the class.

>>> Method: ._start
  [Actions]
    .parse  <- use(self.parse,self.topology)
  [Description]
    Sets the read head to index 0 if the read head is outside of the
  segment domain.

>>> Method: .patch
  [Actions]
    return  <- use(self.parse,self.topology,position,search)
  [Description]
    Returns the index of a patch, or a node, or -1 if none is found.

>>> Method: .display
  [Actions]
    sys.stdout  <- use(self._start,self.parse)
  [Description]
    Displays the segment.

>>> Method: .display
  [Actions]
    sys.stdout  <- use(self._start,self.parse)
  [Description]
    Displays the segment on the standard output.

>>> Method: .merge
  [Actions]
    return  <- use(self.domain,self.topology,self.colors,self.__init__)
  [Description]
    Merges patches together according to a tiling structure on the segment.

>>> Method: .remove
  [Actions]
    return  <- use(self.domain,self.topology,self.colors,self.__init__)
  [Description]
    Removes patches (option = 'patches-given') or nodes (option = 'nodes-given')
  from the segment.
'''
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class SegmentObject:
#------------------------------------------------------------------------------
  def __init__(self, domain: int, topology: list[list[int]], colors: list):
    assert len(colors) == len(topology), "lengths do not match"
    self.domain = domain
    self.topology = topology
    self.colors = colors
    self.parse = 0
#------------------------------------------------------------------------------
  def _start(self):
    if not (0 <= self.parse < len(self.topology)):
      self.parse = 0
#------------------------------------------------------------------------------
  def patch(self, position: int, search = ">1"):
    self._start()
    if not (0 <= position < self.domain):
      return -1
    while 0 <= self.parse < len(self.topology):
      if position < self.topology[self.parse][0]:
        if search[0] != '<':
          return -1
        self.parse -= int(search[1:])
      elif position > self.topology[self.parse][1]:
        if search[0] != '>':
          return -1
        self.parse += int(search[1:])
      return self.parse
    return -1
#------------------------------------------------------------------------------
  def display(self):
    print(''.join(self.strings()))

  def strings(self):
    if not self.topology:
      yield '()'
      return

    yield '('
    #How to display segments with a long masked start patch
    i = self.topology[0][0]
    if i < self.domain: #Should happen
      yield 'o-' + str(i - 1) + '-o' if i > 10 else \
            'o' * i
    else: #Special case where the whole segment is masked
      yield 'o-' + str(self.domain - 2) + '-o' if self.domain > 11 else \
            'o' * self.domain  #Bottleneck case w/t the normal case
    if 0 < i < self.domain:
      yield '|'

    #Display the inside of the segment
    self._start()
    saved_parse = self.parse
    prec_value = -1
    self.parse = 0
    while i <= min(self.domain - 1, self.topology[-1][1]):
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
    if self.domain - self.topology[-1][1] - 1 > 11:
      yield '|o-' + str(self.domain - self.topology[-1][1] - 3) + '-o'
    else:
      yield '|' + 'o' * (self.domain - self.topology[-1][1] - 1)

    self.parse = saved_parse
    yield ')'
#------------------------------------------------------------------------------
  def merge(self, folding_format: list, infimum):
    new_topology = []
    new_colors = []
    initial = 0
    final = 0
    for step, f in enumerate(folding_format):
      start, modulo, end = f
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
        if i % modulo == initial % modulo:
          saved_pos = self.topology[i][0]
        if i % modulo == (initial - 1) % modulo or i == final - 1:
          if saved_color != True:
            new_topology.append((saved_pos, self.topology[i][1]))
            new_colors.append(saved_color)
          #Repeat the same process if the tiling continues
          saved_color = ''
      if step == len(folding_format) - 1:
        new_topology.extend(self.topology[final:])
        new_colors.extend(self.colors[final:])
      initial = final

    return SegmentObject(self.domain, new_topology, new_colors)
#------------------------------------------------------------------------------
  def remove(self, a_list: list, option = 'patches-given'):
    removed_patches = [p for p in (
      map(self.patch, a_list) if option == 'nodes-given' else a_list
    ) if 0 <= p < len(self.topology)]  # Avoid p = -1
    new_topology = []
    new_colors = []
    for i, (topo, color) in enumerate(zip(self.topology, self.colors)):
      if i not in removed_patches:
        new_topology.append(topo)
        new_colors.append(color)
    return SegmentObject(self.domain, new_topology, new_colors)
#------------------------------------------------------------------------------
