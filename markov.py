#!/usr/bin/env python

"""
things to fix later:
- maybe words that end with a period should NOT have the next word be included in their markov rule list because it's a separate, potentially unrelated sentence.
    --> but then do you have to keep periods on the words instead of stripping them off?
    --> and do you ALSO need those because how will you make full sentences in the generator otherise --> is it just a gamble if the sentence is "ended"?
    --> aiming to have a cycle that deletes the last two words if they're "awkard" and shouldn't actually be at the end of a sentence
"""

from sys import argv
from random import choice
import string
import re

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    # first take the 1-string text, turn it into list of words
    wordlist = []
    linelist = corpus.splitlines() # return a list, where each item is one line
    list_to_add = []
    
    # split lines into lists of words with NO PUNCTUATION except for apostrophes and hyphens
    for line in linelist:
        # make a list of words (anything separated by whitespace) for each iterated line
        list_to_add = re.split(' ', line)
        """want to find only words of this pattern: r'\w+(?:-\w)+' but how do you split ones that DON'T follow the pattern like 'alas--we' ???"""
        # go through the list of words that have been split at the whitespace to remove the punctuation from each line 
        """ DOESN'T YET WORK TO DELETE PUNCTUATION"""
        for ind, word in enumerate(list_to_add):
            # string.maketrans("","") makes lookup table, translate then performs raw string ops in C using that with string.punctuation (which just has all the symbols we wanna get rid of)
            list_to_add[ind] = word.translate(string.maketrans("",""),string.punctuation)
        # deletes empty strings from list of strings
        list_to_add = filter(bool, list_to_add) # fastest
        # append that list of words to your FULL list of words
        wordlist += list_to_add 
    # kdo I need the following for getting rid of empty paces in the wordlist?
    
    index = 0
    # make dictionary
    markov_dict = {}
    # take every word FROM THE LIST and make a dictionary key of it if none exists
    # the dictionary value will be a list INCLUDING the following word
    # if the word exists in the dictionary
    for word in wordlist:
        # if we're NOT at the second to last word, then make the spot in the dictionary for it, otherwise the last word doesn't have a following word so you should do anything.
        if index < (len(wordlist)-2):
            word_plus_secondword = (word, wordlist[index+1])
            third_word = wordlist[index+2]
            # check to see if word PAIR is key in dictionary
            if word_plus_secondword in markov_dict:
                """
                EASIER WAY WITHOUT KEEPING COUNT FOR EACH APPEARANCE OF FOLLOWING WORD 
                """
                # if in dictionary, add THIRD word following pair to LIST found in values of that place in the dictionary
                markov_dict[word_plus_secondword].append(third_word) 

                """HARDER WAY NOT YET CODED OF KEEPING COUNT
                """
                # for index, (second_word, sec_word_count) in enumerate(nextword_list)
                # iterate through the markov dictionary to use the second_word list 
                # which means either increase the count or add a NEW word that follows if the word isn't in the tuple list
                
                # GET THE VALUE
                # nextword_list = markov_dict[word]
                # # print nextword_list
                # nextword = wordlist[index+1]
                # #                                 0           1              2
                # # markov_dict = {"the": (("animal", 1), ("pig", 1), ("stuff", 1)), "animal": ("does", 1), ("fell",1)}
                # if nextword in nextword_list:
                #     # use find to get index of nextword
                #     tempindex = nextword_list.index(nextword)
                #     temptuple = nextword_list[tempindex]
                #     # this index gives you a LIST of length 2 (tuple)
                #     temptuple[] += 1
                #     nextword_list[tempindex] = temptuple
                #     markov_dict[word] = nextword_list
                # else:
                #     pass


                    # add new tuple of that (nextword, 1)
                # [(wordlist[index+1]).lower(),1]

                # word.lower(), secondword_list in markov_dict.iteritems():
                # print "%s is a word here?" % word
                # LEARN TO USE ONLY VALUES OF DICTS
                
                # if it is 
                # check to see if 2nd_word is in tuples

                # iterate through value list
                # check if 2nd word is in list
                    # if is, add one to count
                    # if it isn't, append tuple to list, with count = 1
                # if it isn't
            else:
                # print "%s isn't present" % word
                markov_dict[word_plus_secondword]=[third_word]
                
                """for later when I make it more efficient"""
                # add third word in with count = 1 as first list of 2 in a list of words
                # markov_dict[word_plus_secondword]=[wordlist[index+2],1]

            # tell index count we're gonna be on the next word
            index += 1
    # return the dictionary so that it can be used to feed it to the next function
    return markov_dict

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    # randomly pick a tuple, 2 partnered words, which is a random key in dictionary now being referred to as "chains" from when it was an argument during the calling of make_text
    firsttuple = choice(chains.keys())
    markoved_output = []
    random_to_add = [firsttuple[0],firsttuple[1]]
    total_length = len(firsttuple[0]) + len(firsttuple[1])
    #print chains

    while total_length < 1000:
        markoved_output += random_to_add

        last_twople = (markoved_output[-2], markoved_output[-1])
        listpossiblewords = chains[last_twople]
        
        random_to_add = [choice(listpossiblewords)]

        total_length += len(random_to_add[0])

        # make sure that the sentence doesn't end super awkwardly...    
    
    # different than last two words because the second index of last_twople is the first word of last_two_words
    #make sure after the while loop has discovered that if it were to add a word, it'd go over 140 chars, and STOPS, that the variable we're using to represent the last word 
    last_two_words = markoved_output[-2] + ' ' + markoved_output[-1]    
    print last_two_words 
    last_word = markoved_output[-1]
    print last_word
    # this should ONLY run once this while loop is FINISHED, however, I want to loop back to markov-ing process in case like every cycled last 2 words ends up having one of these words in it...
    # "the" can be the second to last word but not the LAST word!
    while "the" in last_word or "a" in last_word or "an" in last_word or "and" in last_two_words or "but" in last_two_words or "therefore" in last_two_words or "so" in last_two_words or "because" in last_two_words or "however" in last_two_words or "or" in last_two_words or "of" in last_two_words or "in" in last_two_words or "over" in last_two_words:

        markoved_output = markoved_output[:-2]
        # make sure to subtract the length from total_length of whatever you deleted so the while loop keeps happening until it really reaches 140 chars.
        total_length -= len(markoved_output[-1]) - len(random_to_add[0])
        last_two_words = markoved_output[-2] + ' ' + markoved_output[-1]    
        last_word = markoved_output[-1]
    
    # use that function that turns the string into "sentence strings" with the first letter before the period capitalized, etc etc.
    return markoved_output

def main():
    script, filename = argv

    text = open(filename).read()

    chain_dict = make_chains(text.lower())
    random_text = make_text(chain_dict)

    random_string = ""

    # turn the list of markov'd words into a sentence-ish string
    for index, word in enumerate(random_text):
        # if it's the first word:
        if index == (len(random_text) - 1):
            random_string += word + "."
            break
        if index == 0:
            random_string += string.capwords(word) + " "
        else:
            random_string += word + " "

    # if the last word or second to last word is a conjunction, then delete from that word until the end --> a sentence most likely won't have a natural feel if it doesn't at least have 2 words following a conjunction.
    
    print random_string

if __name__ == "__main__":
    main()

"""
dictMarkov:
{the: [(animal, 2), (pig, 4), (farm, 1), (water,9)]}
"""