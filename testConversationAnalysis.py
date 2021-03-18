import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.util import skipgrams
import re
import json
import jsonlines
from collections import Counter

badFormatWarriorsPlayers = """Kent Bazemore
Marquese Chriss
Stephen Curry
Draymond Green
Damion Lee
Kevon Looney
Nico Mannion
Mychal Mulder
Kelly Oubre
Eric Paschall
Jordan Poole
Alen Smailagic
Juan Toscano-Anderson
Brad Wanamaker
Andrew Wiggins
James Wiseman
Dragan Bender
Ky Bowman
Alec Burks
Willie Cauley-Stein
Jacob Evans
Zach Norvell
Jeremy Pargo
Chasson Randle
Glenn Robinson
D'Angelo Russell
Omari Spellman
Jordan Bell
Andrew Bogut
Quinn Cook
DeMarcus Cousins
Marcus Derrickson
Kevin Durant
Andre Iguodala
Jonas Jerebko
Damian Jones
Shaun Livingston
Alfonzo McKinnie
Klay Thompson
Chris Boucher
Omri Casspi
Patrick McCaw
JaVale McGee
Zaza Pachulia
David West
Nick Young
Matt Barnes
Ian Clark
James Michael McAdoo
Anderson Varejao
Briante Weber
Leandro Barbosa
Harrison Barnes
Festus Ezeli
Brandon Rush
Marreese Speights
Jason Thompson
Justin Holiday
Ognjen Kuzmic
David Lee
Hilton Armstrong
Steve Blake
MarShon Brooks
Jordan Crawford
Dewayne Dedmon
Toney Douglas
Nemanja Nedovic
Jermaine O'Neal
Andris Biedrins
Jarrett Jack
Richard Jefferson
Charles Jenkins
Carl Landry
Malcolm Thomas
Jeremy Tyler
Earl Barron
Keith Benson
Kwame Brown
Monta Ellis
Mickell Gladness
Dominic McGuire
Mikki Moore
Nate Robinson
Ish Smith
Ekpe Udoh
Chris Wright
Dorell Wright
Jeff Adrien
Lou Amundson
Charlie Bell
Rodney Carney
Dan Gadzuric
Acie Law
Jeremy Lin
Vladimir Radmanovic
Al Thornton
Reggie Williams
Brandan Wright"""

#Converts names separated by lines to a list
listAllWarriorsPlayers = badFormatWarriorsPlayers.splitlines() 

warriorsPlayersFullNames = []
for name in listAllWarriorsPlayers:
    name = name.lower()
    #Splits a players name into [firstName, lastName]
    nameSeparate = name.split() 

    #adds entries [fullName, firstName, lastName]
    warriorsPlayersFullNames.append([name, nameSeparate[0], nameSeparate[1]])

#Load file data into an variable
with open('./conversations.json') as f:
    sample_conversation_data = json.load(f)

def parseAndCombine():
    combinedTitles = ""
    #Iterate over each JSON object (post) and add the title text to a string
    for post in sample_conversation_data:
        combinedTitles += sample_conversation_data[post]['title'] + " "
    combinedTitles = combinedTitles.lower()
    #Substitute all non-letter characters with a space 
    combinedTitles = re.sub(r'[^a-zA-Z\s]', ' ', combinedTitles)
    #Separate each word in a string into an element of a list
    token = nltk.word_tokenize(combinedTitles)
    return token

#Counts all n-grams of size numWords with list token
def ngramAnalysis(token, numWords):
    ngramsCounter = Counter(ngrams(token, numWords)) 
    return ngramsCounter

#Counts all skip-grams of size numWords with list token separated by numSkip
def skipGramAnalysis(token, numWords, numSkip):
    skipgramsCounter = Counter(skipgrams(token, numWords, numSkip))
    return skipgramsCounter

#unigrams has the count of each unigram in the file, we filter entries using mentions
def unigramCounter(unigrams, mentions):
    #For each player in the set of players
    for nameArray in warriorsPlayersFullNames:
        counter = 0
        #Iterates through all single word names in nameArray
        for i in range(1, len(nameArray)):
            counter += unigrams[(nameArray[i],)]
        #Adds the amount of mentions of each word to the respective entry
        mentions[nameArray[0]] = mentions.get(nameArray[0], 0) + counter
    return mentions

#bigrams has the count of each bigram in the file, we filter entries using mentions
def bigramCounter(bigrams, mentions):
    for nameArray in warriorsPlayersFullNames:
        #Returns the amount of bigrams with the corresponding full name
        counter = bigrams[(nameArray[1], nameArray[2])]
        mentions[nameArray[0]] = mentions.get(nameArray[0], 0) + counter
    return mentions

# Set dictionaries to map player names to their occurences
warriorsConversationUnigrams = {}
warriorsConversationBigrams = {}
warriorsUtterancesUnigrams = {}
warriorsUtterancesBigrams = {}

# Return a list of tokens for each word in the file
tokenized = parseAndCombine()

# Return each unigram, bigram, and trigram with its corresponding count
collectionConversationUnigrams = ngramAnalysis(tokenized, 1)
collectionConversationBigrams = ngramAnalysis(tokenized, 2)
# collectionConversationTrigams = ngramAnalysis(tokenized, 3)

#Print the most common unigrams, bigrams, trigrams
# commonUnigrams = collectionConversationUnigrams.most_common(250)
# commonBigrams = collectionConversationBigrams.most_common(250)
# commonTrigrams = collectionConversationTrigams.most_common(250)

# for key, value in commonTrigrams:
#     print(key[0] + " " + key[1] + " " + key[2] + " " + str(value))

# Filter according to the Warriors Players
commonNamesUnigram = unigramCounter(collectionConversationUnigrams, warriorsConversationUnigrams) 
commonNamesBigram = bigramCounter(collectionConversationBigrams, warriorsConversationBigrams)

for key in commonNamesUnigram:
    print(key + " " + str(commonNamesUnigram[key]))

for key in commonNamesBigram:
    print(key + " " + str(commonNamesBigram[key]))


# #Finds the 20 most frequent skip grams with i words in i + 3 range
# for i in range(2, 6):
#     print(skipGramAnalysis(tokenized, i, i + 3).most_common(20))


# with jsonlines.open('utterances.jsonl') as reader:
#     readLine = 1
#     for utterance in reader:
#         print('read' + str(readLine))
#         readLine += 1
#         combinedConversations = utterance['text']
#         combinedConversations = combinedConversations.lower()
#         combinedConversations = re.sub(r'[^a-zA-Z\s\']', ' ', combinedConversations)
#         combinedConversations = nltk.word_tokenize(combinedConversations)
#         collectionUtteranceUnigrams = unigramAnalysis(combinedConversations)
#         unigramCounter(collectionUtteranceUnigrams, warriorsUtterancesMentions)

# tokenized = parseAndCombine()
# # collectionConversationUnigrams = unigramAnalysis(tokenized)
# collectionConversationBigrams = bigramAnalysis(tokenized)
# print(collectionConversationBigrams)

# collectionUtteranceUnigrams = unigramAnalysis(combinedConversations)
# collectionUtteranceBigrams = bigramAnalysis(combinedConversations)
# print(unigramCounter(collectionConversationUnigrams, warriorsConversationMentions))
# print(warriorsUtterancesMentions)

# print(collectionUnigrams.most_common(100))
# print(collectionBigrams.most_common(100))

# def analyzeSentimentSampleConversations():
#     compound = []
#     for post in sample_conversation_data:
#         sentiment = analyzer.polarity_scores(
#             sample_conversation_data[post]['title'])
#         compound.append(sentiment['compound'])
#     return compound

# analyzeSentimentSampleConversations()
