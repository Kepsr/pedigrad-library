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
          - name_of_file  [Type] char
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
  .presence
        [Inputs: 1]
          - element   [Type] 'a
        [Outputs: 1]
          - presence  [Type] bool

[General description]
  This class models the features of a pre-ordered set. The pre-order relations are specified through either a file [name_of_file] or another PreOrder item passed to the constructor [__init__]. The method [closure] computes the transitive closure of the pre-order relations stored in the object [relations]; the method [geq] returns a Boolean value specifying whether there is a pre-order relation between two given elements of the pre-ordered set; the method [inf] returns the infimum of two elements of the pre-ordered set; and the method [presence] returns a Boolean value specifying whether an element belongs to the pre-ordered set.

>>> Method: .__init__
  [Actions]
    .relations  <- use(name_of_file,*args)
    .transitive <- use(*args)
    .mask       <- use(name_of_file,*args)
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

>>> Method: .presence
  [Actions]
    presence <- use(self.relations)
  [Description]
    Specifies whether [element] belongs to the pre-ordered set.
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
#Dependencies: current, Useful
#------------------------------------------------------------------------------
from Pedigrad.Useful.usf import usf, add_to
from functools import reduce
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class PreOrder:
#------------------------------------------------------------------------------
  def __init__(self, name_of_file, cartesian = 0, *args):
    if cartesian > 0 and len(args) == 1:
      self.relations = args[0].relations
      self.transitive = args[0].transitive
      self.mask = args[0].mask
      self.cartesian = cartesian
    else:
      if not name_of_file:
        print("Error in PreOrder.__init__: name of file is empty")
        exit()

      self.relations = []
      self.transitive = False
      self.mask = False
      self.cartesian = cartesian

      with open(name_of_file, "r") as the_file:

        #Search the key words '!obj:' or 'obj:'
        list_of_objects = []
        flag_obj = False
        while not flag_obj:
          heading = usf.read_until(the_file, heading_separators, [':'])
          if not heading:
            print("Error in PreOrder.__init__: in \'"+\
            name_of_file+"\': \'obj:\' was not found")
            exit()
          if heading[-1] == "!obj":
            self.mask = True
            flag_obj = True
          elif heading[-1] == "obj":
            flag_obj = True

        #Search the key word 'rel:'
        flag_rel = False
        while not flag_rel:
          line = usf.read_until(the_file, separators, ['#',':'], inclusive=True)
          objects = []
          if line == ['']:
            break
          if len(line) > 1 and line[-2:] == ["rel", ":"]:
            objects = line[:-2]
            flag_rel = True
          else:
            objects = line[:-1]
            usf.read_until(the_file, separators, ['\n'])

          #Construct [list_of_objects] and [self.relations]
          for obj in objects:
              add_to(obj, list_of_objects)
              add_to([obj], self.relations)

        #If the key word 'rel:' is not found
        if flag_rel == False:
          return

        #If the key word 'rel:' was found, search the symbols '>' and ';'
        flag_EOF = False
        while not flag_EOF:

          all_successors = []
          flag_succ = False
          while not flag_succ:
            line = usf.read_until(the_file, separators, ['#', '>'], inclusive=True)
            successors = []
            if line == ['']:
              break
            if line[-1] == ">":
              successors = line[:-1]
              flag_succ = True
            else:
              successors = line[:-1]
              usf.read_until(the_file, separators, ['\n'])

          #Construct [all_successors]
          for successor in successors:
              add_to(successor, all_successors)

          #Complete [self.relations] with [predecessors] for each successor
          predecessors = usf.read_until(the_file, separators, [';'])
          if not all_successors or not predecessors:
            flag_EOF = True
          for successor in all_successors:
            try:
              index = list_of_objects.index(successor)
              for predecessor in predecessors:
                add_to(predecessor, self.relations[index])
            except:
              print("Warning in PreOrder.__init__: in \'"+\
              name_of_file+"\': "+ successor+" is not an object")
#------------------------------------------------------------------------------
  def closure(self):
    if not self.transitive:
      self.transitive = True
      for i, item in enumerate(self.relations):
        keep_going = True
        while keep_going:
          keep_going = False
          for elt in item:
            for j, jtem in enumerate(self.relations):
              if i != j and elt == jtem[0]:
                for new_elt in jtem:
                  keep_going = new_elt not in item
                  add_to(new_elt, item)
#------------------------------------------------------------------------------
  def _geq(self, element1, element2):
    self.closure()
    for relation in self.relations:
      if relation[0] == element1:
        return True and (element2 in relation)
    return False and (element2 in self.relations[0])
#------------------------------------------------------------------------------
  def geq(self,element1, element2):
    if self.cartesian == 0:
      return self._geq(element1, element2)

    for i in range(self.cartesian):
      if not element2[i] and not self._geq(element1[i], element2[i]):
        return False
    return True
#------------------------------------------------------------------------------
  def _inf(self,element1,element2):
    self.closure()
    relation1 = self.relations[0]
    relation2 = self.relations[0]
    found_relation1 = False
    found_relation2 = False
    # In a single pass, 
    # find the first instance of element1
    # and the first instance of element2
    for relation in self.relations:
      if relation[0] == element1:
        found_relation1 = True
        relation1 = relation
      if relation[0] == element2:
        found_relation2 = True
        relation2 = relation
      if found_relation1 and found_relation2:
        break
    else:
      return self.mask
    intersect = set(relation1) & set(relation2)
    if not intersect:
      return self.mask

    return reduce(lambda x, y: x if self.geq(x, y) else y, intersect)
#------------------------------------------------------------------------------
  def inf(self, element1, element2):
    if self.cartesian == 0:
      return self._inf(element1, element2)

    return [
      self._inf(element1[i], element2[i])
      for i in range(self.cartesian)
    ]
#------------------------------------------------------------------------------
  def presence(self, element):
    return any(element == relation[0] for relation in self.relations)
#------------------------------------------------------------------------------
