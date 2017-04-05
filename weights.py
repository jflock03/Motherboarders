import pickle

class weights(object):
    def __init__(self):
        self.POS_tags = []
        self.label_tags = []

    def get_weight(self, LorP, tag):
        if LorP == "P":
            #return weight of tag in POS tags list
        elif LorP = "L":
            #return weight of tag in label tags list
    

    def load_weights(self, POS_fileName, label_fileName):
        ##Function that loads in the weights list for POS and label tags
        ##Takes in: the pickled file name for POS weights and label weights
        ##Returns: Nothing, just stores the weights in the objects lists
        try:
            self.POS_tags = pickle.load(open("POS_fileName", "rb"))
            self.label_tags = pickel.load(open("label_fileName", "rb"))
        except:
            print("Could not find one of the pickled files")

    #def save_weights(self)

    #def to_string()

    #def train(dictionary)
        
