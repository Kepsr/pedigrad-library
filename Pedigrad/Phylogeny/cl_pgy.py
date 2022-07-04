from . import Phylogenesis
from Pedigrad.PartitionCategory import (
  Partition, MorphismOfPartitions, _epi_factorize_partition
)
from Pedigrad.utils import nub
from Pedigrad.AsciiTree import print_evolutionary_tree

class Phylogeny:
  '''

      The attribute `phylogeneses` is a list of `Phylogenesis` objects.
      The taxon of each phylogenesis should be its index in the list
      and any label appearing in the Phylogenesis items of the list should have its own Phylogenesis item in the list.

  '''

  history = list[list[int]]

  def __init__(self, histories: list[history]):
    ''' Given a list of histories (each a list of lists of indices),
        use every history to create a `Phylogenesis`,
        which is assigned to `phylogeneses`.
    '''
    #Allocates a space in the memory to store the list of phylogenesis items
    #passed to the procedure. The allocation happens after the format of the
    #has been checked to be valid.
    self.phylogeneses = []
    #The following lines
    for i, history in enumerate(histories):
      #A phylogenesis item is created by using the list of lists
      #(i.e. the history) contained in history[1].
      phy = Phylogenesis(history)
      #If the i-th phylogenesis contained phylogeneses is not that of taxon
      #i, then the phylogenesis is not valid and the procedure returns an
      #error message before exiting the program. If the taxon of the i-th
      #phylogensis is i, then the Phylogenesis item is added to the list
      #contained in the object .Phylogeneses.
      assert i == phy.taxon, "phylogeneses is invalid (no taxon should be missing and the taxa should be given in increasing order)"
      self.phylogeneses.append(phy)
    #The following loop checks whether all the taxa coalescing with
    #the taxon i are all included in the range of the set of taxa of the
    #Phylogeny.
    for item in self.phylogeneses:
      #Gets the maximal taxa for the i-th phylogenesis by looking at the
      #first generation.
      max_taxon = max(item.history[-1])
      #If the label of the maximal taxa contained the i-th phylogenesis is
      #greater than or equal to the number of taxa, then either the indexing
      #is not correct, or the collection of Phylogenesis items is missing an
      #item (as all taxa should have their own phylogenesis). In this case,
      #the procedure returns an error message and exits the program.
      assert max_taxon < len(self.phylogeneses), "The taxa are not compatible across the phylogeny"

  def coalescent(self) -> list:
    ''' Return the list of the first generations (i.e the last lists) of the objects .history
        of each of the Phylogenesis item contained in the object .phylogeneses.
        The k-th list of the output is the first generation of the history of taxon k.
    '''
    # The coalescent: the first generations of each of the Phylogenesis
    # items contained in self.phylogeneses.
    # Return a list of the first generation of each phylogenesis of self.phylogeneses.
    return [phylogenesis.history[-1] for phylogenesis in self.phylogeneses]

  #The variable 'extension' is supposed to contain pairs (t,l) where t
  #is a taxon of the phylogeny and l is the extension of the phylogenesis of t.
  #The role of the method .extend is to append the list l to the Phylogenesis
  #item associated with t.
  def extend(self, extension: list):
    ''' Given a list of pairs of the form (t,l)
        where t is the label of a taxon and l is a list of taxa,
        update the object .phylogeneses as follows:
        --> for all pairs (t,l) contained in the input passed to .extend:
        1) if every list l contains the last list of phylogenesis.history and if at least one of the lists l strictly contains the last list of
        phylogenesis.history, then every list l is appended to the list phylogenesis.history and the value True is returned;
          2) if there is no strict inclusion of the last list of phylogenesis.history into l, then the object .phylogeneses is not modified and the value False is returned;
          3) otherwise, an error message is returned and the procedure exit the program;
        --> in any terminating case, for all other taxa t of the phylogeny that do not appear in the input of .extend, the last list of phylogenesis.history (i.e. the first generation of the history of the phylogenesis of t) is again repeated (i.e. appended again) in the list phylogenesis.history.    
    '''
    #The variable indicates whether if the extension of the phylogeny
    #is 'complete', in the sense that all the lists l in 'extension' have
    #already been added in previous generations, which, in fact,
    #should also be the first ones.
    flag = False
    #The following loop checks all the lists l of 'extension' are already
    #appreaing in the first generations.
    for t, phylogenesis in enumerate(self.phylogeneses):
      for x in extension:
        #Checks if the list 'extension' requires to add a new generation
        #to the taxa t. Then the next 'if' tests whether the generation
        #is actually a new generation, adding new taxa to the phylogeny.
        if x[0] == t:
          #The extension will provide a valid phylogeny if all the lists l
          #contains the first generation associated with the history of the
          #taxon t with which they are coupled. The following lines check
          #that this is the case.
          for j in phylogenesis.history[-1]:
            assert j in x[1], f"The extension is not compatible with the phylogenesis of taxon {t}"
          #The following lines check whether the extension is actually adding
          #a new individual to the history of the taxon t. If this is not
          #the case for all the taxa of the extension, then the phylogeny
          #is considered to be already complete, so that the variable flag
          #is never changed to the value True.
          for j in x[1]:
            #The following lines check if new individuals appear in
            #x[1] in addition of those already in
            #phylogenesis.history.
            if j not in phylogenesis.history[-1]:
              #A new generation has been detected, the phylogeny is therefore
              #not complete and 'flag' is set to True.
              flag = True
    #The following condition holds whenever there is at least one phylogenesis
    #that is not complete.
    if not flag:
      # The phylogeny is now complete.
      return False

    #The following lines add the new generation l of a pair
    #(t,l) in 'extension' to the taxa t. Otherwise, the first
    #generation of a taxa that do not appear in 'extension'
    #is repeated in its phylogenesis.
    for t, phylogenesis in enumerate(self.phylogeneses):
      # Does the taxon t appear in the first components of the pairs of the list 'extension'?
      for _ in extension:
        if x[0] == t:
          #The procedure nub is used to eliminate the
          #repetitions of integers that can occur in x[1].
          phylogenesis.history.append(nub(x[1]))
          break
      else:
        continue
      # If the taxon was not associated with any list l in 'extension',
      # the first generation is repeated
      # (there is no repetition of integer in this list).
      phylogenesis.history.append(phylogenesis.history[-1])
    # The phylogeny was not completed,
    # and another run is necessary to complete the phylogeny.
    return True

  def make_friends(self, taxon: int):
    ''' Given the index of a taxon, return a pair of lists (friends, hypothesis).
        The list 'friends' contains all those taxa that have not coalesced with the input taxon,
        which means that there are not in the first generation of phylogenesis of the taxon.
        while the list 'hypothesis' contains the lists obtained by making the union of the first generation of the input taxon with the first generation of one of the taxon in 'friends'.
    '''
    #The friendships are essentially formed at the level of the oldest
    #generation. Friendships will consist of unions of pairs of lists contained
    #in the output of self.coalescent().
    coalescent = self.coalescent()
    x = coalescent[taxon]
    #Allocates two spaces in the memory to store the output of the function:
    #- 'friends' will contain indices (i.e. the taxa that can be
    #  related to the input taxon).
    #- 'coalescence_hypothesis' that  contains the unions of the oldest
    #  generation of 'taxon' with the oldest generation associated with an
    #  individual in 'firends'.
    friends = []
    coalescence_hypothesis = []
    #The following loop fills in the lists 'friends'
    #and 'coalescence_hypothesis'. The list 'friends' contains all those
    #of the phylogeny that are not in x. The list
    #'coalescence_hypothesis' contains the union of x and
    #y for every index r in the list 'friends'.
    for r, y in enumerate(coalescent):
      if r not in x:
        friends.append(r)
        #The union of x and y is computed through
        #nub and then sorted in order to give a unique
        #representative to the union (e.g. [0,1]U[2,5] should be the same
        #as [2,5]U[0,1].
        common_ancestor = sorted(nub(x + y))
        coalescence_hypothesis.append(common_ancestor)
    #the procedure returns the list of friends for the input taxon and the
    #associated common ancestors stored in the list 'coalescence_hypothesis'.
    return (friends, coalescence_hypothesis)

  def set_up_friendships(self):
    ''' Return a pair of lists (friendships, hypotheses) containing the lists of the two different outputs of the method .make_friends for every taxon of the phylogeny. More specifically,
        - 'friendships' is the list of lists whose i-th list contains the first output of the procedure self.make_friends for taxon i;
        - 'hypotheses'  is the list of lists whose i-th list contains the second output of the procedure self.make_friends for taxon i;

    '''
    #Allocates two spaces in the memory to store the two types of output
    #given by the procedure self.make_friends for every taxon
    #of self.phylogeneses. Specifically,
    #- 'friendships' is a list of lists whose t-th list contains the first
    #  output of the procedure self.make_friends for taxon t;
    #- 'coalescence_hypotheses'  is a list of lists whose t-th list contains
    #  the second output of the procedure self.make_friends for taxon t.
    friendships = []
    coalescence_hypotheses = []
    #For every taxon t, the two outputs of the procedure self.make_friends(t)
    #are appended to the lists 'friendships' and 'coalescence_hypotheses'.
    for t in range(len(self.phylogeneses)):
      network = self.make_friends(t)
      friendships.append(network[0])
      coalescence_hypotheses.append(network[1])
    #The two lists are returned.
    return (friendships,coalescence_hypotheses)

  def score(self, partitions, friendship_network):
    ''' Given a list of lists of non-negative integers (i.e. partitions) and a pair of lists, say (friendships,hypotheses), where
          - friendships is a list of lists;
          - hypotheses is a list of lenght len(friendships) whose t-th element is a
            list of length len(friendships[t]) whose elements are lists of integers
            ranging from 0 to len(self.phylogeneses)-1 (preferrably sorted from
            smallest to greatest);
        return a list of length len(friendships) whose t-th element is a list of triples of the form (r,large,exact) where
          - r runs over the elements of friendships[t],
          - 'large' is the large score [4] of the hypothetical ancestor
            hypotheses[t][r] within the set of ancestors contained in
            hypotheses[t] for the list of partitions given in the input,
          - 'exact' is the exact score [4] of the hypothetical ancestor
            hypotheses[t][r] within the set of ancestors contained in
            hypotheses[t] for the list of partitions given in the input.

        This means that 'large' is the number of partitions belonging to the first input list for which there is a morphism of partition x.indices() -> partition
        where we take

        x = Partition([hypotheses[t][r]],len(self.phylogeneses)-1)

        and 'exact' is the number of partitions that were counted in the large score of r such that if these partitions belong to the large score of any other element s in friendships[t], then either the equality hypotheses[t][r] = hypotheses[t][s] holds or the intersection of hypotheses[t][r] with hypotheses[t][s] is empty.
        The second input of the method .score can, for instance, be taken to be the output of the procedure self.set_up_friendships().
    '''

    def homset(partition1: list, partition2: list):
      '''
      Does there exist a morphism of partitions between these two lists
      (seen as partitions)?
      '''
      try:
        MorphismOfPartitions(partition1, partition2)
        return True
      except:
        return False

    def equal_or_disjoint(list1: list, list2: list):
      ''' Are these two lists equal or disjoint?
      '''
      set1 = set(list1)
      set2 = set(list2)
      return set1 == set2 or not bool(set1 | set2)

    #STEP 1:
    #The variable 'score_matrix' will encode a tensor of dimension 3,
    #which means a list of lists of lists. Its coefficients, of the from
    #score_matrix[i][t][r] are defined for
    #- an index i indexing a partition in the list 'partitions'
    #- an index t indexing a list in friendship_network
    #- an index r indexing a taxon in friendship_network[0][t]
    #and they each contain a pair (flag,label) where
    # - 'label' is an integer representing the list stored in
    #friendship_network[1][t][r] (i.e. a hypothetical ancestor) labeled with
    #respect to all the other lists of friendship_network[1][t] up to
    #list equality, which means that if the list friendship_network[1][t][r]
    #is equal to the list friendship_network[1][s][r], then
    #score_matrix[i][t][r] and score_matrix[i][t][s] receive the same label.
    #- 'flag' is a Boolean value indicating whether the partitions indexed
    #by i in 'partitions' satisfies the exactness condition for the
    #hypothetical ancestor friendship_network[1][s][r].
    score_matrix = []
    #For convenience, the list of lists of lists friendship_network[1] is
    #renamed as 'hypotheses'.
    hypotheses = friendship_network[1]
    #The following loop gives labels to the different lists (i.e. the
    #hypothetical ancestors) in hypotheses in order to recognize them up
    #to list equality.
    labeling = [_epi_factorize_partition(hypothesis) for hypothesis in hypotheses]
    #The following loop fills the coefficients of 'score_matrix' in.
    for partition in partitions:
      #The variable score_row will contain the rows of the matrix.
      score_row = []
      #The following loop runs over the set of indices representing
      #each taxon 't' of the phylogeny.
      for t, hypothesis in enumerate(hypotheses):
        #The variable 'score_coalescence' will be used to compute
        #the component 'flag' of score_matrix[i][t][r]' while
        #the variable 'score_labeling' will be used to compute
        #the component 'label' of score_matrix[i][t][r]'
        score_coalescence = []
        score_labeling = []
        #The following loop runs over the set of indices representing the
        #taxa 'r' of the phylogeny that may possibly coalesce with 't'.
        for r, x in enumerate(hypothesis):
          #The variable 'x' contains the obvious partition of the set of taxa
          #whose only non-trivial part is the list of indices
          #representing the hypothetical ancestor 'x'.
          x = Partition([x], len(self.phylogeneses) - 1)
          #The following lines check whether there is a morphism of partitions
          #form 'x' to the partition partition. This condition will
          #later be referred to as the 'large score condition'.
          #i.e. x --> P(partition)
          if homset(x.indices(), partition):
            #If the condition is satisfied, then the hypothetical ancestor
            #x is stored in 'score_coalescence[r]' and
            #its label is stored in 'score_labeling[r]'.
            score_coalescence.append(x)
            score_labeling.append(labeling[t][r])
        #The following lines now construct the coefficients of the list
        #score_matrix[i][t]
        score_coeff = []
        #By construction, the following loop runs over the set of indices
        #representing the taxa 'r' of the phylogeny that satisfy the
        #'large score condition' (see above). The goal is now to determine
        #which of these taxa also satisfy the 'exact score condition'.
        for r, partition1 in enumerate(score_coalescence):
          #The variable 'flag' is the Boolean condition meant to be
          #stored in the pair score_matrix[i][t][r] and is meant to
          #indicate whether the 'exact score condition' is satisfied.
          flag = True
          #The following lines check whether 'r' satisfies the 'exact
          #score condition', which must be checked with respect to all
          #the other taxa 's' satisfying the 'large score condition'.
          for s, partition2 in enumerate(score_coalescence):
            if r != s:
              flag = flag and equal_or_disjoint(partition1, partition2)
          #As described above, the coefficient score_matrix[i][t][r]
          #is constructed as a pair (flag,label).
          score_coeff.append((flag, score_labeling[r]))
        #The list score_coeff corresponds to what is called the 'support
        #functor' in the mathematical version of the present work.
        #Also, since the images of the support functor are sets, we need to
        #consider the output of the procedure nub(score_coeff)
        #instead of the list score_coeff itself since it may contain several
        #times the same list.
        #Use if needed:
        #print("[DEBUG] Support functor("+str((t,i))+"): " \
        #+ str(nub(score_coeff)))
        score_row.append(nub(score_coeff))
      score_matrix.append(score_row)
    #STEP 2:
    #The following lines integrate the tensor score_matrix[i][t][r] over
    #the indices i, namely the indices indexing the partitions
    #of 'partitions'. More specifically, the following lines count the number
    #of segments making the large and exact scores for a given ancestor
    #represented by a certain label 'l'.
    #Below, the variable 'score_cardinality' is meant to contain a matrix
    #that contains the large and exact score.
    # Initialize the matrix 'score_cardinality' with null scores.
    # The first and second integer are the initial values for the large
    # and exact scores, respectively.
    # Run over the image of x,
    # which means that only the representative of the hypothetical
    # ancestors is important and not the taxa 'r' they may be associated with.
    score_cardinality = [[[0, 0] for _ in nub(x)] for x in labeling]
    #The matrix 'score_cardinality' is now updated by counting the flags that
    #were set to False and True in the 3-dimensional tensor 'score_matrix'.
    for row in score_matrix:
      for t, x in enumerate(row):
        for f, l in x:
            if f:
              score_cardinality[t][l][1] += 1
            score_cardinality[t][l][0] += 1
    #STEP 3:
    #The following lines are a copy of STEP 2 but where one produces a matrix
    #indexed by the 'friends' of the given taxon t instead of producing a
    #matrix indexed by the labels of the representative of the common
    #ancestors. Note that STEP 2 was essential for the count of the large and
    #exact scores, which are meant to be computed  with respect to the
    #hypothetical ancestors and not the 'friends' of taxon t.
    friendships = friendship_network[0]
    score_cardinality_adjusted = [[() for _ in x] for x in labeling]
    #This time, the following line is not computed with respect to the
    #image of row.
    for t, row in enumerate(labeling):
      for r, i in enumerate(row):
        y = score_cardinality[t][i]
        score_cardinality_adjusted[t][r] = (friendships[t][r], y[0], y[1])
    #The procedure returns a triple (r,large,exact) where r runs over the
    #elements of friendships[t] where 'large' is the large score of the
    #possible ancestor hypotheses[t][r] and where 'exact' is the exact score
    #of the possible ancestor hypotheses[t][r].
    return score_cardinality_adjusted

  def choose(self, scores):
    ''' Given a list of lists of triples (r,l,e)
        where l and e are non-negative integers,
        return a list of lists whose i-th list is the list of element r of the i-th internal list of the input list
        for which the associated pairs (l,e) are equal to the greatest local maxima of the function (e,l) -> (l,e)
        ordered by the lexicographical order and relative to the pairs of the i-th internal list of the input list.
    '''

    def lex_order(pair1: tuple, pair2: tuple):
      ''' A non-strict lexicographical order on pairs of integers.
      '''
      x1, y1 = pair1
      x2, y2 = pair2
      return x1 < x2 or x1 == x2 and y1 <= y2

    def lex_strict_order(pair1: tuple, pair2: tuple):
      ''' A strict lexicographical order on pairs of integers.
      '''
      x1, y1 = pair1
      x2, y2 = pair2
      return x1 < x2 or x1 == x2 and y1 < y2

    #A space is allocated to store the output of the procedure.
    result = []
    #In the following loop, each internal list of the input list 'score' is
    #sorted with respect to the (opposite) lexicographical order of the last
    #and second last components of its elements.
    #More specifically, every internal list score[t] contains pairs (r,l,e)
    #and these pairs are sorted with respect to the reverse lexicographical
    #order with respect to the part (e,l). Once the list is sorted, the
    #greatest local maximum of the function (e,l) -> (l,e) is found and all
    #the elements r associated with this local maximum (l,e) are stored
    #in a list called 'choose', which is appended to the list 'result'.
    for score in scores:
      #Sorting 'score[t]' as follows ensures that the first local maximum
      #of the function (e,l) -> (l,e) is actually the greatest one.
      score.sort(key = lambda indiv_scores: (-indiv_scores[2], -indiv_scores[1]))
      #Since the pair (e,l) are supposed to contain non-negative integers,
      #we look for the greatest local maximum by starting with the value (0,0).
      loc_max = (0,0)
      #The following loop compute the greatest local maximum of the function
      #(e,l) -> (l,e) for all the pairs (r,e,l) in score[t].
      for r in range(len(score)):
        if not lex_order(loc_max, score[r][1:3]):
          break
        loc_max = score[r][1:3]
      #A space is allocated to store the elements 'r' of the pairs (r,l,e) for
      #which the pair (l,e) is the greatest local maximum of the map
      #(e,l) -> (l,e) relative to the pairs (l,e) coming from score[t].
      choose = []
      #The following loop look for the values 'r' associated with the greatest
      #local maximum (l,e).
      for x in score:
        if lex_strict_order(x[1:3], loc_max):
          continue
        if loc_max != x[1:3]:
          break
        choose.append(x[0])
      #The list of elements 'r' that are associated with the greatest local
      #maximum (l,e) is appended to the list 'result'
      result.append(choose)
    #The list of lists of elements 'r' reaching the greatest local maxima is
    #returned.
    return result

  def set_up_competition(self, best_fit: list[list[int]]):
    ''' Given a list of lists of integers
        whose length must be equal to the length of self.phylogeneses (i.e. the number of taxa of the phylogeny),
        return a list of lists of integers whose length is also equal to the length of self.phylogeneses
        and whose t-th internal list is the union of the t-th list of self.coalescent()
        with the r-th lists of self.coalescent() for every element r in the t-th internal list of the input list.
    '''
    #The competition takes place in the oldest generation.
    #competitors will consist of unions of pairs of lists contained
    #in the output of self.coalescent().
    coalescent = self.coalescent()
    #A space is allocated in the memory to store the different competitors.
    coalescence_hypothesis = []
    #The following loop makes the union of the first generation associated
    #with taxon t with the first generations associated with the taxa r in
    #best_fit[t].
    for x, y in zip(coalescent, best_fit):
        #The following ensures that if y is empty, then the first
        #generation of the phylogenesis of t is given.
        # Add the first generations of the friend of the
        # taxon t to the 'common ancestors.
        common_ancestor = set.intersection(set(x), *(set(coalescent[r]) for r in y))
        #The list 'common_ancestor' to only give one representative to the
        #union it represents.
        coalescence_hypothesis.append(sorted(common_ancestor))
    #The list of competitors is returned, where each competitor is indexed
    #by the integer of the taxon it is supposed to represent.
    return coalescence_hypothesis

  def count_uniformity():
    raise NotImplementedError()

  def boolean_partition():
    raise NotImplementedError()

  def choose_friends():
    raise NotImplementedError()

  def score_dominance():
    raise NotImplementedError()

  def choose_dominants():
    raise NotImplementedError()
