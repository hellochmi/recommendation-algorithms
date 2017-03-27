# tanimoto.py
# code to compute tanimoto coefficient
# -----------------------------------------------------------------

# the tanimoto coefficient is a measure of the similarity
# of two sets based on a list of properties

# consider three sets: set A, set B, and set C, where set A and
# set B intersect. the cardinality of each set is represented by
# a, b, and c, respectively

# the tanimoto coefficient is computed by taking
# c / (a+b-c)

# a tanimoto score of 1 suggests that the sets are identical
# a tanimoto score of 0 suggests that the sets are disjoint

# the function below takes two lists as parameters
# computes the cardinality, c, of the intersection, set C
# and then calculates the tanimoto coefficient

def tanimoto(a,b):
    # c is defined as the list of elements
    # returned if the element is in both a and b
    c=[v for v in a if v in b]
    return float(len(c))/(len(a)+len(b)-len(c))

