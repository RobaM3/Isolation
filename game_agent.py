"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

import random
import math

class SearchTimeout(Exception):
	"""Subclass base exception for code clarity. """
	pass

def get_valid_moves(game,location):
	c,r = location
	directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
	valid_moves = [(c + dc,r + dr) for dr, dc in directions
                       if game.move_is_legal((c + dc,r + dr))]
	return valid_moves


def get_tree(game,player):
	tree = []
	blankSpaces = game.get_blank_spaces()
	for y,x in game.get_legal_moves(player):
		tree+=get_tree_again((y,x),blankSpaces,game)
	return tree

def get_tree_again(location,blankSpaces,game):
	currentLocM = []
	for move in get_valid_moves(game,location):
		if move in blankSpaces:
			currentLocM =[location]+ get_tree_again(move,[blank for blank in blankSpaces if move != blank],game)
	return currentLocM

def custom_score(game, player):
	"""Calculate the heuristic value of a game state from the point of view
	of the given player.
	This should be the best heuristic function for your project submission.
	Note: this function should be called from within a Player instance as
	`self.score()` -- you should not need to call this function directly.
	Parameters
	----------
	game : `isolation.Board`
		An instance of `isolation.Board` encoding the current state of the
		game (e.g., player locations and blocked cells).
	player : object
		A player instance in the current game (i.e., an object corresponding to
		one of the player objects `game.__player_1__` or `game.__player_2__`.)
	Returns
	-------
	float
		The heuristic value of the current game state to the specified player.
	"""

	if game.is_winner(player): return float("inf")
	if game.is_loser(player): return float("-inf")

	maxBlank = game.height * game.width
	leftBlankL = len(game.get_blank_spaces())

	#when the options of moves are various
	if leftBlankL > maxBlank*0.1: 
		return custom_score_2(game, player)
	else:
		myTree = get_tree(game,player)
		oppoTree = get_tree(game,game.get_opponent(player))

	return float(len(myTree) - len(oppoTree))


def custom_score_2(game, player):
	"""Calculate the heuristic value of a game state from the point of view
	of the given player.
	Note: this function should be called from within a Player instance as
	`self.score()` -- you should not need to call this function directly.
	Parameters
	----------
	game : `isolation.Board`
		An instance of `isolation.Board` encoding the current state of the
		game (e.g., player locations and blocked cells).
	player : object
		A player instance in the current game (i.e., an object corresponding to
		one of the player objects `game.__player_1__` or `game.__player_2__`.)
	Returns
	-------
	float
		The heuristic value of the current game state to the specified player.
	"""

	if game.is_winner(player): return float("inf")
	elif game.is_loser(player): return float("-inf")


	myScore, oppoScore = 0,0
	myMoves = game.get_legal_moves(player)
	oppoMoves = game.get_legal_moves(game.get_opponent(player))

	for move in myMoves:
		myScore+=len(get_valid_moves(game,move))

	for move in oppoMoves:
		oppoScore+=len(get_valid_moves(game,move))

	return float(myScore-oppoScore)

def custom_score_3(game, player):
	"""Calculate the heuristic value of a game state from the point of view
	of the given player.
	Note: this function should be called from within a Player instance as
	`self.score()` -- you should not need to call this function directly.
	Parameters
	----------
	game : `isolation.Board`
		An instance of `isolation.Board` encoding the current state of the
		game (e.g., player locations and blocked cells).
	player : object
		A player instance in the current game (i.e., an object corresponding to
		one of the player objects `game.__player_1__` or `game.__player_2__`.)
	Returns
	-------
	float
		The heuristic value of the current game state to the specified player.
	"""

	if game.is_loser(player): return float("-inf")
	if game.is_winner(player): return float("inf")

	myMoves = game.get_legal_moves(player)
	oppoMoves = game.get_legal_moves(game.get_opponent(player))
	myMovesL, oppoMovesL = len(myMoves), len(oppoMoves)
	playerH, playerW = game.get_player_location(player)
	boardH, boardW = game.height/2., game.width/2.
	equ = float(math.sqrt((boardH - playerH)**2 + (boardW - playerW)**2)) * 0.25
	return float(myMovesL-oppoMovesL) - equ
	

class IsolationPlayer:
	"""Base class for minimax and alphabeta agents -- this class is never
	constructed or tested directly.
	********************  DO NOT MODIFY THIS CLASS  ********************
	Parameters
	----------
	search_depth : int (optional)
		A strictly positive integer (i.e., 1, 2, 3,...) for the number of
		layers in the game tree to explore for fixed-depth search. (i.e., a
		depth of one (1) would only explore the immediate sucessors of the
		current state.)
	score_fn : callable (optional)
		A function to use for heuristic evaluation of game states.
	timeout : float (optional)
		Time remaining (in milliseconds) when search is aborted. Should be a
		positive value large enough to allow the function to return before the
		timer expires.
	"""
	def __init__(self, search_depth=3, score_fn=custom_score, timeout=20.):
		self.search_depth = search_depth
		self.score = score_fn
		self.time_left = None
		self.TIMER_THRESHOLD = timeout

	def terminal_test(self, game):
		if game.get_legal_moves():
			return False
		return True
	def time_left(self):
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
			return game.get_legal_moves()[0]


class MinimaxPlayer(IsolationPlayer):
	"""Game-playing agent that chooses a move using depth-limited minimax
	search. You must finish and test this player to make sure it properly uses
	minimax to return a good move before the search time limit expires.
	"""

	def get_move(self, game, time_left):
		"""Search for the best move from the available legal moves and return a
		result before the time limit expires.
		**************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
		For fixed-depth search, this function simply wraps the call to the
		minimax method, but this method provides a common interface for all
		Isolation agents, and you will replace it in the AlphaBetaPlayer with
		iterative deepening search.
		Parameters
		----------
		game : `isolation.Board`
			An instance of `isolation.Board` encoding the current state of the
			game (e.g., player locations and blocked cells).
		time_left : callable
			A function that returns the number of milliseconds left in the
			current turn. Returning with any less than 0 ms remaining forfeits
			the game.
		Returns
		-------
		(int, int)
			Board coordinates corresponding to a legal move; may return
			(-1, -1) if there are no available legal moves.
		"""
		

		self.time_left = time_left

		# Initialize the best move so that this function returns something
		# in case the search fails due to timeout
		moves = game.get_legal_moves()
		if not moves: return (-1,-1)
		best_move = game.get_legal_moves()[0]

		try:
			# The try/except block will automatically catch the exception
			# raised when the timer is about to expire.
			return self.minimax(game, self.search_depth)

		except SearchTimeout:
			return best_move  # Handle any actions required after timeout as needed

		# Return the best move from the last completed search iteration
		return best_move

	def max_value(self, game, depth):

		super().time_left()
		if self.terminal_test(game) or depth <= 0:
			return self.score(game, self)
		v = float("-inf")
		for move in game.get_legal_moves():
			v = max(v, self.min_value(game.forecast_move(move), depth-1))
		return v

	def min_value(self, game, depth):
		super().time_left()
		if self.terminal_test(game) or depth <= 0:
			return self.score(game, self)
		v = float("inf")
		for move in game.get_legal_moves():
			v = min(v, self.max_value(game.forecast_move(move), depth-1))
		return v

	def minimax(self, game, depth):
		"""Implement depth-limited minimax search algorithm as described in
		the lectures.
		This should be a modified version of MINIMAX-DECISION in the AIMA text.
		https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
		**********************************************************************
			You MAY add additional methods to this class, or define helper
				 functions to implement the required functionality.
		**********************************************************************
		Parameters
		----------
		game : isolation.Board
			An instance of the Isolation game `Board` class representing the
			current game state
		depth : int
			Depth is an integer representing the maximum number of plies to
			search in the game tree before aborting
		Returns
		-------
		(int, int)
			The board coordinates of the best move found in the current search;
			(-1, -1) if there are no legal moves
		Notes
		-----
			(1) You MUST use the `self.score()` method for board evaluation
				to pass the project tests; you cannot call any other evaluation
				function directly.
			(2) If you use any helper functions (e.g., as shown in the AIMA
				pseudocode) then you must copy the timer check into the top of
				each helper function or else your agent will timeout during
				testing.
		"""
		if depth<=0 and self.search_depth:
			depth = self.search_depth
		bestScore = float("-inf")
		bestMove =  game.get_legal_moves()[0]
		for move in game.get_legal_moves():
			v = self.min_value(game.forecast_move(move), depth-1)
			if v > bestScore:
				bestScore = v
				bestMove = move
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
		return bestMove
		

class AlphaBetaPlayer(IsolationPlayer):
	"""Game-playing agent that chooses a move using iterative deepening minimax
	search with alpha-beta pruning. You must finish and test this player to
	make sure it returns a good move before the search time limit expires.
	"""

	def get_move(self, game, time_left):
		"""Search for the best move from the available legal moves and return a
		result before the time limit expires.

		Modify the get_move() method from the MinimaxPlayer class to implement
		iterative deepening search instead of fixed-depth search.

		**********************************************************************
		NOTE: If time_left() < 0 when this function returns, the agent will
			  forfeit the game due to timeout. You must return _before_ the
			  timer reaches 0.
		**********************************************************************

		Parameters
		----------
		game : `isolation.Board`
			An instance of `isolation.Board` encoding the current state of the
			game (e.g., player locations and blocked cells).

		time_left : callable
			A function that returns the number of milliseconds left in the
			current turn. Returning with any less than 0 ms remaining forfeits
			the game.

		Returns
		-------
		(int, int)
			Board coordinates corresponding to a legal move; may return
			(-1, -1) if there are no available legal moves.
		"""
		self.time_left = time_left

		moves = game.get_legal_moves()
		if not moves: return (-1,-1)
		bestMove = game.get_legal_moves()[0]
		
		depth=1
		try:
			while 1:
				move = self.alphabeta(game, depth)
				if move == (-1,-1): break
				if move != (-1,-1): bestMove = move
				depth+=1

		except SearchTimeout:
			return bestMove  # Handle any actions required after timeout as needed

		return bestMove

	def alphabeta_min(self, game, depth, alpha=float("-inf"), beta=float("inf")):
		super().time_left()
		if self.terminal_test(game) or depth <= 0:
			return self.score(game, self)
		v1 = float("inf")
		for move in game.get_legal_moves():
			v2 = self.alphabeta_max(game.forecast_move(move),depth-1,alpha,beta)
			if v2<v1: v1=v2
			if v1<=alpha: break
			beta = min(v1,beta)
		return v1

	def alphabeta_max(self, game, depth, alpha=float("-inf"), beta=float("inf")):
		super().time_left()
		if self.terminal_test(game) or depth <= 0:
			return self.score(game, self)
		v1 = float("-inf")
		for move in game.get_legal_moves():
			v2 = self.alphabeta_min(game.forecast_move(move),depth-1,alpha,beta)
			if v2>v1: v1=v2
			if v1 >= beta: break
			alpha = max(v1,alpha)
		return v1

	def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
		"""Implement depth-limited minimax search with alpha-beta pruning as
		described in the lectures.

		This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
		https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

		**********************************************************************
			You MAY add additional methods to this class, or define helper
				 functions to implement the required functionality.
		**********************************************************************

		Parameters
		----------
		game : isolation.Board
			An instance of the Isolation game `Board` class representing the
			current game state

		depth : int
			Depth is an integer representing the maximum number of plies to
			search in the game tree before aborting

		alpha : float
			Alpha limits the lower bound of search on minimizing layers

		beta : float
			Beta limits the upper bound of search on maximizing layers

		Returns
		-------
		(int, int)
			The board coordinates of the best move found in the current search;
			(-1, -1) if there are no legal moves

		Notes
		-----
			(1) You MUST use the `self.score()` method for board evaluation
				to pass the project tests; you cannot call any other evaluation
				function directly.

			(2) If you use any helper functions (e.g., as shown in the AIMA
				pseudocode) then you must copy the timer check into the top of
				each helper function or else your agent will timeout during
				testing.
		"""
		if self.terminal_test(game) or depth <= 0:
			return self.score(game, self)
		if depth<=0 and self.search_depth:
			depth = self.search_depth
		bestScore = float("-inf")
		bestMove = game.get_legal_moves()[0]
		for move in game.get_legal_moves():
			v = self.alphabeta_min(game.forecast_move(move),depth-1,alpha,beta)
			if v>bestScore:
				bestScore = v
				bestMove = move
			if bestScore>=beta: break
			alpha = max(bestScore,alpha)
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
		return bestMove

