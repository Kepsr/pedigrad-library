#------------------------------------------------------------------------------
#convert_atpf_to_atf(atpf,depth): ascii tree format
#------------------------------------------------------------------------------
'''
This function takes an atpf and its depth and returns the associated ascii tree format (abbrev. atf; see the documentation and below for more details).

An atf is a modified version of an atpf in which one substracts all the weights by the rightmost weight of the next level. The reason for this is that the procedure print_atf is to display ascii trees whose trunks are on the left of the screen, as show below.

|
|_____
|     |
|     |
|     |
|__   |__
|  |  |  |
|  |  |  |
1  2  3  4


Substracting the rightmost weights of the atpf from the weight placed below it in the tree allows print_atf (see pa.py) to know when it needs to stop printing the horizontal level of the tree, as shown below with the extra underscores symbols sticking out toward the right.

|
|_________     atpf_weight = 4   atf_weight = 4 - 1 = 3
|     |
|     |
|     |
|__   |__
|  |  |  |
|  |  |  |
1  2  3  4

'''

def convert_atpf_to_atf(atpf: list, depth: int) -> list:
  # Takes care of the non-leaf levels. The procedure starts by the root
  # and uses a recursion to repeat the same actions on the other levels.
  if depth == 1:
    return [((x, 0), y) for x, y in atpf]

  for i, (x, y) in enumerate(atpf):
    # The goal of this procedure is to prepare the atpf for displaying an
    # ascii tree whose trunk is on the left of the screen. For a nice display
    # the rightmost weight of the atpf needs to subtracted from the weight 
    # placed below it in the tree.
    atf_weight = x - y[-1][0]
    atpf[i] = ((x, atf_weight), y)
  # A space is allocated in the memory to store the data of the output atf.
  # This loops takes care of preserving the bracketing structure of 
  # the atpf/atf through the recursion step toward the next levels.
  return [(x, convert_atpf_to_atf(y, depth - 1)) for x in atpf]
