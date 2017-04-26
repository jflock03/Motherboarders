#!/usr/bin/python3
import subprocess
from subprocess import call
import pickle
import numpy as np
import random
import time
from prob_model import probability_model as model
from conversation_dictionary import conversation_dictionary as conversation_dic

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


def talk_to():
    dic = conversation_dic()
    prob_model = model()
    dic.load_dictionary()
    prob_model.train(dic)
    user_input = input("You (X to exit): ")
    while user_input != "X":
        user_input = user_input.lower()
        #escape single quotes for words such as what're
        if "'" in user_input:
            user_input = user_input.replace("'", "\\'")
            
        stdoutdata = subprocess.check_output('echo ' + user_input + ' | syntaxnet/demo.sh', shell=True)
        stdoutdata = str(stdoutdata,'utf-8')
        
        vector = clean_tree(stdoutdata, user_input)

        answer, resp = dic.get_best_response(vector)
        if answer == 0:
            print("Bot: ", resp)
        else:
            try:
                print("Bot:", prob_model.get_response(vector, resp))
            except: #Words not found in probability, just return resp
                print("Bot:", resp[0])

        user_input = input("You (X to exit): ")
       
def main():
    print("--- Welcome to Motherboarders automatic text response program ---")
    print("-"*75)
    print("Options: 1. Add data to the bot" +
                        " 2. Talk to the bot (X to exit)")
    user_choice = input("Choice: ")
    while user_choice != "X":
        if user_choice == "1":
            file_name = input("Name of data text file: ")
            dic = conversation_dic()
            dic.add_data(file_name)
##            except:
##                print("No data file of that name found.")   
        elif user_choice == "2":
            talk_to()
        else:
            print("Choose option 1 or option 2 or X to exit")
        print("-"*75)
        print("Options: 1. Add data to the bot" +
                        " 2. Talk to the bot (X to exit)")            
        user_choice = input("Choice: ")
  
main()


