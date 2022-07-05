
def read_until(file, separators: list[str], EOL_symbols: list[str]):
  ''' Read a file until a character in `EOL_symbols`.
      Returns a list of tokens separated by any character in `separators`.
      The last character read is included in the output.
  '''
  tokens = []
  char = file.read(1)
  while char and char not in EOL_symbols:
    # Skip past non-blank separators
    while char and char in separators and char not in EOL_symbols:
      char = file.read(1)
    if char and char not in EOL_symbols:
      assert char not in separators
      token = ''
      while char and char not in separators and char not in EOL_symbols:
        token += char
        char = file.read(1)
      tokens.append(token)
  tokens.append(char)  # Include the last character read (an EOL symbol or '')
  return tokens


def fasta(filename: str):
  ''' Read a FASTA file and return a list of sequence blocks.
  '''
  names_and_sequences = []
  with open(filename, 'r') as file:
    read_until(file, [], ['>'])
    while (name := ''.join(read_until(file, [], ['\n','\r'])[:-1])):
      names_and_sequences.append((name, ''.join(read_until(file, ['\n', '\r'], ['>'])[:-1])))
  return names_and_sequences


def nub(xs: list) -> list:
  ''' Take a list and return a new list lacking repeats
      but otherwise retaining the order of elements.
  '''
  return list(dict.fromkeys(xs))
