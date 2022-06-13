#------------------------------------------------------------------------------
#PreOrder (Class) | 4 objects | 7 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .relations  [Type] list(list('a))
  .transitive [Type] bool
  .mask       [Type] bool
  .cartesian  [Type] int

[Methods]
  .__init__
        [Inputs: 2+]
          - filename  [Type] char
          - cartesian     [Type] int
          - *args         [Type] list
        [Outputs: 0]
  .closure
        [Inputs: 0]
        [Outputs: 0]
  ._geq
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - return    [Type] bool
  .geq
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - return    [Type] bool
  ._inf
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - return    [Type] 'a
  .inf
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - infimum   [Type] 'a

[General description]
  This class models the features of a pre-ordered set. The pre-order relations are specified through either a file [filename] or another PreOrder item passed to the constructor [__init__]. The method [closure] computes the transitive closure of the pre-order relations stored in the object [relations]; the method [geq] returns a Boolean value specifying whether there is a pre-order relation between two given elements of the pre-ordered set; the method [inf] returns the infimum of two elements of the pre-ordered set; and the method __contains__ returns a Boolean value specifying whether an element belongs to the pre-ordered set.

>>> Method: .__init__
  [Actions]
    .relations  <- use(filename,*args)
    .transitive <- use(*args)
    .mask       <- use(filename,*args)
    .cartesian  <- use(cartesian)
  [Description]
    This method is the constructor of the class.

>>> Method: .closure
  [Actions]
    .transitive <- use()
    .relations  <- use(self.relations)
  [Description]
    Computes the transitive closure of the pre-order relations in the object
  [relations]

>>> Method: ._qeq
  [Actions]
    return <- use(self.relations,element1,element2)
  [Description]
    Specifies whether element1 is greater than or equal to element2.

>>> Method: .qeq
  [Actions]
    return <- use(self.cartesian,self._geq,element1,element2)
  [Description]
    Cartesian version of the method [_geq].

>>> Method: ._inf
  [Actions]
    return <- use(self.relations,self.mask,self.geq,element1,element2)
  [Description]
    Computes the infimum of element1 and element2.

>>> Method: .inf
  [Actions]
    infimum <- use(self.cartesian,self._inf,element1,element2)
  [Description]
    Cartesian version of the method [_inf].

'''
#------------------------------------------------------------------------------
#Global variables
#------------------------------------------------------------------------------
'''
The list _ascii_for_text defined below specifies the characters that can be used
as a variable name for the elements of the pre-ordered set.
ASCII code 33: !
ASCII code between 48 to 57 : [0-9]
ASCII code 64 : @
ASCII code between 65 to 90 : [A-Z]
ASCII code 95 : _
ASCII code between 97 to 122 : [a-z]
'''
heading_separators = list(range(0,33)) + list(range(34,48)) + list(range(58,64)) + list(range(91,95)) + [96] + list(range(123,256))

heading_separators = [chr(sep) for sep in heading_separators]

separators = heading_separators + ['!']
#------------------------------------------------------------------------------
from Pedigrad.utils import read_until
from functools import reduce
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class PreOrder:
#------------------------------------------------------------------------------
  def __init__(self, relations: list, transitive: bool, mask: bool, cartesian: int):
    self.relations = relations
    self.transitive = transitive
    self.mask = mask
    self.cartesian = cartesian

  def copy(self, cartesian):
    assert cartesian > 0
    return PreOrder(self.relations, self.transitive, self.mask, cartesian)

  @staticmethod
  def from_file(filename: str, cartesian = 0):
    assert filename, "filename cannot be empty"

    self = PreOrder(relations=[], transitive=False, mask=False, cartesian=cartesian)

    with open(filename, 'r') as file:

      # Search the key words '!obj:' or 'obj:'
      list_of_objects = []
      while True:
        heading = read_until(file, heading_separators, [':'])
        if not heading:
          raise Exception(f"\'obj:\' was not found im {filename}")
        if heading[-1] == "!obj":
          self.mask = True
          break
        if heading[-1] == "obj":
          break

      # Search the key word 'rel:'
      found_rel = False
      while not found_rel:
        tokens = read_until(file, separators, ['#', ':'], inclusive=True)
        if tokens == ['']:
          break
        if tokens[-2:] == ["rel", ":"]:
          objects = tokens[:-2]
          found_rel = True
        else:
          objects = tokens[:-1]
          read_until(file, separators, ['\n'])

        # Construct [list_of_objects] and [self.relations]
        for obj in objects:
          # assert obj in list_of_objects == [obj] in self.relations
          if obj not in list_of_objects:
            list_of_objects.append(obj)
          if [obj] not in self.relations:
            self.relations.append([obj])

      if not found_rel:
        # If the key word 'rel:' is not found
        return

      # If the key word 'rel:' was found, search the symbols '>' and ';'
      while True:

        while True:
          tokens = read_until(file, separators, ['#', '>'], inclusive=True)
          successors = []
          if tokens == ['']:
            break
          successors = tokens[:-1]
          if tokens[-1] == ">":
            break
          read_until(file, separators, ['\n'])

        # Complete [self.relations] with [predecessors] for each successor
        predecessors = read_until(file, separators, [';'])
        for successor in set(successors):
          try:
            i = list_of_objects.index(successor)
            for predecessor in predecessors:
              if predecessor not in self.relations[i]:
                self.relations[i].append(predecessor)
          except ValueError:  # successor is not in list_of_objects
            print(f"Warning: in \'{filename}\': {successor} is not an object")
        if not successors or not predecessors:
          break  # EOF

    return self
#------------------------------------------------------------------------------
  def closure(self):
    if not self.transitive:
      self.transitive = True
      for i, relation1 in enumerate(self.relations):
        keep_going = True
        while keep_going:
          keep_going = False
          for elt in relation1:
            for j, relation2 in enumerate(self.relations):
              if i != j and elt == relation2[0]:
                for new_elt in relation2:
                  if new_elt not in relation1:
                    keep_going = True
                    relation1.append(new_elt)
                  else:
                    keep_going = False
#------------------------------------------------------------------------------
  def _geq(self, element1, element2):
    self.closure()
    return any(
      relation[0] == element1 and element2 in relation
      for relation in self.relations
    )
#------------------------------------------------------------------------------
  def geq(self, element1, element2):
    if self.cartesian == 0:
      return self._geq(element1, element2)

    return all(
      element2[i] or self._geq(element1[i], element2[i])
      for i in range(self.cartesian)
    )
#------------------------------------------------------------------------------
  def _inf(self, element1, element2):
    self.closure()
    found_relation1 = False
    found_relation2 = False
    # In a single pass,
    # find a relation whose first element is element1
    # and a relation whose first element is element2
    # assert not any(x == y and i != j for i, x in enumerate(self.relations) for j, y in enumerate(self.relations))
    for relation in self.relations:
      if relation[0] == element1:
        relation1 = relation
        found_relation1 = True
      if relation[0] == element2:
        relation2 = relation
        found_relation2 = True
      if found_relation1 and found_relation2:
        break
    else:
      return self.mask
    intersection = set(relation1) & set(relation2)
    if not intersection:
      return self.mask

    return reduce(lambda x, y: x if self.geq(x, y) else y, intersection)
#------------------------------------------------------------------------------
  def inf(self, element1, element2):
    if self.cartesian == 0:
      return self._inf(element1, element2)

    return [
      self._inf(element1[i], element2[i])
      for i in range(self.cartesian)
    ]
#------------------------------------------------------------------------------
  def __contains__(self, element) -> bool:
    ''' Does `element` belong to this pre-ordered set?
    '''
    return any(element == relation[0] for relation in self.relations)
#------------------------------------------------------------------------------
