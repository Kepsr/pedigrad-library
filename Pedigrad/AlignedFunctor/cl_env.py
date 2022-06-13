#------------------------------------------------------------------------------
#Environment (Class) | 4 objects | 3 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .Seg  [Type] CategoryOfSegments('a)
  .pset [Type] PointedSet('b)
  .spec [Type] int
  .b    [Type] list('a)

[Methods]
  .__init__
        [Inputs: 4]
          - Seg       [Type] CategoryOfSegments('a)
          - pset      [Type] PointedSet('b)
          - exponent  [Type] int
          - threshold [Type] list('a)
        [Outputs: 0]
  .segment
        [Inputs: 2]
          - a_list  [Type] list('b)
          - color   [Type] 'a
        [Outputs: 1]
          - return [Type] SegmentObject('a)
  .seqali
        [Inputs: 1]
          - filename [Type] string
        [Outputs: 1]
          - return [Type] SequenceAlignment

[General description]
  This structure models the features of an aligned environment functors, as defined in CTGI. As in aligned environment functors, this structure is associated with a PointedSet item [pset]. The class is also equipped with a fiber operation (pullback along a point in the image of the functor) and a sequence alignment functor constructor call. Specifically, the method [segment] returns a segment that is the pullback of the aligned environment functor above any input list that represents an element in one of its images. If the input list contains a character that is not in the object [pset.symbols], then the node associated with that character is masked in the returned segment. Aditionally, the method [seqali] construct a sequence aligment functor  from a file a sequence alignments, as shown in the development of CGTI.

>>> Method: .__init__
  [Actions]
    .Seg    <- use(Seg)
    .pset   <- use(pset)
    .spec   <- use(exponent)
    .b       <- use(threshold,Seg,spec)
  [Description]
    This is the constructor of the class.

>>> Method: .segment
  [Actions]
    .return   <- use(a_list,color,self.Seg,self.pset)
  [Description]
    This method returns a segment that is the pullback of the underlying environment functor above the input list. If the list contains a character that is not in the list self.pset.symbols, then the node associated with that character is masked in the returned segment.

>>> Method: .seqali
  [Actions]
    .return  <- use(filename,fasta,self.Seg,self.b)
  [Description]
    This method constructs a sequence aligment functor from a file of sequence alignments, as shown in the development of Example 3.22 of CTGI.

'''
#------------------------------------------------------------------------------
#Dependencies: current, SegmentCategory
#------------------------------------------------------------------------------
from .cl_sal import SequenceAlignment

from Pedigrad.SegmentCategory.cl_so import SegmentObject
from Pedigrad.SegmentCategory.cl_cos import CategoryOfSegments

from Pedigrad.utils import fasta
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class Environment:
#------------------------------------------------------------------------------
  def __init__(self, Seg: CategoryOfSegments, pset, exponent: int, threshold: list):
    self.Seg = Seg
    self.pset = pset
    self.spec = exponent
    self.b = threshold
    for i in range(len(self.b)):
      if not self.Seg.preorder.presence(self.b[i]):
        self.b[i] = self.Seg.preorder.mask
    for i in range(len(self.b), self.spec):
      self.b.append(self.Seg.preorder.mask)
#------------------------------------------------------------------------------
  def segment(self, a_list: list, color: list):
    removal = [i for i, item in enumerate(a_list) if item not in self.pset.symbols]
    return self.Seg.initial(len(a_list), color).remove(removal, 'nodes-given')
#------------------------------------------------------------------------------
  def seqali(self, filename: str):

    group_labels = []
    indiv = []
    names, sequences = fasta(filename)
    for name in names:
      x, y, *_ = name
      if x not in group_labels:
        group_labels.append(x)
      if y not in indiv:
        indiv.append(y)

    assert len(indiv) <= len(self.b), f"Error in Environment.seqali: {filename} contains more individuals than the number specified in the environment."
    assert len(indiv) >= len(self.b), f"Error in Environment.seqali: {filename} contains fewer individuals than the number specified in the environment."

    group_colors = []
    alignments = []
    check_lengths = []
    for _ in group_labels:
      group_colors.append([self.Seg.preorder.mask] * len(indiv))
      alignments.append(['masked'] * len(indiv))
      check_lengths.append([])
    for i, name in enumerate(names):
      gl, ind, x = name
      gli = group_labels.index(gl)
      indi = indiv.index(ind)
      group_color = group_colors[gli]
      alignment = alignments[gli]
      check_length = check_lengths[gli]
      if self.Seg.preorder.geq(x, self.b[indi]) or self.b[indi] == True:
        group_color[indi] = x
        alignment[indi] = sequences[i]
        n = len(alignment[indi])
        if n not in check_length:
          check_length.append(n)

    record = []
    indexing = []
    assert len(group_labels) == len(check_lengths) == len(group_colors)
    for check_length, color in zip(check_lengths, group_colors):
      if len(check_length) == 1:
        schema = [check_length[0], color]
        indexing.append([schema, True])
        if schema not in record:
          record.append(schema)
      else:
        indexing.append([[], False])

    assert len(group_labels) == len(indexing) == len(alignments)
    base = [self.Seg.initial(*schema) for schema in record]
    database = [[] for schema in record]
    for (x, y), alignment in zip(indexing, alignments):
      if y:
        database[record.index(x)].append(alignment)
    return SequenceAlignment(self, indiv, base, database)
