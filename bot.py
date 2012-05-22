#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket, random, re, string, time, datetime, os, urllib, shlex, urllib2, json, math, time
import sys
import select
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

brett = [['  ']*8 for i in range(8)]
futuristic_board = [['  ']*8 for i in range(8)]
gameOver = False
piece_count = [16, 16]
moves = []
error_msg = ""
have_they_moved = [[False]*3 for i in range(2)]
last_computer_pos = [[0, 0] for i in range(2)]

def getPiece(y, x, board):
   if y<0 or y>7 or x<0 or x>7:
      return False
   return board[y][x]

def initBoard():
   global brett, gameOver, piece_count, have_they_moved, error_msg, last_computer_pos
   brett = [['   ']*8 for i in range(8)]
   brett[7] = ['bTO', 'bKN', 'bBI', 'bQU', 'bKI', 'bBI', 'bKN', 'bTO']
   brett[6] = ['bPA']*8
   brett[1] = ['wPA']*8
   brett[0] = ['wTO', 'wKN', 'wBI', 'wQU', 'wKI', 'wBI', 'wKN', 'wTO']
   piece_count = [16, 16]
   gameOver = False
   have_they_moved = [[False]*3 for i in range(2)]
   last_computer_pos = [[0,0] for i in range(2)]
   error_msg = ""

def printBoard():
   pieces = {'bKI':u"BK", 'bQU':u"BQ", 'bTO':u"BR", 'bBI':u"BB", 'bKN':u"BKN", 'bPA':u"BPA", 'wKI':u"WK", 'wQU':u"WQ", 'wTO':u"WR", 'wBI':u"WBI", 'wKN':u"WKN", 'wPA':u"WP"}
   os.system('clear')
   print "\n   / __\\ |__   ___ ___ ___ \n  / /  | '_ \\ / _ | __/ __|  White has",piece_count[0],"pieces\n / /___| | | |  __|__ \\__    Black has",piece_count[1],"pieces\n \\____/|_| |_|\\___|___/___/\n"
   print "| # | A | B | C | D | E | F | G | H | # |"
   print "-----------------------------------------"
   for i in range(7,-1,-1):
      outputString = "| "+str(i+1)
      for j in range(8):
         if brett[i][j] == '   ':
            outputString += " |  "
         else:
            outputString += " | " + pieces[brett[i][j]]
      print outputString + " | "+str(i+1)+" |"
      print "-----------------------------------------"
   print "| # | A | B | C | D | E | F | G | H | # |\n"


def verifyCastling(direction, current_player):
   global have_they_moved, brett, error_msg, futuristic_board
   row = 7 if current_player == 2 else 0
   destination = 7 if direction == 1 else 0
   piece = "w" if current_player == 1 else "b"
   piece += "KI"
   if have_they_moved[current_player-1][1] or have_they_moved[current_player-1][1+direction]:
      error_msg = "Someone has been moved before"
      return False
   
   if not areYouSafe(current_player):
      error_msg = "You are in check, you have to escape some other way"
      return False
   
   for i in range(4+direction,destination,direction):
      if brett[row][i].strip() == "":
         if math.fabs(i-4) < 3:
            futuristic_board = [x[:] for x in brett]
            movePiece([4,row, i,row], piece, 1)
            if not areYouSafe(current_player, 1):
               error_msg = "The road is under attack"
               return False
      else:
         return False
   movePiece([4, row, 4+2*direction, row], piece)
   movePiece([destination, row, 4+direction, row], piece[0]+"TO")
   return True
   
def verifyTowerMove(start, end):
   if start[0] != end[0] and start[1] == end[1]:
      clearPath = True
      diff = 1 if start[0]<end[0] else -1
      for i in range(start[0]+diff, end[0], diff):
         if brett[i][start[1]].strip() != '':
            clearPath = False
            break
      return clearPath
   elif start[0] == end[0] and start[1] != end[1]:
      clearPath = True
      diff = 1 if start[1]<end[1] else -1
      for i in range(start[1]+diff, end[1], diff):
         if brett[start[0]][i].strip() != '':
            clearPath = False
            break
      return clearPath
   else:
      return False

def verifyPawnMove(start, end, direction):
   if end[0]==start[0]+direction and (end[1]==start[1]+1 or end[1]==start[1]-1):
      if brett[end[0]][end[1]].strip() == '':
         return False
      return True
   elif end[0]==start[0]+2*direction and end[1]==start[1]:
      if start[0] != direction%7:
         return False
      if brett[start[0]+direction][start[1]].strip() != '' or brett[end[0]][end[1]].strip() != '':
         return False
      return True
   elif end[0]==start[0]+direction and end[1]==start[1]:
      if brett[end[0]][end[1]].strip() != '':
         return False
      return True
   return False

def verifyBishopMove(start, end):
   if math.fabs(end[0]-start[0]) == math.fabs(end[1]-start[1]):
      yDiff = 1 if start[0]<end[0] else -1
      xDiff = 1 if start[1]<end[1] else -1
      clearPath = True
      for i in range(1, int(math.fabs(end[0]-start[0]))):
         if brett[start[0]+yDiff*i][start[1]+xDiff*i].strip() != '':
            clearPath = False
            break
      return clearPath
   return False

def verifyKnightMove(start, end):
   if (start[0] == end[0]+2 or start[0] == end[0]-2) and (start[1] == end[1]+1 or start[1] == end[1]-1):
      return True
   if (start[0] == end[0]+1 or start[0] == end[0]-1) and (start[1] == end[1]+2 or start[1] == end[1]-2):
      return True
   return False

def verifyQueenMove(start, end):
   if math.fabs(end[0]-start[0]) == math.fabs(end[1]-start[1]):
      return verifyBishopMove(start, end)
   if start[1] == end[1] or start[0] == end[0]:
      return verifyTowerMove(start, end)
   return False

def verifyKingMove(start, end):
   if end[0]-start[0]<2 and end[0]-start[0]>-2 and end[1]-start[1]<2 and end[1]-start[1]>-2:
      return True
   return False
def adminMove(move):
   move = move.replace('-', '')
   move = list(move)
   move[0] = ord(move[0].lower())-97
   move[1] = int(move[1])-1
   move[2] = ord(move[2].lower())-97
   move[3] = int(move[3])-1
   piece = brett[move[1]][move[0]]
   
   movePiece(move, piece)
   return True
   
def verifyMove(move, player, just_checking = 0):
   global brett, futuristic_board, error_msg
   #print move
   if isinstance(move, str):
      move = move.replace('-', '')
      move = list(move)
      move[0] = ord(move[0].lower())-97
      move[1] = int(move[1])-1
      move[2] = ord(move[2].lower())-97
      move[3] = int(move[3])-1
   piece = brett[move[1]][move[0]]
   #print "This is you:", piece, "and you are standing at",chr(97+move[0])+str(move[1]+1), "trying to move to",chr(97+move[2])+str(move[3]+1)
   if (piece[0] == "b" and player == 1) or (piece[0] == "w" and player == 2) or piece.strip() == '':
      return False
   
   if (piece[0] == brett[move[3]][move[2]][0]):
      error_msg = "You are standing there already!"
      return False
   
   result = False
   direction = 1 if player == 1 else -1
   if piece[1:3] == "TO":
      result = verifyTowerMove([move[1],move[0]], [move[3], move[2]])
   elif piece[1:3] == "PA":
      result = verifyPawnMove([move[1],move[0]], [move[3], move[2]], direction)
   elif piece[1:3] == "BI":
      result = verifyBishopMove([move[1],move[0]], [move[3], move[2]])
   elif piece[1:3] == "KN":
      result = verifyKnightMove([move[1],move[0]], [move[3], move[2]])
   elif piece[1:3] == "QU":
      result = verifyQueenMove([move[1],move[0]], [move[3], move[2]])
   elif piece[1:3] == "KI":
      result = verifyKingMove([move[1],move[0]], [move[3], move[2]])    
   
   if result:
      futuristic_board = [x[:] for x in brett]
      movePiece(move, piece, 1)
      if not areYouSafe(player, 1):
         error_msg = "You can't do this. Suicide!"
         return False
      if just_checking != 1:
         movePiece(move, piece)
   else:
      error_msg = "You're not that kind of person."
   return result

def movePiece(moves, piece, just_checking = 0):
   global brett, futuristic_board, number_of_queens_computer, have_they_moved
   if just_checking == 0:
      board = brett[:]
   else:
      board = futuristic_board[:]
   pos = [moves[3], moves[2]]
   oldPos = [moves[1], moves[0]]
   global gameOver
   #pawn shall be converted to queen when it reaches the end
   if (pos[0] == 0 or pos[0] == 7) and piece[1:3] == "PA":
      piece = piece[0] + "QU"
   
   if just_checking == 0:
      #this is the part where I kill you
      if board[pos[0]][pos[1]][1:3] == "KI":
         gameOver = piece[0]
      
      # Count them pieces left
      if board[pos[0]][pos[1]].strip() != '':
         if board[pos[0]][pos[1]][0] == 'w':
            piece_count[0] -= 1
         else:
            piece_count[1] -= 1
      
      # Rokade
      player_index = 0 if piece[0] == "w" else 1
      if piece[1:3] == "TO" and oldPos[1] == 0 and (oldPos[0] == 0 or oldPos[0] == 7):
         have_they_moved[player_index][0] = True
      if piece[1:3] == "TO" and oldPos[1] == 7 and (oldPos[0] == 0 or oldPos[0] == 7):
         have_they_moved[player_index][2] = True
      if piece[1:3] == "KI" and oldPos[1] == 4 and (oldPos[0] == 0 or oldPos[0] == 7):
         have_they_moved[player_index][1] = True
   
   board[pos[0]][pos[1]] = piece
   board[oldPos[0]][oldPos[1]] = '   '

def areYouSafe(current_player, just_checking = 0, piece_to_check = "KI"):
   global brett, futuristic_board
   if just_checking == 0:
      board = brett[:]
   else:
      board = futuristic_board[:]
   if current_player == 1:
      color = "w"; anticolor = "b"
   else:
      color = "b"; anticolor = "w"
   if isinstance(piece_to_check, str):
      pos = [0,0]
      for i in range(8):
         for j in range(8):
            if board[i][j] == color+piece_to_check:
               pos = [i,j]
               break
   else:
      pos = piece_to_check
   
   direction = 1 if current_player == 1 else -1
   
   # Attacked by pawns?
   if getPiece(pos[0]+direction, pos[1]-1, board) == anticolor+"PA" or getPiece(pos[0]+direction, pos[1]+1, board) == anticolor+"PA":
      return False
   
   neighbors = [None]*4
   crossneighbors = [None]*4
   for i in range(8):
      # Attacked by towers or sideways queen?
      if i<pos[0] and board[i][pos[1]].strip() != '':
         neighbors[0] = board[i][pos[1]]
      if i>pos[0] and board[i][pos[1]].strip() != '' and neighbors[1] == None:
         neighbors[1] = board[i][pos[1]]
      if i<pos[1] and board[pos[0]][i].strip() != '':
         neighbors[2] = board[pos[0]][i]
      if i>pos[1] and board[pos[0]][i].strip() != '' and neighbors[3] == None:
         neighbors[3] = board[pos[0]][i]
      
      # Attacked by bishops or diagonal queens?
      if i<pos[0]:
         if pos[1]-(pos[0]-i)>=0 and board[i][pos[1]-(pos[0]-i)].strip() != '':
            crossneighbors[0] = board[i][pos[1]-(pos[0]-i)]
         if pos[1]+(pos[0]-i)<8 and board[i][pos[1]+(pos[0]-i)].strip() != '':
            crossneighbors[1] = board[i][pos[1]+(pos[0]-i)]
      if i>pos[0]:
         if pos[1]-(i-pos[0])>=0 and board[i][pos[1]-(i-pos[0])].strip() != '' and crossneighbors[2] == None:
            crossneighbors[2] = board[i][pos[1]-(i-pos[0])]
         if pos[1]+(i-pos[0])<8 and board[i][pos[1]+(i-pos[0])].strip() != '' and crossneighbors[3] == None:
            crossneighbors[3] = board[i][pos[1]+(i-pos[0])]
   if anticolor+"TO" in neighbors or anticolor+"QU" in neighbors:
      return False
   if anticolor+"BI" in crossneighbors or anticolor+"QU" in crossneighbors:
      return False
   
   # Attacked by knight?
   isitahorse = [None]*8
   isitahorse[0] = getPiece(pos[0]-2, pos[1]-1, board)
   isitahorse[1] = getPiece(pos[0]-2, pos[1]+1, board)
   isitahorse[2] = getPiece(pos[0]-1, pos[1]-2, board)
   isitahorse[3] = getPiece(pos[0]-1, pos[1]+2, board)
   isitahorse[4] = getPiece(pos[0]+1, pos[1]-2, board)
   isitahorse[5] = getPiece(pos[0]+1, pos[1]+2, board)
   isitahorse[6] = getPiece(pos[0]+2, pos[1]-1, board)
   isitahorse[7] = getPiece(pos[0]+2, pos[1]+1, board)
   if anticolor+"KN" in isitahorse:
      return False
   
   # Attacked by king?
   isitaking = [None]*8
   isitaking[0] = getPiece(pos[0]-1, pos[1]-1, board)
   isitaking[1] = getPiece(pos[0]-1, pos[1], board)
   isitaking[2] = getPiece(pos[0]-1, pos[1]+1, board)
   isitaking[3] = getPiece(pos[0], pos[1]-1, board)
   isitaking[4] = getPiece(pos[0], pos[1]+1, board)
   isitaking[5] = getPiece(pos[0]+1, pos[1]-1, board)
   isitaking[6] = getPiece(pos[0]+1, pos[1], board)
   isitaking[7] = getPiece(pos[0]+1, pos[1]+1, board)
   if anticolor+"KI" in isitaking:
      return False
   return True
      
def canYouMove(current_player):
   global futuristic_board
   color = "w" if current_player == 1 else "b"
   for i in range(8):
      for j in range(8):
         if brett[i][j][0] == color:
            for k in range(8):
               for l in range(8):
                  if l!=j or k!=i:
                     if verifyMove([j,i,l,k], current_player, 1):
                        return True
   return False

def bestComputerMove(current_player, combat = 0):
   global futuristic_board, brett, last_computer_pos
   bestMoveScore = -10000
   bestMove = []
   pieceCosts = {'PA':1, 'BI':3, 'KN':3, 'TO':5, 'QU':9, 'KI':100}
   if current_player == 1:
      color = "w"; anticolor = "b"
   else:
      color = "b"; anticolor = "w"
   for i in range(3,11):
      startCol = i%8
      for j in range(8):
         this_piece = brett[j][startCol]
         if this_piece[0] == color:
            for k in range(3,11):
               endCol = k%8
               #print k,"mod: ",endCol
               for l in range(8):
                  if l!=j or k!=i:
                     if not verifyMove([startCol,j,endCol,l], current_player, 1):
                        continue
                     if combat == 0:
                        thisMoveScore = 10
                     else:
                        thisMoveScore = random.randint(8,10)
#                    print [startCol,j,endCol,l]
                     
                     # Going in circles
                     if l == last_computer_pos[current_player-1][0] and endCol == last_computer_pos[current_player-1][1]:
                        thisMoveScore -= 1
                        
                     
                     # Please don't move the king
                     if brett[j][startCol][1:3] == "KI":
                        thisMoveScore -= 10
                     
                     # Killing another piece
                     if brett[l][endCol][0] == anticolor:
                        thisMoveScore += pieceCosts[brett[l][endCol][1:3]]
#                    print futuristic_board

                     # Are you safe now?
                     if not areYouSafe(current_player, 0, [j, startCol]):
                        thisMoveScore += pieceCosts[brett[j][startCol][1:3]]
                     # Are you safe afterwards?
                     if not areYouSafe(current_player, 1, [l, endCol]):
                        thisMoveScore -= pieceCosts[brett[j][startCol][1:3]]
                     else:
                        if not areYouSafe(1, 1):
                           thisMoveScore += 100
                     
                     # Maybe you should save some pieces better than yourself?                        
                     for m in range(8):
                        for n in range(8):
                           if brett[m][n][0] == color and pieceCosts[brett[m][n][1:3]] > pieceCosts[this_piece[1:3]]:
                              piece_safe_now = areYouSafe(current_player, 0, [m, n])
                              piece_safe_future = areYouSafe(current_player, 1, [m, n])
                              
                              if not piece_safe_now and piece_safe_future:
                                 thisMoveScore += pieceCosts[brett[m][n][1:3]]
                              if piece_safe_now and not piece_safe_future:
                                 thisMoveScore -= pieceCosts[brett[m][n][1:3]]
                                             
#                    print thisMoveScore
                     
                     if thisMoveScore > bestMoveScore:
                        bestMoveScore = thisMoveScore
                        bestMove = [startCol,j,endCol,l]
   last_computer_pos[current_player-1] = [bestMove[1], bestMove[0]]
   send(convertMoves(bestMove))
   return bestMove

def convertMoves(moveList):
   moveString = ''
   letters = 'ABCDEFGH'
   lettersR = 'HGFEDCBA'
   moveString+= letters[moveList[0]] + str(moveList[1]+1) + "-"
   moveString+= letters[moveList[2]] + str(moveList[3]+1)
   return moveString

                     
def gameLoop(mode = "computer"):
   global gameOver, moves, error_msg
   initBoard()
   current_player = 1
   while 1:
      error_msg = ""
      player_name = "White" if current_player == 1 else "Black"
      print player_name + " player's turn:"
      if mode == "computer" and current_player == 2:
         user_move = bestComputerMove(2)
         validMove = True
         time.sleep(0.7)
      elif mode == "combat":
         user_move = bestComputerMove(current_player, 1)
         validMove = True
         time.sleep(0.7)
      elif mode == "demo":
         user_move = moves.pop(0)
         validMove = True
         time.sleep(0.7)
      else:
         send('Trekk: ')
         user_move = message
         validMove = re.match("[A-Ha-h]{1}[1-8]{1}(-)[A-Ha-h]{1}[1-8]{1}", user_move)
         
      # Check and validate input, and move pieces
      if validMove != None and verifyMove(user_move, current_player):
         validMove = True
      elif user_move == "0-0" or user_move == "0-0-0":
         direction = 1 if user_move == "0-0" else -1
         if verifyCastling(direction, current_player):
            validMove = True
         else:
            validMove = False
      elif user_move == "exit":
         break
      elif user_move == "help":
         print "Type your move as A1-H8, where A1 marks the square of the piece you want to move, and H8 is where you want to go."
         print "To perform a castling, type 0-0 for kingside castling and 0-0-0 for queenside."
         print "Type exit to exit"
         continue
      else:
         if error_msg == "":
            error_msg = "Invalid input."
         validMove = False
      
      # Update board and switch players, or print error messages
      if validMove:
         current_player = current_player % 2 + 1
         if not areYouSafe(current_player):
            if not canYouMove(current_player):
               print "Game over, bro!"
               gameOver = True
            else:
               print "You are in check!"
      else:
         print error_msg
         print "Try again... (For help, type help)"
         error_msg = ""
      
      if gameOver != False:
         player_name = "Black" if current_player == 1 else "White"
         print player_name, "wins!"
         break
   mainMenu()

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
   mottaker = user
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

def smiley():
   smileys=[' :D', ' :)', ' :>', ' €:', ' ;*']
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

   if ('!pingall' in message):
      send(':'.join(listOfUsers))

   if ('!bruker' in message):
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

def randomUser():
   lengden = len(listOfUsers)-1
   tallet = random.randint(0, lengden)
   return string

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

def kickUser(username, melding):
   irc.send('KICK ' + " #fyllechat " + username + " :" + melding + '\r\n')

listOfUsers = []
today = datetime.date.today()
day = today.weekday()
dag = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lårdag", "Såndag"]
dagstatus = ["HATER DET!", "Lenge til helg :(", "OK dag.", "i morgon år det freedaaag!", "YAYY HELGGG", "zbduhiWHF", "Er sykt klein ass"]

samtaleLvl = 0
filmLevel = 0
pong = 0
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
      #fyllechatIndex = bruker2.index(':End')
      listOfUsers = bruker2[1:(#fyllechatIndex-3)]
      for i in range(0, len(listOfUsers)):
         if (listOfUsers[i][0] == '@'):
            listOfUsers[i] = listOfUsers[i][1:]
      listOfUsers.remove('Q')
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

   if greet() and ('fyllebot' in message):
      send(randomGreet() + ', ' + user + smiley())

   if ('hi doggie' in message):
      send('\'The Room\' sucks!')

   if ('parently' in message):
      send('Mente du APparently, Christian?')

   try:
      if (shlex.split(message)[0]=='!kick') and (admins()):
         (kickUser(shlex.split(message)[1],shlex.split(message)[2]))
   except:
      pass

   try:
      if (shlex.split(message)[0]== '!deleteFromUsers') and (admins()):
         (listOfUsers.remove(shlex.split(message)[1]))
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

   if ('!sjakk' in message):
      gameLoop()

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
      send('Er for full til å forlenge URLer atm :( Prøv igjen senere')
      continue

   if ('url' in message) or ("www." in message) and not (user == "fyllebot"):
      if (finishedLoading == 1):
         send('Ler jentene av URLen din fordi den er for kort? Prøv !long <URL>')

   if ("!random") in message:
      send(randomGreet() +  ", " +  randomUser() + smiley)

   try: 
      if 'JOIN' in msg[1] and ('fyllebot' not in user):
         listOfUsers.append(user)
         send(user + ' joina kanalen! VELKOMMEN ASS. Dagens film: http://www.youtube.com/watch?v=gRFJvRb4A9c')
   except:
      pass

   try:
      if ('QUIT' in msg[1]) or ('PART' in msg[1]) and ('fyllebot' not in user):
         send('Snakkes da, ' + user + smiley())
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

   #kræsjgreie
   if ('!kræsj' in message) and (user=="Assios"):
      send(jfriojfro)
   

   rhapsody()
   Commands()

   print data
