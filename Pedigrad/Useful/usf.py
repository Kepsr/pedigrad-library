#------------------------------------------------------------------------------
#usf (Class item) | 0 objects | 5 functions
#------------------------------------------------------------------------------
'''

[Functions]
  usf.read_until
        [Inputs: 4]
          - a_file            [Type] file
          - separators        [Type] list(string)
          - EOL_symbols       [Type] list(string)
          - inclusive = False [Type] bool
        [Outputs: 1]
          - words             [Type] list(string)
  usf.fasta
        [Inputs: 1]
          - name_of_file  [Type] string
        [Outputs: 2]
          - names     [Type] list(list(string))
          - sequences [Type] list(string)
  usf.add_to
        [Inputs: 1]
          - element   [Type] 'a
          - a_list    [Type] list('a)

[General description]
  This structure is equipped with a collection of functions that turned out to be very useful while coding the present library.

>>> Function: usf.read_until
  [Description]
    This function reads a file until it reads a character belonging to the list [EOL_symbols]. It returns the list of words that were separated by a character in [separators]. If the argument [inclusive] is set to True, then the last character read is included in the output. Otherwise, it is always excluded.

>>> Function: usf.fasta
  [Description]
    This function takes a fasta file and returns two outputs:
      - [names], containing the list of sequence labels specified in the file;
      - [sequences], containing the list of sequences.
  Furthermore, every sequence label is parsed such that every words separated by a colon is given as a distinct element within a list representing the sequence label.

>>> Function: usf.add_to
  [Description]
    This function appends an element to a list if this element is not present in the list. Otherwise, the element is not appended.

'''
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class _Useful:
#------------------------------------------------------------------------------
  @staticmethod
  def read_until(a_file, separators, EOL_symbols, inclusive = False):
    words = []
    read = a_file.read(1)
    while read not in EOL_symbols + ['']:
      while read in separators and read not in EOL_symbols + ['']:
        read = a_file.read(1)
      if read not in EOL_symbols + ['']:
        word = ''
        while read not in separators and read not in EOL_symbols + ['']:
          word += read
          read = a_file.read(1)
        words.append(word)
    if inclusive:
      words.append(read)
    return words
#------------------------------------------------------------------------------
  @staticmethod
  def fasta(name_of_file):
    names = []
    sequences = []
    with open(name_of_file, "r") as the_file:
      flag_EOF = False
      usf.read_until(the_file, [], ['>'])
      while not flag_EOF:
        name = usf.read_until(the_file, [':'], ['\n','\r'])
        if name:
          names.append(name)
          sequences.append(''.join(usf.read_until(the_file, ['\n', '\r'], ['>'])))
        else:
          flag_EOF = True
    return (names, sequences)
#------------------------------------------------------------------------------
  @staticmethod
  def add_to(element, a_list: list):
      if element not in a_list:
        a_list.append(element)
#------------------------------------------------------------------------------
#  def trim(self,string,character,option = "suffix"):
#    def rev(i,option):
#      if option == "suffix":
#        return len(string)-1-i
#      else:
#        return i
#    for i in range(len(string)):
#      if string[rev(i,option)] == character:
#        return (string[:rev(i,option)],string[rev(i,option)+1:])
#------------------------------------------------------------------------------
#  def cut_at(self,a_list,an_index):
#    return a_list[0:an_index]+a_list[an_index+1:len(a_list)]
#------------------------------------------------------------------------------
usf = _Useful()
#------------------------------------------------------------------------------
