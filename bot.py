#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import socket, random, re, string, time, datetime, os, urllib, shlex, urllib2, json, math
from time import sleep
from pprint import pprint
from xml.dom.minidom import parseString

network = 'irc.quakenet.org'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 1024 )
channel = '#fyllechat'
irc.send ( 'NICK fyllebot\r\n' )
irc.send ( 'USER fyllebot fyllebot fyllebot :FylleBOOOT\r\n' )
irc.send ( 'JOIN '+channel+'\r\n' )
irc.send ( 'PRIVMSG '+channel+ ' :HEI ASS.\r\n' )

def send(melding):
   irc.send ( 'PRIVMSG ' + channel + ' :' + melding + '\r\n' )
def privsend(melding):
   irc.send('PRIVMSG ' + user + ' :' + melding + '\r\n')

from imdb import *
from mat import *
from admins import *
from quiz import *

lastUrls = []

#QUIZ START

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
   return 'Vinneren er ' + theuser + ' med ' + str(users[theuser]['quiz']) + ' poeng!'

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
      strr+=(brukere + ': ' + str(users[brukere]['alltimequiz']) + ' poeng. ')
   return strr

#QUIZ END

def array_multiplier(message):
   #if message.split("--")[-1]=="verbose":
      #verbose = True
      #vurdere å implementere --verbose (debug info underveis, mellomregning etc)

   v1,v2 = [eval(re.sub("[^0-9,\.\[\]]*","",i)) for i in message.split("*")]
   final_array = [[None]*len(v2[0]) for i in range(len(v1))]
   #send(str(len(v2[0])),str(len(v1)))

   for a in range(len(v1)):
      for b in range(len(v2[0])):
         current = 0
         for c in range(len(v2)):
            current += (v1[a][c] * v2[c][b])
            #if verbose:
               #send(str(v1[a][c],"*",v2[c][b]))
               #send(str("nåværende delsum er",current))
         #if verbose:
            #send(str("adding",current,"to",a," , ",b))
         final_array[a][b] = current

   send("___RESULTAT___")
   for i in range(len(v1)):
      send("  "+str(final_array[i]))

def stengetidpolet():
    dato = str(datetime.datetime.now())
    aar = int(dato[0:4])
    maaned = int(dato[5:7])
    dag = int(dato[8:10])
    dato = datetime.date(aar, maaned, dag)
    polet = [17, 17, 17, 18, 18, 15, 10000]
    aapent = 1
    poltid = polet[dato.weekday()]
    tiden = str(datetime.datetime.now())
    timer = int(tiden[11:13])+1
    minutt = int(tiden[14:16])
    if (dato.weekday() >= 0) and (dato.weekday() <= 3):
        if timer<10:
            aapent = 0
            send('Polet er stengt. åpner om ' + str(10-timer) + ' timer og ' + str(59-minutt) + ' min')
    elif (dato.weekday() == 4) or (dato.weekday() == 5):
        if timer<9:
            aapent = 0
            send('Polet er stengt. åpner om ' + str(9-timer) + ' timer og ' + str(59-minutt) + ' min')
    elif (dato.weekday() == 6):
        aapent = 0
        send('Polet er stengt i dag, sjekk barskapet')
    polsteng = poltid - timer
    polmin = 59-minutt
    if polsteng < 0:
      send('Polet er stengt for i dag :( Sjekk barskapet og prøv igjen i morra!')
      return ''
    if aapent==1:
        send (str(polsteng)+' timer og '+str(polmin) + 'min til stengetid')
    return ''

def randomSupSvar():
   nr = random.randint(0, 7)
   mld = ["Drikker tequila!", "Shotter vodka ass.", "Drikker rista martini. Ikke stirra", "leker batman. I'M BATMAN!", "NANANANANA BATMAAAN!", "LOLOLOLO SUPERMAAN!", "zzZZZzZZZZSOVNER ASS", "ssshhhhh, prøver å gjemme meg!"]
   return mld[nr]

def lastUrl(newurl):
   if len(lastUrls) < 5:
      lastUrls.append(newurl)
   elif len(lastUrls) == 5:
      for i in range(0, len(lastUrls)-1):
         lastUrls[i] = lastUrls[i+1]
      lastUrls[4] = newurl

def rhapsody():
   f = open('lyrics.txt', 'r+')
   string=''
   for linje in f:
    string+=linje
   lyrics = string.splitlines()
   for i in range(len(lyrics)):
      if (lyrics[i].lower() in message):
         irc.send ( 'PRIVMSG ' + channel + ' :'+lyrics[i+1]+'\r\n' )

def sjekketriks():
   f = open('sjekketriks.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   sjekketriks = string.splitlines()
   tall = random.randint(0, len(sjekketriks)-1)
   string = sjekketriks[tall]
   return string

def returnURLs(message):
   start = message.find('http://')
   end = -1
   urlen = fyllemessage[start:]
   urlen = shlex.split(urlen)[0]
   lastUrl(urlen)
   return urlen


def urlTitle(url):
   filehandle = urllib.urlopen(url).read()
   start = filehandle.find('<title>')
   end = filehandle.find('</title>')
   return filehandle[start:end][7:]

def count(tall):
   tallet = int(tall)
   if (tallet > 60):
      send("kanke telle så langt")
      return
   for i in range(0, tallet+1):
      send(str(tallet-i))
      sleep(1.1)

def beer():
   mottaker = user;
   f = open('beer.txt', 'r+')
   for linje in f:
      irc.send('NOTICE ' + mottaker +  ' :' + linje + '\r\n')
      sleep(0.2)

def langsetning():
   f = open('langsetning.txt', 'r+')
   for linje in f:
      send(linje)
      sleep(0.4)

def fylla():
   f = open('fylla.txt', 'r+')
   string = ""
   for line in f:
      string+= line
      send(string)

def randomPong():
   pongstr = ['|    .', '|         .', '| .', '|  .', '|   .', '|  .', '|     .', '|  .', '. |   ', '|    .']
   tall = random.randint(0, len(pongstr)-1)
   return pongstr[tall]

def randomReply():
   f = open('reply.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   reply = string.splitlines()
   tall = random.randint(0, len(reply)-1)
   string = reply[tall]
   return string

def youtube():
   f = open('youtube.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   reply = string.splitlines()
   tall = random.randint(0, len(reply)-1)
   string = reply[tall]
   return string

def smiley():
   smileys = random.choice((' :D', ' :)', ' :>', ' €:', ' ;*', '<3', 'HØHØ'))
   return smileys

def greet():
   f = open('greetings.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   greetings = string.splitlines()
   for i in range(0, len(greetings)):
      if (greetings[i] in message):
         return True
   return False

def filmz():
   f = open('film.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   filmerz = string.splitlines()
   for i in range(0, len(filmerz)):
      if (filmerz[i].lower() in message):
         return True
   return False

def filmReturn():
   f = open('film.txt', 'r+')
   thefilm = ''
   string = ''
   for linje in f:
      string+=linje
   filmerz = string.splitlines()
   for i in range(0, len(filmerz)):
      if (filmerz[i].lower() in message.lower()):
         thefilm = filmerz[i].lower()
         return thefilm
   return ''

def no():
   f = open('no.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   nei = string.splitlines()
   for i in range(0, len(nei)):
      if (nei[i] in message):
         return True
   return False

def meld():
   f = open('mld.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   mldd = string.splitlines()
   for i in range(0, len(mldd)):
      if (mldd[i] in message):
         return True
   return False

def calc(num1, num2, operator):
   if (operator == '*'):
      return num1*num2
   elif (operator == '+'):
      return num1+num2
   elif (operator == '-'):
      return num1-num2
   elif (operator == '/'):
      return num1/num2

def calculate(string):
   liste = []
   tall = []
   op = []
   operators = '*/-+'
   num = '1234567890'
   k = 0
   for i in range(0, len(string)):
      if string[i] not in num:
         if string[i] not in operators:
            send('Klarer ikke regne ut det der ass')
            return ''
         else:
            liste.append(string[k:i])
            op.append(string[i])
            k=i+1
   liste.append(string[k:])
   for i in range(0, len(liste)):
      tall.append(int(liste[i]))
   print tall
   print op
   summen = tall[0]
   for i in range(0, len(op)):
      summen = calc(summen, tall[i+1], op[i])
   print summen
   summenz = str(summen)
   send(['Kan det stemme at svaret er ' + summenz + '?', 'Hmm, jeg tror svaret er ' + summenz, 'Muligens ' + summenz, 'Er ikke sikkert ass. Sånn ca ' + summenz + ' kanskje?'][random.randint(0,3)])

def filmene():
   f = open('film.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   film = string.splitlines()
   for i in range(0, len(film)):
      if (film[i] in message):
         return True
   return False

def yes():
   f = open('yes.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   ja = string.splitlines()
   for i in range(0, len(ja)):
      if (ja[i] in message):
         return True
   return False

def yearInfo(year):
   string=""
   filehandle = urllib.urlopen("http://numbersapi.com/" + year + "/year")
   for lines in filehandle.readlines():
      string+=lines
   if ("Cannot GET" in string) or ("Invalid url" in string):
      send('Skriv inn et ordentlig årstall a')
   else:
      send(string)

def numberInfo(number):
   string=""
   filehandle = urllib.urlopen("http://numbersapi.com/" + number + "/math")
   for lines in filehandle.readlines():
      string+=lines
   if ("Cannot GET" in string) or ("Invalid url" in string):
      send('Skriv inn et ordentlig tall a')
   else:
      send(string)


def randomMath():
   string=""
   filehandle = urllib.urlopen("http://numbersapi.com/random/math")
   for lines in filehandle.readlines():
      string+=lines
   send(string)

def Commands():
   if (message == '!sjekketriks'):
      send(sjekketriks()+'\r\n')
   if ('!film' == message):
      send('Tilfeldig film: ' + film())
   if ('!dickfilm' == message):
      send('Tilfeldig film: ' + dickfilm())
   if ('!promille' == message):
      send('Kalkulerer promille.')
      sleep(0.2)
      send('Kalkulerer promille..')
      sleep(0.4)
      send('Din promille er: ' + str(round(random.uniform(1.02, 2.92), 3)))
   if ('!polet' in message):
      stengetidpolet()
   if ('!middag' == message):
      send(maat())

   if ('!beer' in message):
      beer()

   if ('!bruker' in message) and admins():
      for i in range(0, len(listOfUsers)):
         send(listOfUsers[i])

   if ('!drikke' == message):
      send(drikkee())

   if ('!commands' == message):
      mottaker = user;
      f = open('cmd.txt', 'r+')

      irc.send('NOTICE ' + mottaker +  ' :' + '      ***** KOMMANDOER ******' + '\r\n')

      nr = 1
      for linje in f:
         irc.send('NOTICE ' + mottaker + ' :' + str(nr) + ': ' + linje + '\r\n')
         nr=nr+1
         sleep(0.2)

def long(string):
   link = string[6:].strip()
   length = 3

   url = 'http://tidla.us/py/' 
   values = {'shorturl':link, 'length':length }
   data = urllib.urlencode(values)
   req = urllib2.Request(url,data)
   response = urllib2.urlopen(req)
   the_page = response.read()
   thepage = the_page.split(" ")[0]
   if (thepage != "<!DOCTYPE"):
      return thepage
   else:
      return "Ikke gyldig link, skløtte."

def randomUser():
   try:
      tallet = random.randint(0, len(listOfUsers)-1)
      return listOfUsers[tallet]
   except:
      return user

def ukenummer():
   filehandle = urllib.urlopen("http://ukenummer.no/json")
   json_data= urllib.urlopen("http://ukenummer.no/json")

   data = json.load(json_data)
   pprint(data)
   json_data.close()
   return "Uke " + data["weekno"] + " varer fra " + data["dates"]["fromdate"] + " til " + data["dates"]["todate"]

def weather():
   file = urllib2.urlopen('http://api.met.no/weatherapi/textforecast/1.5/?forecast=land;language=nb')
   #convert to string:
   data = file.read()
   #close file because we dont need it anymore:
   file.close()
   #parse the xml you downloaded
   dom = parseString(data)
   #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
   xmlTag = dom.getElementsByTagName('title')[0].toxml()
   #strip off the tag (<tag>data</tag>  --->   data):
   xmlData=xmlTag.replace('<title>','').replace('</title>','')
   #print out the xml tag and data in this format: <tag>data</tag>
   print xmlTag
   #just print the data
   send(xmlData)
   print xmlData

def randomGreet():
   greetings = ['hei', 'hallo', 'heisann', 'hej', 'hey', 'halla', 'hi', 'hola', 'yo']
   nr = random.randint(0, len(greetings)-1)
   string = greetings[nr]
   return string.strip()

def film():
   f = open('film.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   filmer = string.splitlines()
   nr = random.randint(0, len(filmer)-1)
   string = filmer[nr]
   return "\""+string+"\""

def dickfilm():
   if random.randint(1000,2000) == 1337:
      return "The twilight saga"
      
   f = open('film.txt', 'r+')
   string = ''
   string2 = ''
   for linje in f:
      if (' ' in linje):
         string+=linje
   filmer = string.splitlines()
   string = filmer[random.randint(0, len(filmer)-1)]
   words = string.split(' ')
   tall = random.randint(0, len(words)-1)
   if (words[tall] == 'The' or words[tall] == 'the'):
      tall=tall+1
   if (tall == 0 or words[tall][0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      if (words[tall][-1]=='s'):
         words[tall] = 'Dicks'
      else:
         words[tall] = 'Dick'
   else:
      if (words[tall][-1]=='s'):
         words[tall] = 'dicks'
      else:
         words[tall] = 'dick'
   for i in range(0, len(words)):
      string2+= words[i]
      if (i < len(words)-1):
         string2 += ' '
   return "\""+string2+"\""



def deopUser(username):
    irc.send('MODE ' + channel + ' -o ' + username + '\r\n')

def kickUser(username, melding):
   irc.send('KICK ' + channel + ' ' + username + " :" + melding + '\r\n')

def opUser(username):
	irc.send('MODE ' + channel + ' +o ' + username + '\r\n')

def halfopUser(username):
	irc.send('MODE ' + channel + ' +h ' + username + '\r\n')

def dehalfopUser(username):
	irc.send('MODE ' + channel + ' -h ' + username + '\r\n')


listOfUsers = {}

users = {
      'assios':{'quiz':0,'creds':0,'alltimequiz':0}, 
      'aleksanb':{'quiz':0,'creds':0,'alltimequiz':0}, 
      'torcm':{'quiz':0,'creds':0,'alltimequiz':0}, 
      'stiaje':{'quiz':0,'creds':0,'alltimequiz':0}, 
      'sigveseb':{'quiz':0,'creds':0,'alltimequiz':0}, 
      'chritv':{'quiz':0,'creds':0,'alltimequiz':0},
      'Oddweb':{'quiz':0,'creds':0,'alltimequiz':0},
      'kjetiaun':{'quiz':0,'creds':0,'alltimequiz':0},
      'juliejk':{'quiz':0,'creds':0,'alltimequiz':0},
      'julie':{'quiz':0,'creds':0,'alltimequiz':0},
      'Kronoz-':{'quiz':0,'creds':0,'alltimequiz':0},
      'fyllik19':{'quiz':0,'creds':0,'alltimequiz':0}
      }

users['test'] = {'quiz':0,'creds':0,'alltimequiz':0}

if ('!printquiz' in message):
   printQuiz(users)

dag = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lårdag", "Såndag"]
dagstatus = ["HATER DET!", "Lenge til helg :(", "OK dag.", "i morgon år det freedaaag!", "YAYY HELGGG", "zbduhiWHF", "Er sykt klein ass"]

samtaleLvl = 0
filmLevel = 0
pong = 0
mld=0
smallTalk = 0
finishedLoading = 0
while True:
   data = irc.recv(1024)
   msg = data.split(' ')
   message = ' '.join(msg[3:]).lower().strip()[1:]
   #Legger til en "kopi" av message uten lower, slik at man kan sende capslock-sensitive meldinger gjennom fyllebot
   fyllemessage = ' '.join(msg[3:]).strip()[1:]

   #Tar datoen hver gang:
   currentDate = str(datetime.datetime.now())

   user = msg[0].split("!")
   user = user[0].replace(":", "")
   if ("End of /NAMES list" in fyllemessage):
      finishedLoading = 1

   #Liste med brukere
   try:
      brukerliste = data.split('= ' + channel + ' ')[1]
      bruker2 = brukerliste.split(' ')
      fyllechatIndex = bruker2.index(':End')
      listOfUsers = bruker2[1:(fyllechatIndex-3)]
      for i in range(0, len(listOfUsers)):
         if (listOfUsers[i][0] == '@'):
            listOfUsers[i] = listOfUsers[i][1:]
      listOfUsers.remove('Q')
   except:
      pass

   def bursdag():
      f = open('bursdag.txt', 'r+')
      string = ''
      for linje in f:
         if (shlex.split(linje)[0][4:] == shlex.split(currentDate)[0][4:]):
            if (user == shlex.split(linje)[1]):
               send('GRATULERER MED DAGEN, ' + user + smiley())

   #Denne admins()-funksjonen skal flyttes over senere. Får feilmeldinge "user not defined" når den er plassert i egen fil...
   def admins():
      f = open('adminz.txt', 'r+')
      string = ''
      for linje in f:
         string+= linje
      admin = string.splitlines()
      for i in range(0, len(admin)):
         if (admin[i].lower() == user.lower()):
            return True
      return False



   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
   if data.find ( 'KICK' ) != -1:
      irc.send ( 'JOIN ' + channel + '\r\n' )

   if greet() and ('fyllebot' in message):
      send(randomGreet() + ', ' + user + smiley())
      smallTalk = 1
      brukerTalk = user
      continue

   if ('!youtube' in message):
      thisURL = youtube()
      try:
         send(urlTitle(thisURL) + ": ")
      except:
         pass
      send(thisURL)
      continue

   if ('http://' in message) and not (user == 'fyllebot') and (finishedLoading == 1):
      firstURL = str(returnURLs(message).strip())
      try:        
         tittelen = urlTitle(firstURL)
         if (tittelen == "Parallels Confixx"):
            send('Det der er ikke en gyldig webside ass')
         else:
            send(tittelen)
         continue
      except:
         pass

   #if (smallTalk == 1) and (user == brukerTalk):
   #   send(['jeg spiller pong, ' + user + ', der a? :D', 'Snart eksamen, JIPPI. Skjer der?', 'Skal vi spille pong, ' + user + '?'][random.randint(0,2)])
   #   smalltalk = 0

   if ('hi doggie' in message):
      send('\'The Room\' sucks!')

   if ('parently' in message) and ('app' not in message):
      send('Mente du APparently, Christian?')

   try:
      if (shlex.split(message)[0]=='!kick') and (admins()):
         (kickUser(shlex.split(message)[1],shlex.split(message)[2]))
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!adduser') and (admins()):
         listOfUsers.append(shlex.split(message)[1])
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!removeuser') and (admins()):
         listOfUsers.remove(shlex.split(message)[1])
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!kalkuler'):
            send(calculate(message[9:].replace(' ', '')))
   except:
      pass

   if (message[0:4] == '!msg' and admins()):
      send(fyllemessage[4:].strip())

   if ('!pong' in message):
      mottaker = user
      f = open('ponghead.txt', 'r+')
      for line in f:
         send(line)
         sleep(1.0)
      gameOver = 0
      sleep(0.2)
      send('Din tur! Sjekk http://bash.org/?9322 for regler! Du skyter mot venstre.')
      pong = 1

   if ('!imdb' in message):
      send(imdbInfo(message, 'score'))

   if ('!plot' in message):
      send(imdbInfo(message, 'plot'))

   try:
      if (shlex.split(message)[0]=='!op') and (admins()):
         opUser(shlex.split(message)[1])
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!deop') and (admins()):
         deopUser(shlex.split(message)[1])
   except:
      pass
   
   try:
      if (shlex.split(message)[0]=='!halfop') and (admins()):
         halfopUser(shlex.split(message)[1])
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!dehalfop') and (admins()):
         yodehalfopUser(shlex.split(message)[1])
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!år'):
         send(yearInfo(shlex.split(message)[1]))
   except:
      pass

   try:
      if (shlex.split(message)[0]=='!matte'):
         send(numberInfo(shlex.split(message)[1]))
   except:
      pass

   if ('!matte' == message):
      try:
         send(randomMath())
      except:
         pass

   if (pong==1) and ('.' in message) and ('|' in message) and ('fyllebot' not in user):
      if (message[0] != '.'):
         send('DU TAPTE! :D')
         gameOver = 1
         pong = 0
         sendPong= ''
      else:
         sendPong = randomPong()
         send(sendPong)
      if (sendPong == '. |   '):
         send('DU SLO MEG :( GRATULERER!')
         gameOver = 1
         pong = 0

   if ('!familydoctors' in message):
      langsetning()

   if ('bærsj' in message):
      send('Det skrives ikke med r, julie >:(')

   if (('wood' in message) and ('woodchuck' in message)):
      send('A woodchuck would chuck so much wood he wouldn\'t know how much wood he chucked.')

   if ('anyone really been far even as decided to use' in message):
      send ('what is this i don\'t even')

   if ('dad is' in message) and ('dead' or 'ded' in message):
      send('THEN WHO WAS PHONE?')

   if ('meaning of' in message and 'life' in message) or ('mening' in message and 'liv' in message):
      send (['41', '43'][random.randint(0,1)])

   if (('klokken' in message or 'klokka' in message) or ('tiden?' in message)):
      now = datetime.datetime.now() 
      tiden = now.strftime("%I:%M %p")
      send('Klokka er ' + tiden + '!')

   if ('!wiki' in message):
      send(wiki())   

   if ('!ukenummer' in message):
      send(ukenummer())

   if ('!fylla' in message) and (admins()):
      fylla()

   if (('hvilken' in message) and ('dag' in message)):
      today = datetime.date.today()
      day = today.weekday()
      send('Det er ' + dag[day] + ' i dag! ' + dagstatus[day])

   if ((('hvilken film' in message) or ('se film' in message) or (' film' in message and 'anbefal' in message) or (' film' in message and 'sett' in message) or ('hvilke film' in message)) and ('hva' not in message)):
      send('Har du sett filmen ' + film() + '?' + smiley())
      filmLevel=1
      continue

   if yes() and (filmLevel==1):
      send(['Den filmen er veldig bra, ikke sant?', 'DEN FILMEN ER HELT KONGE, RIGHT?!', 'Det er en av favorittfilmene mine ass. Likte du den?'][random.randint(0, 2)])
      message=" "
      filmLevel=2
      continue

   if yes() and (filmLevel==2):
      send(['Jeg likte den også', 'vil se den igjen ass, joinerru kino?'][random.randint(0,1)] + smiley())
      filmLevel=0
      continue

   if no() and (filmLevel==1):
      send(['Du burde se den ass!', 'Den er braaa, men du burde ikke se traileren. Inneholder massse spoilers. HATER SPOILERS'][random.randint(0,1)] + smiley())
      filmLevel=0
      continue

      #STARTQUIZ
   if ('!quiz' in message):
      quizLvl = 1
      sporsmal = getQuestions()
      svar = getAnswers()
      nummer = makeListOfNumbers(sporsmal, 10)

      for i in range(0, len(nummer)):
         count = i
         send("Spørsmål nr. " + str(i+1) + ": ")
         send(sporsmal[nummer[i]])
         while (count == i):
            data = irc.recv(1024)
            msg = data.split(' ')
            message = ' '.join(msg[3:]).lower().strip()[1:]
            user = msg[0].split("!")
            user = user[0].replace(":", "")
            print message
            for ans in svar[nummer[i]]:
               if (ans == message.strip()):
                  addPoints(user, 'quiz')
                  send(user + ' scorer! ' + user + ' har ' + str((users[user]['quiz'])) + ' poeng.')
                  count = count + 1
                  continue
               if (message == 'nxt'):
                  send(svar[nummer[i]][0])
                  count = count + 1
                  continue

      if (quizLvl == 1):
         send(getWinner(users))
         resetScore(users)
         quizLvl = 0

   '''if ("count" in message):
      try:
         count(message[6:len(message)])
      except:
         pass'''

   if ('!gjettelek' in message):
      gjett = 1
      count = 0
      guess = (random.randint(0, 1000))
      send('Gjett et tall mellom 0 og 1000')
      while (gjett == 1):
         data = irc.recv(1024)
         gjettemelding = ' '.join(data.split(' ')[3:]).lower().strip()[1:]
         if (gjettemelding.isdigit()):
            if (int(gjettemelding) != guess):
               count+=1
               if (count > 9):
                  send('For mange feilforsøk. Du tapte! :(')
                  gjett = 0
                  continue
               if int(gjettemelding) < guess:
                  send('For lavt. Prøv igjen!')
                  send(str(10 - count) + ' forsøk igjen.')
               elif int(gjettemelding) > guess:
                  send('For høyt. Prøv igjen!')
                  send(str(10 - count) + ' forsøk igjen.')
            else:
               send('Riktig! :D')
               gjett = 0
      
   if ("!vær" in message):
      weather()

   if ("!printquiz" in message):
      send(printQuiz(users))
      continue

   if ("!lastlink" in message):
      try:
         if ((len(lastUrls) == 5)):
            send('Siste 5 linker:')
         else:
            send('Siste linker:')
         for i in range(0, len(lastUrls)):
            send(lastUrls[i])
      except:
         pass

   if no() and (filmLevel==2):
      send(['WHATTHEFUCK? :C', 'Hadde tenkt å be deg med på kino, men IKKE Nå LENGER NEI >:C', 'hvafaaaen. hvilke filmer liker dua?:c', 'omfg, du suger.'][random.randint(0,3)])
      filmLevel=3
      message=''

   if (filmLevel==3) and (message!=''):
      send(['Fuck deg. FUCK DEG!', 'fu.', 'hater deg.'][random.randint(0,2)])
      filmLevel=0
      continue

   if ('fuck' in message) and ('fyllebot' in message):
      send('>:C')
      continue

   if (message=="ingen liker deg, fyllebot") or (message=='stikk a, fyllebot') and (admins()):
      irc.send ( 'PRIVMSG ' + channel + ' :ingen liker deg heller, ' + user + '\r\n' )
      
   bursdag()

   if ((message.endswith('fyllebot?')) and (len(message)>10)) and (not filmz()):
      send('ER DRITA :D')
      continue
   if (message=="sup fyllebot"):
      send(randomSupSvar())
      continue
   if ( 'slaps fyllebot' ) in message:
      send('WELL FUCK YOU.')

   if ('fyllebot' in message) and ('takk' in message):
      send(['care.', 'værsågod' + smiley(), 'np, ' + user, 'awww, ' + user + smiley()][random.randint(0,3)])
      continue

   if (message == 'fyllebot') or (message == 'fyllebot?'):
      send('ja?')
      brukerSvar = user;
      samtaleLvl = 1
      continue

   if ('hvem' in message) and ('er' in message):
      send(['Jeg vil snakke med ' + randomUser() + '!', 'Hvorfor er ikke ' + randomUser() + ' her?', 'Hvafaeeeeen. ' + randomUser() + '!?!?!'][random.randint(0, 2)])

   if (" " in message) and (samtaleLvl==1) and (user == brukerSvar):
      send(['HAHAH, du ass!', 'Hvor er ' + randomUser() + '?', 'fu.', 'hater deg ' + user + '.', 'elsker deg, ' + user, 'idiot ass, ' + user + smiley(), 'Skriv !kalkuler 2*3 for å få meg til å regne ut 2*3 :D', 'du må jo være drita da, ' + user + '.'][random.randint(0,6)])
      samtaleLvl=0
      brukerSvar = ""
      continue

   if ('fyllebot' in message) and (not greet()) and (not meld()) and not (user=="fyllebot"):
         send(randomReply())
         continue

   if ('hvor' in message):
	randomUser()

   try:
      if ('!long' in message):
         xmelding = ""
         if (long(message) != 'Ikke gyldig link, skløtte.'):
            xmelding = "Lang link: "
         send(xmelding + long(message))
         continue
   except:
      send('Er for full til å forlenge URLer atm :( Prøv igjen senere')

   if ("www." in message) and not (user == "fyllebot"):
      if (finishedLoading == 1):
         if (len(message) < 22):
            send('Ler jentene av URLen din fordi den er for kort? Prøv !long <URL>')
            continue

   try: 
      if 'JOIN' in msg[1] and ('fyllebot' not in user):
         listOfUsers.append(user)
         send(user + ' joina fyllechat! VELKOMMEN, ' + user)
   except:
      pass

   if ('pong' in message) and not (user == 'fyllebot'):
      send('Skriv !pong for å spille pong mot meg!' + smiley())
      continue

   try:
      if ('QUIT' in msg[1]) or ('PART' in msg[1]) and ('fyllebot' not in user):
         send('Hadet bra, ' + user + smiley())
         listOfUsers.remove(user)
   except:
      pass

   try:
      if ('NICK' in msg[1]):
         listOfUsers.remove(user)
         thisUser = msg[2][1:].strip()
         listOfUsers.append(thisUser)
         send('Bra navnevalg, ' +  thisUser + '!')
   except:
      pass

   try:
      if ('!matrise' in message or '!matrix' in message):
         array_multiplier(message)
   except:
      send('Faen ass ugyldie matrise ' + smiley())

   if (('neo' in message or 'agent smith' in message or 'matrix' in message or 'matrise' in message) and not ('!matrix' in message) and not ('!matrise' in message)):
      send('Skal jeg gange matrisa di? Prøv !matrise [matrix]*[matrix]'+smiley())

   #kræsjgreie
   if ('!kræsj' in message) and (user=="Assios"):
      send(jfriojfro)
   
   rhapsody()
   Commands()

   print data
