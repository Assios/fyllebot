#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket, random, re, string, time, datetime, os, urllib, shlex, urllib2, json
from time import sleep
from pprint import pprint
from xml.dom.minidom import parseString


network = 'irc.quakenet.org'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 1024 )
irc.send ( 'NICK fyllebot\r\n' )
irc.send ( 'USER fyllebot fyllebot fyllebot :FylleBOOOT\r\n' )
irc.send ( 'JOIN #fyllechat\r\n' )
irc.send ( 'PRIVMSG #fyllechat :HEI ASS.\r\n' )

from imdb import *
from mat import *
from admins import *

dato = str(datetime.datetime.now())
aar = int(dato[0:4])
maaned = int(dato[5:7])
dag = int(dato[8:10])
dato = datetime.date(aar, maaned, dag)
polet = [17, 17, 17, 18, 18, 15, 10000]

def stengetidpolet():
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

def send(melding):
   irc.send ( 'PRIVMSG #fyllechat :' + melding + '\r\n' )
def privsend(melding):
   irc.send('PRIVMSG ' + user + ' :' + melding + '\r\n')

def randomSupSvar():
	nr = random.randint(0, 7)
	mld = ["Drikker tequila!", "Shotter vodka ass.", "Drikker rista martini. Ikke stirra", "leker batman. I'M BATMAN!", "NANANANANA BATMAAAN!", "LOLOLOLO SUPERMAAN!", "zzZZZzZZZZSOVNER ASS", "ssshhhhh, prøver å gjemme meg!"]
	return mld[nr]
 
def rhapsody():
   f = open('lyrics.txt', 'r+')
   string=''
   for linje in f:
    string+=linje
   lyrics = string.splitlines()
   for i in range(len(lyrics)):
      if (lyrics[i].lower() in message):
         irc.send ( 'PRIVMSG #fyllechat :'+lyrics[i+1]+'\r\n' )

def sjekketriks():
   f = open('sjekketriks.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   sjekketriks = string.splitlines()
   tall = random.randint(0, len(sjekketriks)-1)
   string = sjekketriks[tall]
   return string

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

def fylla():
   mottaker = user;
   f = open('fylla.txt', 'r+')
   for linje in f:
      send('   ' + linje)
      sleep(0.2)

def randomReply():
   f = open('reply.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   reply = string.splitlines()
   tall = random.randint(0, len(reply)-1)
   string = reply[tall]
   return string

def smiley():
   smileys=[' :D', ' :)', ' :>', ' €:', ';*']
   nr = random.randint(0, len(smileys)-1)
   return smileys[nr]

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

def Commands():
   if (message == '!sjekketriks'):
      send(sjekketriks()+'\r\n')
   if ('!film' == message):
      send('Tilfeldig film: ' + film())
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

def imdb(filmnavn):
   ting = filmnavn
   ting2 = ting[6:]
   filehandle = urllib.urlopen('http://www.imdbapi.com/?t=' + ting2)
   string=''
   for lines in filehandle.readlines():
      string+=lines
   stringen = string.split('imdbRating')[1][3:6]
   score = float(stringen)
   return(str(score))

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

today = datetime.date.today()
day = today.weekday()
dag = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lårdag", "Såndag"]
dagstatus = ["HATER DET!", "Lenge til helg :(", "OK dag.", "i morgon år det freedaaag!", "YAYY HELGGG", "zbduhiWHF", "Er sykt klein ass"]

samtaleLvl = 0
filmLevel = 0
mld=0
finishedLoading = 0
while True:
   data = irc.recv(1024)
   msg = data.split(' ')
   message = ' '.join(msg[3:]).lower().strip()[1:]
   #Legger til en "kopi" av message uten lower, slik at man kan sende capslock-sensitive meldinger gjennom fyllebot
   fyllemessage = ' '.join(msg[3:]).strip()[1:]

   user = msg[0].split("!")
   user = user[0].replace(":", "")
   if ("End of /NAMES list" in fyllemessage):
      finishedLoading = 1

   #Liste med brukere
   try:
      brukerliste = data.split('= #fyllechat ')[1]
      bruker2 = brukerliste.split(' ')
      fyllechatIndex = bruker2.index(':End')
      listOfUsers = bruker2[1:(fyllechatIndex-3)]
      listOfUsers.remove('@Q')
      for i in range(0, len(listOfUsers)):
         if (listOfUsers[i][0] == '@'):
            listOfUsers[i] = listOfUsers[i][1:]
   except:
      pass

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

   #Melding når folk joiner


   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
   if data.find ( 'KICK' ) != -1:
      irc.send ( 'JOIN #fyllechat\r\n' )

   if greet() and ('fyllebot' in message):
      send(randomGreet() + ', ' + user + smiley())

   if ('hi doggie' in message):
      send('\'The Room\' sucks!')

   if ('parently' in message):
      send('Mente du APparently, Christian?')

   try:
      if (shlex.split(message)[0]=='!kick') and (admins()):
         send(kickUser(shlex.split(message)[1],shlex.split(message)[2]))
   except:
      pass


   if (message[0:4] == '!msg' and admins()):
      send(fyllemessage[4:].strip())


   try:
      if ('!imdb' in message):
         send(imdbNavn(message))
   except:
      send('Lol, gidder ikke si no om den filmen asss')

   try:
      if (shlex.split(message)[0]=='!op') and (admins()):
         opUser(shlex.split(message)[1])
   except:
      pass

   if ('x78437c' in message):
      syng()

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

   if ('vår' in message):
      send('DET ER DRITFINT VåR I DAG. SOL N SHIT')

   if (('hvilken' in message) and ('dag' in message)):
      send('Det er ' + dag[day] + ' i dag! ' + dagstatus[day])

   if ((('hvilken film' in message) or ('se film' in message) or (' film' in message and 'anbefal' in message) or (' film' in message and 'sett' in message) or ('hvilke film' in message)) and ('hva' not in message)):
      send('Har du sett filmen ' + film() + '?' + smiley())
      filmLevel=1

   if yes() and (filmLevel==1):
      send(['Den filmen er veldig bra, ikke sant?', 'DEN FILMEN ER HELT KONGE, RIGHT?!', 'Det er en av favorittfilmene mine ass. Likte du den?'][random.randint(0, 2)])
      message=" "
      filmLevel=2

   if yes() and (filmLevel==2):
      send(['Jeg likte den også', 'vil se den igjen ass, joinerru kino?'][random.randint(0,1)] + smiley())
      filmLevel=0

   if no() and (filmLevel==1):
      send(['Du burde se den ass!', 'Den er braaa, men du burde ikke se traileren. Inneholder massse spoilers. HATER SPOILERS'][random.randint(0,1)] + smiley())
      filmLevel=0

   if ("count" in message):
      try:
         count(message[6:len(message)])
      except:
         pass

   if filmz() and ('!imdb' not in message):
      send(filmScore(filmReturn()))
      
   if ("!vær" in message):
      weather()

   if no() and (filmLevel==2):
      send(['WHATTHEFUCK? :C', 'Hadde tenkt å be deg med på kino, men IKKE Nå LENGER NEI >:C', 'hvafaaaen. hvilke filmer liker dua?:c', 'omfg, du suger.'][random.randint(0,3)])
      filmLevel=3
      message=''

   if (filmLevel==3) and (message!=''):
      send(['Fuck deg. FUCK DEG!', 'fu.', 'hater deg.'][random.randint(0,2)])
      filmLevel=0

   if ('fuck' in message) and ('fyllebot' in message):
      send('>:C')

   if (message=="ingen liker deg, fyllebot") or (message=='stikk a, fyllebot') and (admins()):
      irc.send ( 'PRIVMSG #fyllechat :ok FU!\r\n' )
      irc.send ( 'QUIT\r\n' )

   if ((message.endswith('fyllebot?')) and (len(message)>10)) and (not filmz()):
      send('ER DRITA :D')
   if (message=="sup fyllebot"):
      send(randomSupSvar())
   if ( 'slaps fyllebot' ) in message:
      send('WELL FUCK YOU.')

   if ('fyllebot' in message) and ('takk' in message):
      send(['care.', 'værsågod' + smiley(), 'np, ' + user, 'awww, ' + user + smiley()][random.randint(0,3)])

   if (message == 'fyllebot') or (message == 'fyllebot?'):
      send('ja?')
      brukerSvar = user;
      samtaleLvl = 1

   if (" " in message) and (samtaleLvl==1) and (user == brukerSvar):
      send(['HAHAH, du ass!', 'fu.', 'hater deg ' + user + '.', 'elsker deg, ' + user, 'idiot ass, ' + user + smiley(), 'du må jo være drita da, ' + user + '.'][random.randint(0,5)])
      samtaleLvl=0
      brukerSvar = ""

   if ('fyllebot' in message) and (not greet()) and (not meld()):
         send(randomReply())

   try:
      if ('!long' in message):
         xmelding = ""
         if (long(message) != 'Ikke gyldig link, skløtte.'):
            xmelding = "Lang link: "
         send(xmelding + long(message))
         continue
   except:
      pass

   if ('url' in message) or ("www." in message) and not (user == "fyllebot"):
      if (finishedLoading == 1):
         send('Ler jentene av URLen din fordi den er for kort? Prøv !long <URL>')

   if ("!bruker" in message):
      for i in range(0, len(listOfUsers)):
         send(listOfUsers[i])

   try: 
      if 'JOIN' in msg[1] and ('fyllebot' not in user):
         listOfUsers.append(user)
         send(user + ' joina kanalen! VELKOMMEN ASS')
   except:
      pass

   try:
      if ('QUIT' in msg[1]) or ('PART' in msg[1]) and ('fyllebot' not in user):
         send(user)
         listOfUsers.remove(user)
   except:
      pass

   try:
      if ('NICK' in msg[1]):
         listOfUsers.remove(user)
         listOfUsers.append(msg[2][1:])
         send(user + ' bytta til ' + msg[2][1:])
   except:
      pass

   #kræsjgreie
   if ('!kræsj' in message):
      send(jfriojfro)
   

   rhapsody()
   Commands()

   print data
