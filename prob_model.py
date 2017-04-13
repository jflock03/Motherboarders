#!/usr/bin/python3

import pickle
import random

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

    def load_dictionary(self):
        ## Load dictionary and save it as self.dictionary
        if len(self.dictionary) == 0:
            dic_file = input("Dictionary model file name to load: ")
            try:
                self.dictionary = pickle.load(open( dic_file, "rb"))
            except:
                print("No existing pickled dictionary model. Creating empty one.")
        else:
            print("Current dictionary model not empty, save first.")
        
    def save_dictionary(self):
        ## Dump (write) dictionary to disk
        dic_file = input("Dictionary file name to save to: ")
        pickle.dump(self.dictionary, open( dic_file, "wb"))

    def train(self, dictionary):
        for input_vector, response_vector in dictionary.dictionary.items():
            for word in input_vector[1:]:
                word = word[0]
                if word not in self.dictionary:
                    ## If tagged input word not already in main dictionary
                    self.dictionary[word] = {}
                    for response in response_vector:
                        for response_word in response[1:]:
                            POS_tag = response_word[1]
                            label_tag = response_word[2]
                            key = (POS_tag, label_tag)
                            
                            if key not in self.dictionary[word]:
                                self.dictionary[word][key] = {}
                                
                            if response_word[0] in self.dictionary[word][key]:
                                self.dictionary[word][key][response_word[0]]+=1
                            else:
                                self.dictionary[word][key][response_word[0]] = 1
                else:
                    ## Tagged input word is already in main dictionary
                    for response in response_vector:
                        for response_word in response[1:]:
                            POS_tag = response_word[1]
                            label_tag = response_word[2]
                            key = (POS_tag, label_tag)
                            
                            if key not in self.dictionary[word]:
                                self.dictionary[word][key] = {}
                                
                            if response_word[0] in self.dictionary[word][key]:
                                self.dictionary[word][key][response_word[0]]+=1
                            else:
                                self.dictionary[word][key][response_word[0]] = 1

        self.to_string()

    def to_string(self):
        for key, val in self.dictionary.items():
            print("Input Key: ", key)
            for key2, val2 in val.items():
                print("Response tags key: ", key2, end = "   ")
                print("value: ", val2)
            print("-----------------------------------")

                        
    def remove_words_from_tags(self, tagged_sentence):
        my_lis = []
        for tagged_word in tagged_sentence:
            tags = tagged_word[1:]
            my_lis.append(tags)

        return tuple(my_lis)

    def find_max(self, dictionary):
        myMax = 0
        myWordCandidates = []
        for word, count in dictionary.items():
            if count > myMax:
                myMax = count
                myWordCandidates = [word]
            elif count == myMax:
                myWordCandidates.append(word)
        i = random.randint(0, len(myWordCandidates)-1)
        return myWordCandidates[i]
            
    def get_response(self, input_sentence, output_format):
        
        strip_format = self.remove_words_from_tags(output_format)
        response_string = ''
        for tags in strip_format:
            response_candidates = {}
            for tagged_word in input_sentence:
                my_words = self.dictionary[tagged_word[0]][tags]
                for word in my_words:
                    if word in response_candidates:
                        response_candidates[word] += my_words[word]
                    else:
                        response_candidates[word] = my_words[word]
            response_word = self.find_max(response_candidates)

            response_string += response_word
            response_string += ' '

        return response_string
        
    


    

