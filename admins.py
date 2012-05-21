#! /usr/bin/env python
# -*- coding: utf-8 -*-


def kickUsers(username, melding):
   return('KICK ' + " #fyllechat " + username + " :" + melding + '\r\n')

def opUser(username):
   return('O ' + " #fyllechat " + username + '\r\n')
