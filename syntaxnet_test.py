#!/usr/bin/python3
import subprocess
from subprocess import call
import pickle

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
                statement_vector = clean_tree(parseyed_statement)
                x += 1
            elif x == 2:
                # Response
                response = line
                if "'" in response:
                    response = response.replace("'", "\\'")
                parseyed_response = subprocess.check_output('echo ' + response + ' | syntaxnet/demo.sh', shell=True)
                parseyed_response = str(parseyed_response,'utf-8')
                response_vector = clean_tree(parseyed_response)
                # Store statement/response pair in db
                self.add_pair(statement_vector, response_vector)
                x = 1  

        input_data.close()
        self.save_dictionary()
        print("Data added successfully.")
        

    ## def get_best_response(self, input_vector):
        ## Takes in an input vector and runs through the dictionary
        ## Finding the closest vector to the input.
        ## Returns a response in string format

def clean_tree(tree):
    ##Input: Takes in the string representing a tree and cleans it
    ##Idea: Go until you find a \n and take everything before it.
    ##      Then skip every non-alphabet or punctuation character and repeat.
    ##Returns: Vector tuple of sentence: ((sentence_tuple), (word1_list), (word2_list))

    sentence_vector = []
    start_of_tree = tree.find("Input:")
    tree = tree[start_of_tree+7:]
    tree_list = tree.split("\n")
    for word in tree_list:
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
    user_input = input("Text to tag (X to exit): ")
    while user_input != "X":
        #escape single quotes for words such as what're
        if "'" in user_input:
            user_input = user_input.replace("'", "\\'")
            
        stdoutdata = subprocess.check_output('echo ' + user_input + ' | syntaxnet/demo.sh', shell=True)
        stdoutdata = str(stdoutdata,'utf-8')
        vector = clean_tree(stdoutdata)
        print("vector: ", vector)

        user_input = input("Text to tag (X to exit): ")


       
def main():
    print("Training/Test Menu")
    print("------------------")
    print("1. Test parsey on strings")
    print("2. Create/Load dictionary")
    print("X. Exit")
    user_input = input("Choice: ")
    while user_input != "X":
        if user_input == "1":
            #Test run on user strings
            test_run()
        elif user_input == "2":
            #Add data to dictionary
            dic = conversation_dictionary()
            data_file = input("File name of text data to add to dictionary: ")
            dic.add_data(data_file)
            print_dic = input("Would you like to see the dictionary?(y/n): ")
            if print_dic == "y":
                dic.to_string()
        else:
            user_input = input("Choose between option 1 or option 2: ")
        print("\n")
        print("Training/Test Menu")
        print("------------------")
        print("1. Test parsey on strings")
        print("2. Create/Load dictionary")
        print("X. Exit")
        user_input = input("Choice: ")
   
  
main()


