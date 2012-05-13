#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random

middag = {'laks': ['eburger', 'sitronmarinert -', 'egrandis', ' i fiskesuppe', 'vegetar-'], 'grandis':[''], 'burger':['tallerken', ' med cornflakes', 'kylling-'], 'kylling':[' og chips', ' og ris', 'gryte', 'vinger'], 'pyttipanne':['fløtegratinert -'], 'kebab':[' i pita', 'rulle-', 'vegetar-'], 'lasagne':['tysk -', 'fransk -'], 'spagetti':[' bolognaise', ' carbonara'], 'tomatsuppe':[' og biff', 'gratinert -'], 'taco':['mexikansk -', 'spansk -', 'svensk -'], 'pølse':['blod-','grise-','kjøtt-', ' og potetmos'], 'pannekaker':['bacon-',' med sirup'], 'shake':['protein-', 'kebab-']}
drikke = {'shots': ['jäger-', 'vodka-', 'minttu-', 'tequila-'], 'vin':['rød-', 'hvit-'], 'martini':['shaken -', 'stirred -', ', shaken, not stirred'], 'whiskey':['scottish -', 'irish -'], 'akevitt':['', 'jule-']}

def maat():
   hovedrett = middag.keys()
   retten = hovedrett[random.randint(0,len(hovedrett)-1)]
   tilbehor = middag[retten]
   tilbehoret = tilbehor[random.randint(0,len(tilbehor)-1)]
   mat = retten + tilbehoret
   if mat[-1]=='-':
      mat = tilbehoret.strip('-')+retten
   print('Du skal spise ' + mat)
   return('Du skal spise ' + mat)

def drikkee():
   hoveddrikke = drikke.keys()
   drikk = hoveddrikke[random.randint(0,len(hoveddrikke)-1)]
   drikketillegg = drikke[drikk]
   drikketillegget = drikketillegg[random.randint(0,len(drikketillegg)-1)]
   drikken = drikk+drikketillegget
   if drikken[-1]=='-':
      drikken = drikketillegget.strip('-')+drikk
   if drikken[-1]+drikken[-2]+drikken[-3] == 'sto':
      return('Drikk '+ str(random.randint(2,10))+ ' ' + drikken)
      #if drikken[0:3]=='teq':
      #   return('Husk salt og sitron a!')
   else:
      return('Drikk ' + drikken)