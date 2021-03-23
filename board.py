import numpy as np

SIZE = 15
BONUSES = {
    '3w': [(0,0),(0,7),(0,14),(7,0),(7,14),(14,0),(14,7),(14,14)],
    '2l': [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6)\
          ,(6,8),(6,12),(7,3),(7,11),(8,2),(8,6),(8,8),(8,12),(11,0),\
            (11,7),(11,14),(12,6),(12,8),(14,3),(14,11)],
    '2w': [(1,1),(1,13),(2,2),(2,12),(3,3),(3,11),(4,4),(4,10)\
          ,(10,4),(10,10),(11,3),(11,11),(12,2),(12,12),(13,1),(13,13)],
    '3l': [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)],
    '*': [(7,7)]
}

LETTERS = {
    "A": 1,
    "Á": 3,
    "B": 5,
    
}

class ScrabbleBoard:


    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2
        self.player_1_turn = True
        self.board = self._build_board()

    def __str__(self) -> str:
        return str(self.board)
    

    def _build_board(self):
        board = [["" for _ in range(SIZE)] for i in range(SIZE)]
        for bonus, locations in BONUSES.items():
            for cell in locations:
                board[cell[0]][cell[1]] = bonus

        return np.array(board)

if __name__ == '__main__':
    board = ScrabbleBoard(1,2)
    print(board)