#------------------------------------------------------------------------------
#Tree (Class) | 4 objects | 4 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .depth  [Type] int
  .level  [Type] int
  .parent [Type] 'a
  .children [Type] list(Tree('a))

[Methods]
  .__init__
        [Inputs: +1]
          - parent  [Type] 'a
          - args    [Type] list(Tree('a))
        [Outputs: 0]
  .stdout
        [Inputs: 0]
        [Outputs: 0]
  .levelup
        [Inputs: 0]
        [Outputs: 0]
  .paths
        [Inputs: 0]
        [Outputs: 1]
          - l [Type] list('a)

[General description]
  This structure models the features of a tree structure. A Tree item is equipped with an object [parent] in which it is possible to store information and an object [children] through which one can specify descendants. A Tree item can be constructed recursively from the constructor. Tree items whose object [parent] is equal to the string "leaf"  are distinguished from the rest of the structure and considered as terminal states. For instance, these terminal states are useful if one wants to enumerate all the paths in the tree. For instance, the class [Tree] is equipped with a method [paths] that returns a list of all the paths going from the root to a leaf.

>>> Method: .__init__
  [Actions]
    .depth  <- use(args[0])
    .level  <- use()
    .parent <- use(parent)
    .children <- use(args[0])
  [Description]
    This is the constructor of the class.

>>> Method: .stdout
  [Description]
    This method displays the tree structure on the standard output.

>>> Method: .levelup
  [Actions]
    .level  <- use()
    .children <- use()
  [Description]
    This method increments all the objects [level] by 1 in the recursive structure of the [Tree] item.


>>> Method: .paths
  [Description]
    This method returns a list of all the paths going from the root to a leaf.

'''
#------------------------------------------------------------------------------
#Dependencies: sys
#------------------------------------------------------------------------------
import sys
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class Tree:
#------------------------------------------------------------------------------
  def __init__(self, parent: str or list, children: list = []):
    self.depth = 0
    self.level = 0
    self.parent = parent
    if self.parent != "leaf":
      self.children = children
      for child in self.children:
        child.levelup()
      self.depth = 1 + max(child.depth for child in self.children)
#------------------------------------------------------------------------------
  def stdout(self):
    if self.parent != 'leaf':
      sys.stdout.write("." * self.level)
      sys.stdout.write(f"[{self.level}] -> {self.parent}\n")
      for child in self.children:
        child.stdout()
#------------------------------------------------------------------------------
  def levelup(self):
    self.level += 1
    if self.parent != 'leaf':
      for child in self.children:
        child.levelup()
#------------------------------------------------------------------------------
  def paths(self):
    if self.parent == 'leaf':
      return [[]]

    return sum((
      [[self.parent, *path] for path in child.paths()]
      for child in self.children
    ), [])
#------------------------------------------------------------------------------
