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
          - name_of_file [Type] string
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
    .return  <- use(name_of_file,usf.fasta,self.Seg,self.b)
  [Description]
    This method constructs a sequence aligment functor from a file of sequence alignments, as shown in the development of Example 3.22 of CTGI.

'''
#------------------------------------------------------------------------------
#Dependencies: current, SegmentCategory, Useful
#------------------------------------------------------------------------------
from .cl_sal import SequenceAlignment

from Pedigrad.SegmentCategory.cl_so import SegmentObject
from Pedigrad.SegmentCategory.cl_cos import CategoryOfSegments

from Pedigrad.Useful.usf import usf, add_to
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
  def segment(self, a_list, color):
    removal = [i for i, item in enumerate(a_list) if item not in self.pset.symbols]
    return self.Seg.initial(len(a_list), color).remove(removal, 'nodes-given')
#------------------------------------------------------------------------------
  def seqali(self,name_of_file):
    group_labels = []
    indiv = []
    names,sequences = usf.fasta(name_of_file)
    for name in names:
      x, y, *_ = name
      add_to(x, group_labels)
      add_to(y, indiv)
    if len(indiv) > len(self.b):
      print("Error in Environment.seqali: "+name_of_file+" contains more individuals than the number specified in the environment.")
      exit()
    if len(indiv) < len(self.b):
      print("Error in Environment.seqali: "+name_of_file+" contains fewer individuals than the number specified in the environment.")
      exit()

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
      if self.Seg.preorder.geq(x, self.b[indi]) or self.b[indi] == True:
        group_colors[gli][indi] = x
        alignments[gli][indi] = sequences[i]
        add_to(len(alignments[gli][indi]), check_lengths[gli])
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
    base = [self.Seg.initial(*schema) for schema in record]
    database = [[] for schema in record]
    assert len(group_labels) == len(indexing) == len(alignments)
    for (x, y), alignment in zip(indexing, alignments):
      if y:
        database[record.index(x)].append(alignment)
    return SequenceAlignment(self, indiv, base, database)
#------------------------------------------------------------------------------
