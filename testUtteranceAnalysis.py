import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
from nltk.util import ngrams
import os
import re
import json
import jsonlines
import matplotlib
import seaborn
import numpy
import pandas
import time
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
Alen Smailagić
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
Anderson Varejão
Briante Weber
Leandro Barbosa
Harrison Barnes
Festus Ezeli
Brandon Rush
Marreese Speights
Jason Thompson
Justin Holiday
Ognjen Kuzmić
David Lee
Hilton Armstrong
Steve Blake
MarShon Brooks
Jordan Crawford
Dewayne Dedmon
Toney Douglas
Nemanja Nedović
Jermaine O'Neal
Andris Biedriņš
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
Vladimir Radmanović
Al Thornton
Reggie Williams
Brandan Wright"""

listAllWarriorsPlayers = badFormatWarriorsPlayers.splitlines()
warriorsPlayersFullNames = []
for name in listAllWarriorsPlayers:
    name = name.lower()
    nameSeparate = name.split()
    if(name == "Stephen Curry"):
        warriorsPlayersFullNames.append([name, 'Steph', nameSeparate[0], nameSeparate[1]])
    else:
        warriorsPlayersFullNames.append([name, nameSeparate[0], nameSeparate[1]])


combinedConversations = ""
with jsonlines.open('linesUtterances.jsonl') as reader:
    for utterance in reader:
        combinedConversations += utterance['text'] + " "
    combinedConversations = combinedConversations.lower()
    combinedConversations = re.sub(r'[^a-zA-Z\s\']', ' ', combinedConversations)
    token = nltk.word_tokenize(combinedConversations)
print(token)


# listDates = []

# with jsonlines.open('linesUtterances.jsonl') as reader:
#     for obj in reader:
#         listDates.append(time.strftime("%m/%d/%Y", time.localtime(obj['timestamp'])))

# counterDates = Counter(listDates)
# commonDates = counterDates.most_common(5)
# print(commonDates)