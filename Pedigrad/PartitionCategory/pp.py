#------------------------------------------------------------------------------
#print_partition(partition): standard output
#------------------------------------------------------------------------------
from .piop import _preimage_of_partition

def print_partition(partition: list):
  ''' Print the preimage of a list.
  '''
  print(_preimage_of_partition(partition))
