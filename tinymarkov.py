from sys import argv
import re
from random import choice
import string
import twitter

api = twitter.Api(consumer_key='DSL1YlRGJWzN4YC23pBZQ', 
    consumer_secret='xNpXY7WjmsHmaUP1p9cAkw0Sh8fu6oQdySUhncQ0U', 
    access_token_key='1278792427-k9UpLpiYKL6MfTmuLJrFtMJ2VTD3lQ9KAYiG35B', 
    access_token_secret='zOgkUB5riRnnef6ZnDt10QLN5hnwbww1K5jzt7RW0')

def tweet(random_string):
	api.PostUpdate(random_string)


NGRAM_SIZE = 2

def main():
	script, filename = argv

	text = open(filename).read()
	chains = make_chains(text)
	sentence_list = markov_text(chains)
	tweet = make_sentence(sentence_list)

	print tweet

def make_chains(text):
	wordlist = []
	text = re.sub("[\[\.\?\-\+:;\]\(\)\"]", " ", text.lower())
	wordlist = text.split() # return a list, where each item is one line
	d = {}

	ngram = tuple([ wordlist.pop(0) for i in range(NGRAM_SIZE) ])

	# makes chains
	while wordlist:
		next = wordlist.pop(0)
		d.setdefault(ngram, []).append(next)
		ngram = ngram[1:] + (next,)

	return d

	# for idx in range(len(wordlist)-2):
	# 	k = (wordlist[idx], wordlist[idx+1])
	# 	v = wordlist[idx+2]

	# 	d.setdefault(k, []).append(v)

		# if k in d:
		# 	d[k].append(v)
		# else:
		# 	d[k] = [v]


def markov_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    # randomly pick a tuple, 2 partnered words, which is a random key in dictionary now being referred to as "chains" from when it was an argument during the calling of make_text
    firsttuple = choice(chains.keys())
    markoved_output = []
    random_to_add = [firsttuple[0],firsttuple[1]]
    total_length = len(firsttuple[0]) + len(firsttuple[1])
    #print chains

    while total_length < 141:
        markoved_output += random_to_add

        last_twople = (markoved_output[-2], markoved_output[-1])
        listpossiblewords = chains[last_twople]
        
        random_to_add = [choice(listpossiblewords)]

        total_length += len(random_to_add[0])

        # make sure that the sentence doesn't end super awkwardly...    

    # different than last two words because the second index of last_twople is the first word of last_two_words
    #make sure after the while loop has discovered that if it were to add a word, it'd go over 140 chars, and STOPS, that the variable we're using to represent the last word 
    last_two_words = markoved_output[-2] + ' ' + markoved_output[-1]    
    last_word = markoved_output[-1]
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

def make_sentence(random_list):
    random_string = ""

    # turn the list of markov'd words into a sentence-ish string
    for index, word in enumerate(random_list):
        # if it's the first word:
        if index == (len(random_list) - 1):
            random_string += word + "."
            break
        if index == 0:
            random_string += string.capwords(word) + " "
        else:
            random_string += word + " "

    return random_string

if __name__ == "__main__":
    main()
