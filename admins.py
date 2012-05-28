#! /usr/bin/env python
# -*- coding: utf-8 -*-


def kickUsers(username, melding):
   return('KICK ' + " #fyllechat " + username + " :" + melding + '\r\n')

def opUser(username):
<<<<<<< HEAD
   irc.send('MODE ' + " #fyllechat +o " + username + '\r\n')
=======
   return('O ' + " #fyllechat " + username + '\r\n')
>>>>>>> 47e602c12bd00c85e708ff8a0a0e7c2ab650dc13
