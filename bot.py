#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import random
import re
import string
import time
import datetime
import os
import urllib
import shlex
from time import sleep

network = 'irc.quakenet.org'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 1024 )
irc.send ( 'NICK fyllebot\r\n' )
irc.send ( 'USER fyllebot fyllebot fyllebot :FylleBOOOT\r\n' )
irc.send ( 'JOIN #fyllechat\r\n' )
irc.send ( 'PRIVMSG #fyllechat :HEI ASS.\r\n' )

middag = {'laks': ['eburger', 'sitronmarinert -', 'egrandis', ' i fiskesuppe', 'vegetar-'], 'grandis':[''], 'burger':['tallerken', ' med cornflakes', 'kylling-'], 'kylling':[' og chips', ' og ris', 'gryte', 'vinger'], 'pyttipanne':['fløtegratinert -'], 'kebab':[' i pita', 'rulle-', 'vegetar-'], 'lasagne':['tysk -', 'fransk -'], 'spagetti':[' bolognaise', ' carbonara'], 'tomatsuppe':[' og biff', 'gratinert -'], 'taco':['mexikansk -', 'spansk -', 'svensk -'], 'pølse':['blod-','grise-','kjøtt-', ' og potetmos'], 'pannekaker':['bacon-',' med sirup'], 'shake':['protein-', 'kebab-']}
drikke = {'shots': ['jäger-', 'vodka-', 'minttu-', 'tequila-'], 'vin':['rød-', 'hvit-'], 'martini':['shaken -', 'stirred -', ', shaken, not stirred'], 'whiskey':['scottish -', 'irish -'], 'akevitt':['', 'jule-']}

dato = str(datetime.datetime.now())
aar = int(dato[0:4])
maaned = int(dato[5:7])
dag = int(dato[8:10])
dato = datetime.date(aar, maaned, dag)
polet = [17, 17, 17, 18, 18, 15, 10000]

def maat():
   hovedrett = middag.keys()
   retten = hovedrett[random.randint(0,len(hovedrett)-1)]
   tilbehor = middag[retten]
   tilbehoret = tilbehor[random.randint(0,len(tilbehor)-1)]
   mat = retten + tilbehoret
   if mat[-1]=='-':
      mat = tilbehoret.strip('-')+retten
   send('Du skal spise ' + mat)

def drikkee():
   hoveddrikke = drikke.keys()
   drikk = hoveddrikke[random.randint(0,len(hoveddrikke)-1)]
   drikketillegg = drikke[drikk]
   drikketillegget = drikketillegg[random.randint(0,len(drikketillegg)-1)]
   drikken = drikk+drikketillegget
   if drikken[-1]=='-':
      drikken = drikketillegget.strip('-')+drikk
   if drikken[-1]+drikken[-2]+drikken[-3] == 'sto':
      send('Drikk '+ str(random.randint(2,10))+ ' ' + drikken)
      if drikken[0:3]=='teq':
         send('Husk salt og sitron a!')
   else:
      send('Drikk ' + drikken)


def stengetidpolet():
    aapent = 1
    poltid = polet[dato.weekday()]
    tiden = str(datetime.datetime.now())
    timer = int(tiden[11:13])+1
    minutt = int(tiden[14:16])
    if (dato.weekday() >= 0) and (dato.weekday() <= 3):
        if timer<10:
            aapent = 0
            send('Polet er stengt. Aapner om ' + str(10-timer) + ' timer og ' + str(59-minutt) + ' min')
    elif (dato.weekday() == 4) or (dato.weekday() == 5):
        if timer<9:
            aapent = 0
            send('Polet er stengt. Aapner om ' + str(9-timer) + ' timer og ' + str(59-minutt) + ' min')
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

def imdben(filmnavn):
   filehandle = urllib.urlopen('http://www.imdbapi.com/?t=' + filmnavn)
   string=''
   for lines in filehandle.readlines():
      string+=lines
   stringen = string.split('imdbRating')[1][3:6]
   return int(round(float(stringen)))

def filmScore(filmen):
   score = ['Verste filmen ever!', 'FILMEN SUGER!!!', 'Veldig dårlig film!', 'OK film da...', 'Grei film..', 'Ganske bra film :)', 'Bra film ass!! :D', 'VELDIG BRA FILM!!!', 'En av de beste filmene jeg har sett! :O']
   send(score[imdben(filmen)-1])

def randomReply():
   f = open('reply.txt', 'r+')
   string = ''
   for linje in f:
      string+=linje
   reply = string.splitlines()
   tall = random.randint(0, len(reply)-1)
   string = reply[tall]
   return string

def send(melding):
   irc.send ( 'PRIVMSG #fyllechat :' + melding + '\r\n' )
def privsend(melding):
   irc.send('PRIVMSG ' + user + ' :' + melding + '\r\n')
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
      if (filmerz[i].lower() in message):
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

def admins():
   f = open('admins.txt', 'r+')
   string = ''
   for linje in f:
      string+= linje
   admin = string.splitlines()
   for i in range(0, len(admin)):
      if (admin[i].lower() == user.lower()):
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
      maat()

   if ('!drikke' == message):
      drikkee()

   if ('!commands' == message):
      mottaker = user;
      f = open('cmd.txt', 'r+')

      irc.send('NOTICE ' + mottaker +  ' :' + '      ***** KOMMANDOER ******' + '\r\n')

      nr = 1
      for linje in f:
         irc.send('NOTICE ' + mottaker + ' :' + str(nr) + ': ' + linje + '\r\n')
         nr=nr+1
         sleep(0.2)


def kickUser(username, melding):
   irc.send('KICK ' + " #fyllechat " + username + " :" + melding + '\r\n')

def opUser(username):
   irc.send('OP ' + " #fyllechat " + username + '\r\n')

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
dag = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
dagstatus = ["HATER DET!", "Lenge til helg :(", "OK dag.", "i morgon är det freedaaag!", "YAYY HELGGG", "zbduhiWHF", "Er sykt klein ass"]

filmLevel = 0
mld=0

while True:
   data = irc.recv(1024)
   msg = data.split(' ')
   mess = ' '.join(msg[3:])
   messa = mess.lower()
   messag = messa.strip()
   message = messag[1:]

   user = msg[0].split("!")
   user = user[0].replace(":", "")

   #Melding når folk joiner
   try: 
      if msg[1] == 'JOIN' and ('fyllebot' not in user):
         send(user + ' joina kanalen! VELKOMMEN ASS')
   except:
      pass

   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
   if data.find ( 'KICK' ) != -1:
      irc.send ( 'JOIN #fyllechat\r\n' )

   if greet() and ('fyllebot' in message):
      send(randomGreet() + ', ' + user + smiley())

   if ('hi doggie' in message):
      send('\'The Room\' sucks!')

   if ('parently' in message):
      send('Mente du APparently?')

   try:
      if (shlex.split(message)[0]=='!kick') and (admins()):
         kickUser(shlex.split(message)[1],shlex.split(message)[2])
   except:
      pass

   try:
      if ('!imdb' in message):
         send('Score: ' + imdb(message))
   except:
      send('Lol, gidder ikke si no om den filmen asss')

   try:
      if (shlex.split(message)[0]=='!op') and (admins()):
         opUser(shlex.split(message)[1])
   except:
      pass

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

   if ('vær' in message):
      send('DET ER DRITFINT VÆR I DAG. SOL N SHIT')

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



   if filmz() and ('!imdb' not in message):
      filmScore(filmReturn())
      

   if no() and (filmLevel==2):
      send(['WHATTHEFUCK? :C', 'Hadde tenkt å be deg med på kino, men IKKE NÅ LENGER NEI >:C', 'hvafaaaen. hvilke filmer liker dua?:c', 'omfg, du suger.'][random.randint(0,3)])
      filmLevel=3
      message=''

   if (filmLevel==3) and (message!=''):
      send(['Fuck deg. FUCK DEG!', 'fu.', 'hater deg.'][random.randint(0,2)])
      filmLevel=0

   if ('fuck' in message) and ('fyllebot' in message):
      send('>:C')

   if (message=="ingen liker deg, fyllebot") or (message=='stikk a, fyllebot'):
      irc.send ( 'PRIVMSG #fyllechat :ok FU!\r\n' )
      irc.send ( 'QUIT\r\n' )

   if ((message.endswith('fyllebot?')) and (len(message)>10)):
      send('ER DRITA :D')
   if (message=="sup fyllebot"):
      send(randomSupSvar())
   if ( 'slaps fyllebot' ) in message:
      send('WELL FUCK YOU.')

   if (message == 'fyllebot') or (message == 'fyllebot?'):
      send('ja?')

   if ('fyllebot' in message) and (not greet()) and (not meld()):
         send(randomReply())


   rhapsody()
   Commands()

   print data