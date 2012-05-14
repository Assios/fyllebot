#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

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

def imdbNavn(filmnavn):
   fulltnavn = ''
   ting = filmnavn
   ting2 = ting[6:]
   filehandle = urllib.urlopen('http://www.imdbapi.com/?t=' + ting2)
   string=''
   for lines in filehandle.readlines():
      string+=lines
   stringen = string.split('imdbRating')[1][3:6]
   score = str(float(stringen))
   fulltnavn = string.split('Title')[1].split(',', 1)[0][2:]
   aar = string.split('Year')[1].split(',', 1)[0][3:7]
   return('Filmen ' + fulltnavn + ' fra ' + aar + ' har scoren ' + score)

def imdben(filmnavn):
   filehandle = urllib.urlopen('http://www.imdbapi.com/?t=' + filmnavn)
   string=''
   for lines in filehandle.readlines():
      string+=lines
   stringen = string.split('imdbRating')[1][3]
   return int(stringen)

def filmScore(filmen):
   score = ['Verste filmen ever!', 'FILMEN SUGER!!!', 'Veldig dårlig film!', 'OK film da...', 'Grei film..', 'Ganske bra film :)', 'Bra film ass!! :D', 'VELDIG BRA FILM!!!', 'En av de beste filmene jeg har sett! :O']
   return(score[imdben(filmen)-1])
