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
        ## Iterate through the input/response dictionary and create prob model
        for input_vector, response_vector in dictionary.dictionary.items():
            for word in input_vector[1:]:
                word = word[0]
                word = word.lower()
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
                                ## maybe lowercase response word?
                                self.dictionary[word][key][response_word[0]] = 1


    def to_string(self):
        for key, val in self.dictionary.items():
            print("Input Key: ", key)
            for key2, val2 in val.items():
                print("Response tags key: ", key2, end = "   ")
                print("value: ", val2)
            print("-----------------------------------")

                        
    def remove_words_from_tags(self, tagged_sentence):
        ## Removes the word from it's tags in order to put it into the
        ## probability dicitonary. ex: (hand, NN, nsubj) to (NN, nsubj)
        my_lis = []
        for tagged_word in tagged_sentence:
            tags = tagged_word[1:]
            my_lis.append(tags)

        return tuple(my_lis)

    def find_max(self, dictionary):
        ## Finds the highest probable word from the corresponding tags
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

    def reorder_vector(self, vector):
        ## Reorders the vector that parsey returns into it's original word order
        string = vector[0]
        tagged_words = vector[1:]

        indexed_list = []
        seen_words = []

        for tagged_word in tagged_words:
            word = tagged_word[0]
            seen_count = seen_words.count(word)
            if seen_count > 0:
                new_string = string
                char_skipped = 0
                for i in range(seen_count):
                    ind = new_string.find(word)
                    char_skipped += (ind + len(word))
                    new_string = new_string[ind+len(word):]
                ind = new_string.find(word)
                index = ind + char_skipped        
            else:
                seen_words.append(word)
                index = string.find(word)

            tagged_word_list = [index, word, tagged_word[1], tagged_word[2]]
            indexed_list.append(tagged_word_list)

        new_string = ''

        return_list = []
        while len(indexed_list) > 0:
            cur = min(indexed_list[j][0] for j in range(0,len(indexed_list)))
            for tagged_word in indexed_list:
                if tagged_word[0] == cur:
                    return_list.append(tuple(tagged_word[1:]))
                    indexed_list.remove(tagged_word)
        return tuple(return_list)
            
    def get_response(self, input_sentence, output_format):
        ## Creates a list of reponse candidates corresponding with the current
        ## tagged words from the input sentence. Then gets the most probable
        ## words and creates a sentence by concatenating them together.
        
        reordered_output_format = self.reorder_vector(output_format)
        strip_format = self.remove_words_from_tags(reordered_output_format)
        response_string = ''
        x = 0
        for tags in strip_format:
            response_candidates = {}
            for tagged_word in input_sentence[1:]:
                try:
                    my_words = self.dictionary[tagged_word[0]][tags]
                    word_sum = sum(my_words.values())
                    for word in my_words:
                        if word in response_candidates:
                            response_candidates[word] += my_words[word] / word_sum
                        else:
                            response_candidates[word] = my_words[word] / word_sum
                except:
                    # No tags corresponding to current word
                    continue

            response_word = self.find_max(response_candidates)

            if x == 0 or response_word == "," or response_word == "." \
               or "'" in response_word or reponse_word == "?" \
               or reponse_word == "!":
                response_string += response_word
            else:
                response_string += ' ' + response_word
            x = 1

        return response_string
        
    


    

