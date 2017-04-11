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
        self.dictionary{}

    #def load_model
        
    #def save_model

    #def train(dictionary)

    #def get_best_sentence(input_sentence, output_format)
    ## Input: parseyed input sentence & output sentence format
    ## Output: String of response sentence
    ## Method: iterate over words in input_sentence then
    ##         iterate over POStag/labeltag in output sentence format
    ##         for each tag pair look up the corresponding key
    ##         its value will be the words with probabilities.
    ##         Get list of words that all of the input words share.
    ##         Use most used word when from this list.
    ##         i.e max(sum of prob(inword, outword) * prob(inword2, outword2)..)

