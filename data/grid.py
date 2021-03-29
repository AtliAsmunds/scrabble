import numpy as np
from .constants import BONUSES

class Grid:

    def __init__(self, row, col, word_list) -> None:
        
        self.row = row
        self.col = col
        self.temp_letters = []
        self.index_list = []
        self.word_list = word_list
        self.grid = []
        self.played_words = []
        self.temp_words = []
        self.first_play = True
        self.letters_on_board = 0

        for row in range(self.row):
            self.grid.append([])
            for col in range(self.col):
                self.grid[row].append(None)
        

    def add_to_grid(self, x, y, element):
        for row in range(self.row):
            for col in range(self.col):
                if self.grid[row][col] == element:
                    self.grid[row][col] = None
        # self.remove_from_grid(element)
        self.grid[x][y] = element
        self.letters_on_board += 1
        self.temp_letters.append(element)
        self.index_list.append((x,y))


    
    def remove_from_grid(self, element):
        for row in range(self.row):
            for col in range(self.col):
                if self.grid[row][col] == element:
                    self.grid[row][col] = None
                    self.letters_on_board -= 1
        if element in self.temp_letters:
            index = self.temp_letters.index(element)
            self.temp_letters.remove(element)
            self.index_list.pop(index)


    def _is_aligned(self):
        if not self.index_list:
            return False
        elif len(self.index_list) == 1:
            return True
        horizontal = True
        vertical = True
        x_0, y_0 = self.index_list[0]
        for x,y in self.index_list:
            if x != x_0:
                horizontal = False
            if y != y_0:
                vertical = False

        return horizontal or vertical
    
    # TODO: Finna leið til að tékka á báðum öxulum ef aðeins einn stafur er settur inn

    def _is_no_space(self):
        if self._is_aligned()[0]:  # Is horizontal
            sorted_index = sorted([y for x,y in self.index_list])
            x = self.index_list[0][0]
            y_0 = sorted_index[0]
            for y in sorted_index[1:]:
                if y != y_0+1:
                    if self.grid[x][y] == None:
                        return False
                y_0 = y
            return True
        
        elif self._is_aligned()[1]:  # Is vertical
            sorted_index = sorted([x for x,y in self.index_list])
            y = self.index_list[0][1]
            x_0 = sorted_index[0]
            for x in sorted_index[1:]:
                if x != x_0+1:
                    if self.grid[x][y] == None:
                        return False
                x_0 = x
            return True
        
        return False
    def _validate_words(self):
        self.temp_words = self._check_words()

        for word in self.played_words:
            if word in self.temp_words:
                self.temp_words.remove(word)


        
        wrong_words = []
        joined_words = ["".join([sprite.letter for sprite in word]) for word in self.temp_words]
        for word in joined_words:
            if word not in self.word_list:
                wrong_words.append(word)
        
        return wrong_words
        



    def check(self):
        indexed_letters = list(zip(self.temp_letters, self.index_list))


        # if not self._is_no_space():
        #     return False

        checked_list = []
        nr_connected = self._check_connected(7,7, checked_list)
        is_connected = nr_connected >= self.letters_on_board

        if not is_connected:
            return False

        if self.first_play:
            if self.grid[7][7] == None:

                return False
            if len(self.temp_letters) == 1:
                if self.temp_letters[0].letter in self.word_list:
                    return True
                else:
                    return [self.temp_letters[0].letter]

        
        if not self._is_aligned():

            return False
        
        wrong_words = self._validate_words()
        if wrong_words:

            return wrong_words

        return True



    def _check_words(self):         # TODO: Gera mögulegt að spila út einn staf í byrjun
        words = []
        for row in self.grid:
            string = []
            for letter in row:
                if letter == None:
                    if len(string) > 1:
                        words.append(string)
                    string = []
                else:
                    string.append(letter)
            words.append(string)
        transposed = np.array(self.grid).transpose()

        for row in transposed:
            string = []
            for letter in row:
                if letter == None:
                    if len(string) > 1:
                        words.append(string)
                    string = []
                else:
                    string.append(letter)
            words.append(string)
        words = [letter for letter in words if letter != []]


        return words
        
    def play(self, player):
        if self.check() == True:
            self.played_words.extend(self.temp_words)
            score = 0
            if self.first_play:
                words = [[letter for letter in self.temp_letters]]
            else:
                words = self.temp_words
            for word in words:
                for letter in word:
                    score += letter.score

            indexed_letters = list(zip(self.temp_letters, self.index_list))

            bonus_score = 0
            for letter, (x, y) in indexed_letters:
                
                if (x, y) in BONUSES['3l']:
                    bonus_score += letter.score * 2
                elif (x, y) in BONUSES['2l']:
                    bonus_score += letter.score
                elif (x, y) in BONUSES['3w']:
                    bonus_score = 2*score
                elif (x, y) in BONUSES['2w']:
                    bonus_score = score
            
            if len(self.temp_letters) == 7:
                bonus_score += 50

            score += bonus_score
            player.score += score




            self.temp_words.clear()
            self.temp_letters.clear()
            self.index_list.clear()
            if self.first_play:
                self.first_play = False
            
            return score


        

    def _check_connected(self, x, y, checked:list, banned_direction=None):
        if (x > 14) or (x < 0) or (y > 14) or (y < 0):
            return 0
        if (self.grid[x][y] == None) or ((x,y) in checked):
            return 0
        checked.append((x,y))
        if not banned_direction:
            left = self._check_connected(x,y-1, checked, "right")
            right = self._check_connected(x,y+1,checked , "left")
            up = self._check_connected(x-1,y,checked, "down")
            down = self._check_connected(x+1,y,checked, "up")
        if banned_direction == 'right':
            left = self._check_connected(x,y-1,checked, "right")
            right = 0
            up = self._check_connected(x-1,y,checked, "down")
            down = self._check_connected(x+1,y,checked, "up")
        if banned_direction == 'left':
            left = 0
            right = self._check_connected(x,y+1, checked, "left")
            up = self._check_connected(x-1,y, checked, "down")
            down = self._check_connected(x+1,y, checked, "up")
        if banned_direction == 'up':
            left = self._check_connected(x,y-1, checked, "right")
            right = self._check_connected(x,y+1, checked, "left")
            up = 0
            down = self._check_connected(x+1,y, checked, "up")
        if banned_direction == 'down':
            left = self._check_connected(x,y-1, checked, "right")
            right = self._check_connected(x,y+1, checked, "left")
            up = self._check_connected(x-1,y, checked, "down")
            down = 0
        return 1 + up + down + left + right

            


    
def get_wordlist(file_name):
    with open(file_name, 'r') as f:
        word_set = [word.strip().upper() for word in f.readlines()]
        return word_set
            
        



if __name__ == '__main__':
    file_name = 'ordmyndir.txt'
    word_list = get_wordlist(file_name)

    grid = Grid(15,15, word_list)
    grid.add_to_grid(7,7,'I')
    grid.add_to_grid(7,6,'T')

