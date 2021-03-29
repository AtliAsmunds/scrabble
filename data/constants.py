##############################################################
# This file is for the constants used in other scripts       #
# Most of them are self explanatory but others are described #
##############################################################

SCALE = 1.5
ROW_COUNT = COLUMN_COUNT = 15

# Width of tiles and letters
WIDTH = round(30 * SCALE)
HEIGHT = round(30 * SCALE)

GRID_MARGIN = 5
MARGIN = 50

# Space below board
PLAYER_SPACE = round(200)

# Space to the right of the board
INFO_SPACE = round(250)


BOARD_WIDTH = COLUMN_COUNT*(WIDTH+GRID_MARGIN)
BOARD_HEIGHT = ROW_COUNT*(HEIGHT+GRID_MARGIN)

# Mat/Rack measurments
MAT_X = MARGIN + (BOARD_WIDTH // 4)
MAT_Y = MARGIN * 1.5

LETTERS_ON_HAND = 7

SCREEN_WIDTH = round(BOARD_WIDTH)+INFO_SPACE
SCREEN_HEIGHT = round(BOARD_HEIGHT)+PLAYER_SPACE
SCREEN_TITLE = "SKRAFL"

# Button names with their coordinates
BUTTON_NAMES = {
    'check': (900, 200),
    'reset': (900, 850),
    'confirm': (900, 400),
    'draw': (900, 300),
    'pass': (900, 500)
}

#Bonuses and their coordinates
BONUSES = {
    '3w': [(0,0),(0,7),(0,14),(7,0),(7,14),(14,0),(14,7),(14,14)],
    '2l': [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6)\
          ,(6,8),(6,12),(7,3),(7,11),(8,2),(8,6),(8,8),(8,12),(11,0),\
            (11,7),(11,14),(12,6),(12,8),(14,3),(14,11)],
    '2w': [(1,1),(1,13),(2,2),(2,12),(3,3),(3,11),(4,4),(4,10)\
          ,(10,4),(10,10),(11,3),(11,11),(12,2),(12,12),(13,1),(13,13)],
    '3l': [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(9,1),(9,5),(9,9),(9,13),(13,5),(13,9)],
    'center': [(7,7)]
}

# Letters with their score value and amount in letter bag
LETTERS = {
    'A' : (1, 11),
    'Á' : (3,2),
    'B' : (5,1),
    'D' : (5,1),
    'Ð' : (2,4),
    'E' : (3,3),
    'É' : (7,1),
    'F' : (3,3),
    'G' : (3,3),
    'H' : (4,1),
    'I' : (1,7),
    'Í' : (4,1),
    'J' : (6,1),
    'K' : (2,4),
    'L' : (2,5),
    'M' : (2,3),
    'N' : (1,7),
    'O' : (5,1),
    'Ó' : (3,2),
    'P' : (5,1),
    'R' : (1,8),
    'S' : (1,7),
    'T' : (2,6),
    'U' : (2,6),
    'Ú' : (4,1),
    'V' : (5,1),
    'X' : (10,1),
    'Y' : (6,1),
    'Ý' : (5,1),
    'Þ' : (7,1),
    'Æ' : (4,2),
    'Ö' : (6,1),
    '0' : (0,2)
}