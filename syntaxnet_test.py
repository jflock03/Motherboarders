#!/usr/bin/python3
import subprocess
from subprocess import call
import pickle
import numpy as np
import random

class conversation_dictionary(object):
    ## Dictionary object
    ## Each dictionary key = input vector, value = list of response vectors
    ## Vector format: [[list of words],[tagged root word],[next tagged word],..]
    
    def __init__(self):
        self.dictionary = {}

    def add_pair(self, input_vector, output_vector):
        ## Takes in a tagged input vector and tagged reponse vector
        ## Adds response vector to list of reponses if input vector already exists
        ## If input vector doesn't exist, add new input/output to dictionary
        
        if input_vector in self.dictionary:
            if output_vector not in self.dictionary[input_vector]:
                self.dictionary[input_vector].append(output_vector)
        else:
            self.dictionary[input_vector] = [output_vector]

    def to_string(self):
        for key,value in self.dictionary.items():
            print("key: ", key)
            print("value: ", value)
            print("\n")

    def load_dictionary(self):
        ## Load dictionary and save it as self.dictionary
        if len(self.dictionary) == 0:
            try:
                self.dictionary = pickle.load(open( "dictionary.p", "rb"))
            except:
                print("No existing pickled dictionary")
        else:
            print("Current dictionary not empty, save first.")

    def save_dictionary(self):
        ## Dump (write) dictionary to disk
        pickle.dump(self.dictionary, open( "dictionary.p", "wb"))

    def add_data(self, file_name):
        ## Takes in a txt file name, runs throught the file line by line
        ## input file format: statement on line 1, response line 2, empty line 3
        ## Loads pickled dictionary if it exists then adds key/value pairs
        
        self.load_dictionary()
        input_data = open(file_name, 'r')
        x = 1
        for line in input_data:
            line = line.strip()
            if x == 1:
                # Input statement
                statement = line
                if "'" in statement:
                    statement = statement.replace("'", "\\'")
                parseyed_statement = subprocess.check_output('echo ' + statement + ' | syntaxnet/demo.sh', shell=True)
                parseyed_statement = str(parseyed_statement,'utf-8')
                statement_vector = clean_tree(parseyed_statement, line)
                x += 1
            elif x == 2:
                # Response
                response = line
                if "'" in response:
                    response = response.replace("'", "\\'")
                parseyed_response = subprocess.check_output('echo ' + response + ' | syntaxnet/demo.sh', shell=True)
                parseyed_response = str(parseyed_response,'utf-8')
                response_vector = clean_tree(parseyed_response, line)
                # Store statement/response pair in db
                self.add_pair(statement_vector, response_vector)
                x = 1  

        input_data.close()
        self.save_dictionary()
        print("Data added successfully.")
        
    def compare_parsey_vectors(self, vector1, vector2):
        ##Takes in parseyed vectors1 and 2
        ##Vectors in the form ((sentence tuple), (word1, POS, senTag), (word2, POS, senTag), ...)
        tree_vector = vector1[1:]
        tree_vector2 = vector2[1:]
        numpy_vector = []

        #Only compare words up to the length of the shortest sentence
        for i in range(0, min(len(tree_vector), len(tree_vector2))):
            for j in range(0, 3):
                if tree_vector[i][j] == tree_vector2[i][j]:
                    numpy_vector.append(1)
                else:
                    numpy_vector.append(0)
        numpy_vector.append(1/len(tree_vector))
        numpy_vector = np.array(numpy_vector)
        return np.linalg.norm(numpy_vector)
        
            
    def get_best_response(self, input_vector):
        ## Takes in an input vector and runs through the dictionary
        ## Finding the closest vector to the input.
        ## Returns a response in string format
        best_response = ''
        max_value = 0
        for key, value in self.dictionary.items():
            result_score = self.compare_parsey_vectors(key, input_vector)
            if result_score > max_value:
                max_value = result_score
                random_index = random.randint(0, len(value)-1)
                response_vector = value[random_index][0]
        
        return response_vector
            
        

def clean_tree(tree, initial_sentence):
    ##Input: Takes in the string representing a tree and cleans it
    ##Idea: Go until you find a \n and take everything before it.
    ##      Then skip every non-alphabet or punctuation character and repeat.
    ##Returns: Vector tuple of sentence: ((sentence_tuple), (word1_list), (word2_list))

    sentence_vector = [initial_sentence]
    start_of_tree = tree.find("Input:")
    tree = tree[start_of_tree+7:]
    tree_list = tree.split("\n")
    for word in tree_list[1:]:
        word = word.replace("+--", "")
        word_vector = word.split(' ')
        while '' in word_vector:
            word_vector.remove('')
        while '|' in word_vector:
            word_vector.remove('|')
        if len(word_vector) >= 1 and 'Parse:' not in word_vector:
            sentence_vector.append(tuple(word_vector))
    
    return tuple(sentence_vector)


def test_run():
    dic = conversation_dictionary()
    dic.load_dictionary()
    user_input = input("You (X to exit): ")
    while user_input != "X":
        #escape single quotes for words such as what're
        if "'" in user_input:
            user_input = user_input.replace("'", "\\'")
            
        stdoutdata = subprocess.check_output('echo ' + user_input + ' | syntaxnet/demo.sh', shell=True)
        stdoutdata = str(stdoutdata,'utf-8')
        
        vector = clean_tree(stdoutdata, user_input)
        print("Bot: ", dic.get_best_response(vector))

        user_input = input("You (X to exit): ")
       
def main():
##    dic = conversation_dictionary()
##    dic.add_data('greetings_data.txt')
##    dic.to_string()
    print("--- Welcome to Motherboarders automatic text response program ---")
    print("Options: 1. Add data to dictionary" +
                        " 2. Talk to the bot (X to exit)")
    user_choice = input("Choice: ")
    while user_choice != "X":
        if user_choice == "1":
            file_name = input("Name of data text file: ")
            dic = conversation_dictionary()
            try:
                dic.add_data(file_name)
                print("Finished adding data.")
            except:
                print("No data file of that name found.")   
        elif user_choice == "2":
            test_run()
        else:
            print("Choose option 1 or option 2 or X to exit")
        print("Options: 1. Add data to dictionary" +
                        " 2. Talk to the bot (X to exit)")            
        user_choice = input("Choice: ")
  
main()


