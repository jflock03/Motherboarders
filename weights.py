import pickle

class weights(object):
    def __init__(self):
        ## format of dictionary: {[tag]:weight, [tag2]:weight2}
        self.POS_tags = {}
        self.label_tags = {}

    def get_weight(self, LorP, tag):
        if LorP == "P":
            #return weight of tag in POS tags dictionary
            return self.POS_tags[tag]
        elif LorP = "L":
            #return weight of tag in label tags dictionary
            return self.label_tags[tag]

    def load_weights(self, POS_fileName, label_fileName):
        ##Function that loads in the weights dictionary for POS and label tags
        ##Takes in: the pickled file name for POS weights and label weights
        ##Returns: Nothing, just stores the weights in the objects dictionary
        try:
            self.POS_tags = pickle.load(open("POS_fileName", "rb"))
            self.label_tags = pickel.load(open("label_fileName", "rb"))
        except:
            print("Could not find one of the pickled files")

    def save_weights(self, POS_fileName, label_fileName):
        try:
            pickle.dump(self.POS_tags, POS_fileName)
            pickle.dump(self.label_tags, lable_fileName)
        except:
            print("Could not find one of the pickled files")

    #def to_string()

    #def train(dictionary)
        
