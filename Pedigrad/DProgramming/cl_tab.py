#------------------------------------------------------------------------------
#Table (Class) | 3 objects | 9 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .name [Type] type

[Methods]
  .name
        [Inputs: ]
          - name [Type] type
        [Outputs: ]
          - name [Type] type

[General description]
  This structure models the features of a score table for the purpose of Dynamic programming. In particular, it encodes the dynamic programming algorithm required to be able to do the type of analysis discussed in CTGI for mechanism recognition.

>>> Method: .name

  [Actions]
    .object  <- use(class & arg)
    .output <- use(class & arg)

  [Description]
    This method


'''
#------------------------------------------------------------------------------
#Dependencies: current, sys
#------------------------------------------------------------------------------
import sys
from .cl_seq import Sequence
from .cl_tre import Tree

#------------------------------------------------------------------------------
#CODE
#-----------------------------------------------------------------------------
class Table:
#-----------------------------------------------------------------------------
  def __init__(self, seq1: Sequence, seq2: Sequence):
    self.seq1 = seq1
    self.seq2 = seq2
    self.content = [[
      '.'
      for j in range(len(self.seq2.seq) + 2)
    ] for i in range(len(self.seq1.seq) + 2)]
    self.content[0][0] = '.'
    self.content[1][1] = 0
    for i, x in enumerate(self.seq1.seq):
      self.content[i+2][0] = x
      self.content[i+2][1] = 0
    for j, y in enumerate(self.seq2.seq):
      self.content[0][j+2] = y
      self.content[1][j+2] = 0
#-----------------------------------------------------------------------------
  def incidence(self):
    for i, x in enumerate(self.seq1.seq):
      for j, y in enumerate(self.seq2.seq):
        self.content[i+2][j+2] = int(x == y)
#-----------------------------------------------------------------------------
  def fillout(self):
    for i, x in enumerate(self.seq1.seq):
      for j, y in enumerate(self.seq2.seq):
        self.content[i+2][j+2] = max(
          self.content[i+2][j+2] + self.content[i+1][j+1] if x == y else
          self.content[i+2][j+2],
          self.content[i+2][j+1],
          self.content[i+1][j+2]
        )
#-----------------------------------------------------------------------------
  def choices(self, i: int, j: int):
    choices = []
    if 0 <= i < len(self.seq1.seq) and 0 <= j < len(self.seq2.seq):
      m = max(self.content[i+2][j+2], self.content[i+2][j+1], self.content[i+1][j+2])
      # diagonal
      if self.seq1.seq[i] == self.seq2.seq[j] and self.content[i+2][j+2] == m:
        choices.append([i-1, j-1, 'd'])
      # vertical and horizontal
      if self.content[i+2][j+1] == m:
        choices.append([i, j-1, 'h'])
      if self.content[i+1][j+2] == m:
        choices.append([i-1, j, 'v'])
    if i == -1 and 0 <= j < len(self.seq2.seq):
      choices.append([i, j-1, 'h'])
    if j == -1 and 0 <= i < len(self.seq1.seq):
      choices.append([i-1, j, 'v'])
    return choices
#-----------------------------------------------------------------------------
  def tree(self, i: int, j: int, move):
    choices = self.choices(i, j)
    if not choices:
      return Tree("leaf")

    children = [self.tree(x, y, m) for x, y, m in choices]
    s1 = '-' if i == -1 else self.seq1.seq[i]
    s2 = '-' if j == -1 else self.seq2.seq[j]
    return Tree([s1, s2, move], children)
#-----------------------------------------------------------------------------
  def traceback(self, debug: bool):
    tree = self.tree(len(self.seq1.seq) - 1, len(self.seq2.seq) - 1, 'end')
    if debug:
      print("\ntree")
      tree.stdout()
    return tree.paths()
#-----------------------------------------------------------------------------
  def read_path(self, path: str, move: str):
    if not path:
      return [], []

    seq1 = []
    seq2 = []
    head = path[-1]
    if move in ['d', 'start']:
      seq1.append(head[0])
      seq2.append(head[1])
    if move == 'h':
      seq1.append('-')
      seq2.append(head[1])
    if move == 'v':
      seq1.append(head[0])
      seq2.append('-')
    new_path = path[:-1]
    s1, s2 = self.read_path(new_path, head[2])
    return seq1 + s1, seq2 + s2
#-----------------------------------------------------------------------------
  def write(self, filename: str, mode: str = 'a', debug=False, display=True):
    paths = self.traceback(debug)

    if debug:
        print("\npaths")
        for path in paths:
          print(path)

    outputs = [self.read_path(path, 'start') for path in paths]

    with open(filename, mode) as file:
      for i, output in enumerate(outputs):
        assert len(output) == 2
        x, y = output
        n1 = f'>{i}:{self.seq1.name}:{self.seq1.color}'
        s1 = ''.join(x)
        n2 = f'>{i}:{self.seq2.name}:{self.seq2.color}'
        s2 = ''.join(y)
        for line in [n1, s1, n2, s2]:
          file.write(line + '\n')
        if display:
          for line in [n1, s1, n2, s2]:
            sys.stdout.write(line + '\n')

    return outputs
#-----------------------------------------------------------------------------
  def stdout(self):
    for x in self.content:
      for y in x:
        sys.stdout.write(str(y) + " | ")
      sys.stdout.write('\n')
      sys.stdout.flush()
#-----------------------------------------------------------------------------
