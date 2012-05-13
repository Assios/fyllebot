#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

def kickUser(username, melding):
   irc.send('KICK ' + " #fyllechat " + username + " :" + melding + '\r\n')

def opUser(username):
   irc.send('O ' + " #fyllechat " + username + '\r\n')