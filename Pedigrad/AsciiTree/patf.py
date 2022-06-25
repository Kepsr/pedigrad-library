#------------------------------------------------------------------------------
#print_atf(atf,depth): standard output
#------------------------------------------------------------------------------
'''
This function  takes an atf and its depth and prints the ascii tree associated with the atf on the standard output.

e.g. 

l = [[0,1,0,0,0,0], [0,2,0,0,0,1], [0,4,2,3,3,5]]

tree = tree_of_partitions(l)
atpf = convert_tree_to_atpf(tree)
atf  = convert_atpf_to_atf(atpf[0],atpf[1])

The output of print_atf(atf,atpf[1]) is given below.

|                   |   
|________________   |   
|               |   |   
|________       |   |   
|   |   |       |   |   
A   C   D...E   F   B
'''

def print_atf(atf: list, depth: int):
  #If depth = 0 then the program terminates and the tree is printed 
  #on the standard output.
  if depth == 0:
    return

  for x in atf:
    print("|   ")
    for _ in range(x[0][0] - 1):
      print("    ")
  print("\n")
  for x in atf:
    #Prints branches for intermediate levels.
    if depth != 1:
      print("|")
    #Prints the label of the leaves.
    else:
      for k, ktem in enumerate(x[1]):
        if k > 0:
          print("...")
        print(chr(65 + ktem))
    for _ in range(x[0][1]):
      print("____")
    #Prints spaces between the branches of intermediate levels.
    if depth != 1:
      for _ in range(x[0][0] - x[0][1] - 1):
        print("    ")
    print("   ")
  print("\n")
  #Truncates the atf from below so that 
  #the next level of the atf is turned into a forest.
  next_atf = sum((x[1] for x in atf), [])
  #Recursion step: continues to the next line on the standard output.
  print_atf(next_atf, depth - 1)
