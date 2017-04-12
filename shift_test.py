import numpy as np

##JUST USED TO TEST THE SHIFTING ALGORITHM DO NOT USE IN ACTUAL CODE
## TEST WAS SUCCESSFUL

def compare_parsey_vectors(vector1, vector2):
    ##Takes in parseyed vectors1 and 2
    ##Vectors in the form ((sentence tuple), (word1, POS, senTag), (word2, POS, senTag), ...)
    ##tree_vector = key from dic, tree_vector2 = input vector
    tree_vector = vector1
    tree_vector2 = vector2
    
    scores = []

    shifts = max(len(tree_vector), len(tree_vector2)) - \
             min(len(tree_vector), len(tree_vector2))

    
    #Only compare words up to the length of the shortest sentence
    #Then shift to the right up to the distance between vectors
    
    for x in range(0, shifts+1):
        numpy_vector = []
        for i in range(0, min(len(tree_vector), len(tree_vector2))):
            for j in range(0, 3):
                if len(tree_vector) > len(tree_vector2):
                    print(tree_vector[i+x])
                    if tree_vector[i+x][j] == tree_vector2[i][j]:
                        numpy_vector.append(1)
                    else:
                        numpy_vector.append(0)
                else:
                    print(tree_vector2[i+x])
                    if tree_vector[i][j] == tree_vector2[i+x][j]:
                        numpy_vector.append(1)
                    else:
                        numpy_vector.append(0)
        if len(tree_vector2) > len(tree_vector):
            weight = len(tree_vector2) - len(tree_vector) + 1
        else:
            weight = len(tree_vector)- len(tree_vector2) + 1
        numpy_vector.append(1/weight)
        numpy_vector = np.array(numpy_vector)
        print(numpy_vector)
        scores.append(np.linalg.norm(numpy_vector))
    return max(scores)

vector1 = [["hello", "UH", "d"]]
vector2 = [["hello", "UH", "d"], ["man", "AB", "c"], ["what", "is", "up"]]
compare_parsey_vectors(vector1, vector2)
