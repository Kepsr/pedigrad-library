from Pedigrad.SegmentCategory import SegmentObject, CategoryOfSegments
from Pedigrad.AlignedFunctor import PointedSet, SequenceAlignment
from Pedigrad.utils import fasta


class Environment:
  '''
  This structure models the features of an aligned environment functor,
  as defined in CTGI.
  As in aligned environment functors,
  this structure is associated with a `PointedSet` (`pset`).
  The class is also equipped with a fiber operation
  (pullback along a point in the image of the functor)
  and a sequence alignment functor constructor.
  '''

  def __init__(
    self, Seg: CategoryOfSegments, pset: PointedSet, exponent: int, threshold: list
  ):
    self.Seg = Seg
    self.pset = pset
    self.spec = exponent
    for i, x in enumerate(threshold):
      if x not in self.Seg.proset:
        threshold[i] = self.Seg.proset.mask
    self.b = threshold
    for i in range(len(self.b), self.spec):
      self.b.append(self.Seg.proset.mask)

  def segment(self, xs: list, color: list):
    ''' Return a segment that is the pullback of the aligned environment functor above `xs`,
        which represents an element in one of its images.
        If `xs` contains a character that is not in the pointed set `self.pset`,
        then the node associated with that character is masked in the returned segment.
    '''
    removal = [i for i, item in enumerate(xs) if item not in self.pset]
    return self.Seg.initial(len(xs), color).remove(removal, 'nodes-given')

  def seqali(self, filename: str):
    ''' Construct a sequence aligment functor from a file of sequence alignments.
        See example 3.22 in CTGI.
    '''

    group_labels = []
    indiv = []
    names_and_sequences = fasta(filename)
    for name, sequence in names_and_sequences:
      g, i, _ = name.split(':')
      if g not in group_labels:
        group_labels.append(g)
      if i not in indiv:
        indiv.append(i)

    assert len(indiv) <= len(self.b), f"{filename} contains more individuals than the number specified in the environment."
    assert len(indiv) >= len(self.b), f"{filename} contains fewer individuals than the number specified in the environment."

    group_colors = []
    alignments = []
    check_lengths = []
    for _ in group_labels:
      group_colors.append([self.Seg.proset.mask] * len(indiv))
      alignments.append(['masked'] * len(indiv))
      check_lengths.append([])
    for name, sequence in names_and_sequences:
      gl, ind, x = name.split(':')
      i = group_labels.index(gl)
      j = indiv.index(ind)
      group_color = group_colors[i]
      alignment = alignments[i]
      check_length = check_lengths[i]
      if self.Seg.proset.geq(x, self.b[j]) or self.b[j] == True:
        group_color[j] = x
        alignment[j] = sequence
        n = len(alignment[j])
        if n not in check_length:
          check_length.append(n)

    record = []
    indexing = []
    assert len(group_labels) == len(check_lengths) == len(group_colors)
    for check_length, color in zip(check_lengths, group_colors):
      if len(check_length) == 1:
        schema = [check_length[0], color]
        indexing.append((schema, True))
        if schema not in record:
          record.append(schema)
      else:
        indexing.append(([], False))

    assert len(group_labels) == len(indexing) == len(alignments)
    base = [self.Seg.initial(*schema) for schema in record]
    database = [[] for schema in record]
    for (x, y), alignment in zip(indexing, alignments):
      if y:
        database[record.index(x)].append(alignment)
    return SequenceAlignment(self.Seg.proset ** self.spec, indiv, base, database)
