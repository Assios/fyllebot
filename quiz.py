#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random

users = {'assios':{'quiz':0,'creds':0,'alltimequiz':0}, 'aleksanb':{'quiz':0,'creds':0,'alltimequiz':0}, 'torcm':{'quiz':0,'creds':0,'alltimequiz':0}, 'sigveseb':{'quiz':0,'creds':0,'alltimequiz':0}}

#POENGSYSSTEM:

def addPoints(username, field):
	users[username][field]+=1
def getPoints(username, field):
	try:
		return users[username][field]
	except:
		return -1

def resetScore(users):
	for brukere in users:
		users[brukere]['alltimequiz'] += users[brukere]['quiz']
		users[brukere]['quiz'] = 0


def getWinner(users):
	theuser = max(users, key=lambda x:users[x]['quiz'])
	return 'The winner is ' + theuser + ' with ' + str(users[theuser]['quiz']) + ' points.'

def makeListOfNumbers(questions, numberOfQuestions):
	nums = range(len(questions))
	random.shuffle(nums)
	return nums[:numberOfQuestions]

def getQuestions(filen = 'questions.txt'):
	return [line for line in open(filen, 'r')]

def getAnswers(filen = 'answers.txt'):
	f = open(filen, 'r+')
	string = ''
	for linje in f:
		string+=linje
	tempList = string.splitlines()
	for i in range(0, len(tempList)):
		if (('[' in tempList[i]) and (']' in tempList[i]) and (', ' in tempList[i])):
			tempList[i] = tempList[i][1:-1]
			tempList[i] = tempList[i].lower().split(', ')
		else:
			placeholder = []
			placeholder.append(tempList[i].lower())
			tempList[i] = placeholder
	return tempList

def checkAnswer(answerList, count, answer):
	for svar in answerList[count]:
		if (svar == answer):
			return True
	return False

def printQuiz(users):
	strr=''
	for brukere in users:
		strr+=(brukere + ': ' + str(users[brukere]['alltimequiz'] + ' poeng. '))
	return strr