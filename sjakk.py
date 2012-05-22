#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, math, re, time, random
import sys
import select

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
#							print [startCol,j,endCol,l]
							
							# Going in circles
							if l == last_computer_pos[current_player-1][0] and endCol == last_computer_pos[current_player-1][1]:
								thisMoveScore -= 1
								
							
							# Please don't move the king
							if brett[j][startCol][1:3] == "KI":
								thisMoveScore -= 10
							
							# Killing another piece
							if brett[l][endCol][0] == anticolor:
								thisMoveScore += pieceCosts[brett[l][endCol][1:3]]
#							print futuristic_board

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
															
#							print thisMoveScore
							
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

def demoLoop():
	if loadFile():
		gameLoop("demo")
	else:
		mainMenu()



def loadFile():
	global moves
	try:
		theGame = open('immortal.txt', 'r')
	except IOError as e:
   		print 'Couldn\'t find the file immortal.txt. This is where the demo is stored.'
   		return False
	moves = theGame.readlines()
	for i in range(len(moves)-1):
		moves[i] = moves[i][0:len(moves[i])-1]
	return True

# Start the game
os.system('clear')
gameLoop()