#!/usr/bin/python3

## This object is built using the conversation_dictionary object
## It parses through the dictionary and determines probability of seeing
## a certain word (with tags) in the response, based on the certain word in the
## input being evaluated. It will then have a model that will give the top
## words that should be in the response based on the word evaluated.

class probability_model(object):
    ## Dictionary containing dictionary object
    ## Key = word vector in format (word, POS tag, label tag)
    ## Value = dictionary...
    ##         where key = (POS tag, label tag), value = [word,probability]

    def __init__(self):
        self.dictionary = {}

    #def load_model(self)
        
    #def save_model(self)

    def train(self, dictionary):
        for input_vector, response_vector in dictionary.dictionary.items():
            for word in input_vector[1:]:
                if word not in self.dictionary:
                    ## If tagged input word not already in main dictionary
                    self.dictionary[word] = {}
                    for response in response_vector:
                        for response_word in response[1:]:
                            POS_tag = response_word[1]
                            label_tag = response_word[2]
                            key = (POS_tag, label_tag)
                            if key in self.dictionary[word]:
                                self.dictionary[word][key].append(response_word[0])
                            else:
                                self.dictionary[word][key] = [response_word[0]]
                else:
                    ## Tagged input word is already in main dictionary
                    for response in response_vector:
                        for response_word in response[1:]:
                            POS_tag = response_word[1]
                            label_tag = response_word[2]
                            key = (POS_tag, label_tag)
                            if key in self.dictionary[word]:
                                self.dictionary[word][key].append(response_word[0])
                            else:
                                self.dictionary[word][key] = [response_word[0]]

        self.to_string()

    def to_string(self):
        for key, val in self.dictionary.items():
            print("Input Key: ", key)
            for key2, val2 in val.items():
                print("Response tags key: ", key2, end = "   ")
                print("value: ", val2)
            print("-----------------------------------")

                        

    #def get_response(self, input_sentence, output_format)
    ## Input: parseyed input sentence & output sentence format
    ## Output: String of response sentence
    ## Method: iterate over words in input_sentence then
    ##         iterate over POStag/labeltag in output sentence format
    ##         for each tag pair look up the corresponding key
    ##         its value will be the words with probabilities.
    ##         Get list of words that all of the input words share.
    ##         Use most used word when from this list.
    ##         i.e max(sum of prob(inword, outword) * prob(inword2, outword2)..)

##dictionary = {}
##dictionary[(('hello', 'UH', 'discourse'),)] = [(('hi', 'UH', 'discourse'),), (('yo', 'UH', 'discourse'),)]
##dictionary[(('hello', 'UH', 'discourse'), ('man', 'NN', 'nn'))] = \
##           [(('hi', 'UH', 'discourse'), ('man','NN', 'nn')), (('yo', 'UH', 'discourse'),)]
##
##dic = probability_model()
##dic.train(dictionary)
##dic.to_string()
    

