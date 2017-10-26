"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass



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
    # TODO: finish this function!
    #raise NotImplementedError
    #return float(len(game.get_legal_moves()))
    #If the move is to the edges, then we give the move less score. Otherwise higher score.

    edges=[
        [(0,i) for i in range (1,game.width-2)],
        [(i,0) for i in range(1,game.height-2)],
        [(game.width-1,i) for i in range(1,game.height-2)],
        [(i,game.height-1)for i in range(1,game.width-2)]
    ]
    corners=[(0,0),(0,game.height-1),(game.width-1,0),(game.width-1,game.height-1)]
    score=0.0
    score=len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player)))
    blanks = game.get_blank_spaces()

    for m in game.get_legal_moves():
        for x in edges:
            if m in x:
                score = score + 1
            else:
                score = score + 2
        if m in corners:
            score = score + .5

    own_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    for x in own_moves:
        for y in opponent_moves:
            if is_neighbour(x, y):
                score = score - 2
            else:
                score = score + 1

    return float(score)

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
    # TODO: finish this function!
    #    raise NotImplementedError
    # Check 2 level of moves to ensure that the opponent does not have moves which can block own moves.
    own_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    blanks = game.get_blank_spaces()
    #This is used to help determine opening/middle/end
    open_space_percent = (len(blanks)*100)/(game.height*game.width)

    score = 0.
    score = score + len(own_moves)-len(opponent_moves)
    if(open_space_percent>50):
        for x in own_moves:
            if x in opponent_moves:
                score = score +2

    elif(open_space_percent<50):
        for x in own_moves:
            game.forecast_move(x)
            own_next = game.get_legal_moves(player)
            for y in opponent_moves:
                game.forecast_move(y)
                opp_next=game.get_legal_moves(game.get_opponent(player))
                score = score + len(own_next)-len(opp_next)
    return score

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
    # TODO: finish this function!
    #raise NotImplementedError

    # This hueristic is used to determine if the opponent can pursue the player
    own_moves = game.get_legal_moves(player)
    opponent_moves=game.get_legal_moves(game.get_opponent(player))


    score = 0.
    for x in own_moves:
        for y in opponent_moves:
            if x==y:
                score = score + 2
            if is_neighbour(x,y):
                score=score-2
            else:
                score=score+1
    return score


def is_neighbour (own_move, opp_move):
    (ownX,ownY) = own_move
    (oppX,oppY)=opp_move
    if ownX==oppX:
        if ownY==oppY+1 or ownY== oppY-1:
            return True
    if ownY==oppY:
        if ownX==oppX+1 or ownX== oppX-1:
            return True
    return False

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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    best_move=(-1,-1)
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
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return self.best_move


    def max_value(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        #check if terminal state
        if(game.get_legal_moves()==0):
            return float("-inf")
        # check if the current depth is zero
        elif depth==0:
            return self.score(game,self)
        # call min_value
        else:

            score = float("-inf")
            for m in game.get_legal_moves():
                v = self.min_value(game.forecast_move(m),depth-1)
                if v>score:
                    score=v
            return score


    def min_value(self,game,depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # check if terminal state
        if (game.get_legal_moves() == 0):
            return float("inf")
        # check if the current depth is zero
        elif depth==0:
            return self.score(game,self)
        # call min_value
        else:

            score = float("inf")
            for m in game.get_legal_moves():
                v = self.max_value(game.forecast_move(m),depth-1)
                if v<score:
                    score=v
            return score

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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        #print("Player location: ", game.get_player_location(self))
        if (game.get_player_location(self) == None):
            # Implies the user has no position yet
            # (oppX, oppY) = game.get_player_location(game.get_opponent(self))
            (centerX, centerY) = (int(game.width / 2.0), int(game.height / 2.0))
            # print("center: ", (centerX, centerY))

            # print("Opposition: ", (oppX,oppY))

            # if (oppX, oppY) == None:
            # Implies I am the first player
            #    return (centerX, centerY)
            if game.move_is_legal((centerX, centerY)):
                return (centerX, centerY)
            else:
                return (centerX + 1, centerY + 1)

        else:
            score=float("-inf")
            for x in game.get_legal_moves():
                if depth==1:
                    v = self.score(game.forecast_move(x),self)
                else:
                    v = self.min_value(game.forecast_move(x),depth-1)
                if v>score:
                    score=v
                    self.best_move=x
            return self.best_move

        # TODO: finish this function!
        #raise NotImplementedError


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    best_move=(-1,-1)
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

        # TODO: finish this function!
        #raise NotImplementedError
        try:
            iter_depth=0
            #for i in range(0,self.search_depth):
            while(True):
                self.best_move = self.alphabeta(game,iter_depth)
                iter_depth = iter_depth + 1
        except SearchTimeout:
            pass
        return self.best_move



    def max_value(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #check if terminal node
        if len(game.get_legal_moves())==0:
            return float("-inf")

        #Check if depth is zero
        if(depth==0):
            return self.score(game,self)

        #Recursively call min_value
        else:
            v=float("-inf")
            for m in game.get_legal_moves():
                v = max(v,self.min_value(game.forecast_move(m),depth-1,alpha,beta))
                if v>=beta:
                    return v
                alpha=max(alpha,v)
            return v

    def min_value(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # check if terminal node
        if len(game.get_legal_moves()) == 0:
            return float("inf")

        # Check if depth is zero
        if depth == 0:

            return self.score(game, self)
        # Recursively call max_value
        else:
            v = float("inf")
            for m in game.get_legal_moves():
                v=min(v,self.max_value(game.forecast_move(m),depth-1,alpha,beta))
                if v<=alpha:
                    return v
                beta=min(beta,v)
            return v



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

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        move=(-1,-1)
        #if depth == 1:
        #    for x in game.get_legal_moves():
        #        v = self.score(game.forecast_move(x), self)
        #        if v>score:
        #            move=x
        #    return move




        if (game.get_player_location(self) == None):
            # Implies the user has no position yet
            #(oppX, oppY) = game.get_player_location(game.get_opponent(self))
            (centerX, centerY) = (int(game.width / 2.0), int(game.height / 2.0))
            #print("center: ", (centerX, centerY))

            #print("Opposition: ", (oppX,oppY))

            #if (oppX, oppY) == None:
                # Implies I am the first player
            #    return (centerX, centerY)
            if game.move_is_legal((centerX, centerY)):
                return (centerX, centerY)
            else:
                return (centerX + 1, centerY + 1)
        elif depth == 1:
            score = float("-inf")

            for x in game.get_legal_moves():
                v = self.score(game.forecast_move(x), self)

                if v>score:
                    score=v
                    move=x
            return move
        else:
            #v = float("-inf")

            for m in game.get_legal_moves():
                v = self.min_value(game.forecast_move(m),depth-1, alpha, beta)
                if v>alpha:
                    alpha=v
                    self.best_move=m
            return self.best_move



        # TODO: finish this function!
        #raise NotImplementedError