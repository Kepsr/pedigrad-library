'''

[Functions]
  read_until
        [Inputs: 4]
          - a_file            [Type] file
          - separators        [Type] list(string)
          - EOL_symbols       [Type] list(string)
          - inclusive = False [Type] bool
        [Outputs: 1]
          - words             [Type] list(string)
  fasta
        [Inputs: 1]
          - filename  [Type] string
        [Outputs: 2]
          - names     [Type] list(list(string))
          - sequences [Type] list(string)

[General description]
  This structure is equipped with a collection of functions that turned out to be very useful while coding the present library.

>>> Function: read_until
  [Description]
    This function reads a file until it reads a character belonging to the list [EOL_symbols]. It returns the list of words that were separated by a character in [separators]. If the argument [inclusive] is set to True, then the last character read is included in the output. Otherwise, it is always excluded.

>>> Function: fasta
  [Description]
    This function takes a fasta file and returns two outputs:
      - [names], containing the list of sequence labels specified in the file;
      - [sequences], containing the list of sequences.
  Furthermore, every sequence label is parsed such that every words separated by a colon is given as a distinct element within a list representing the sequence label.

'''

def read_until(file, separators, EOL_symbols, inclusive = False):
  tokens = []
  blanks = EOL_symbols + ['']
  char = file.read(1)
  while char not in blanks:
    while char in separators and char not in blanks:
      char = file.read(1)
    if char not in blanks:
      token = ''
      while char not in separators and char not in blanks:
        token += char
        char = file.read(1)
      tokens.append(token)
  if inclusive:
    tokens.append(char)
  return tokens

def fasta(filename):
  names = []
  sequences = []
  with open(filename, 'r') as file:
    read_until(file, [], ['>'])
    while True:
      name = read_until(file, [':'], ['\n','\r'])
      if not name:
        break
      names.append(name)
      sequences.append(''.join(read_until(file, ['\n', '\r'], ['>'])))

  return (names, sequences)
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

def nub(xs: list) -> list:
  ''' Take a list and return a new list lacking repeats
      but otherwise retaining the order of elements.
  '''
  return list(dict.fromkeys(xs))
