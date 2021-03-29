import numpy as np
from .constants import BONUSES

class Grid:

    def __init__(self, row, col, word_list) -> None:
        
        # Initialize class variables
        self.row = row
        self.col = col
        self.temp_letters = []  # List for temporory letter sprites 
        self.coordinate_list = []    # List for x,y coordinates
        self.word_list = word_list
        self.grid = []
        self.played_words = []
        self.temp_words = []    # List for temporary words on board (even non existant)
        self.first_play = True
        self.letters_on_board = 0

        # Populate the grid with None cells
        for row in range(self.row):
            self.grid.append([])
            for col in range(self.col):
                self.grid[row].append(None)
        
    def _set_tile_to_none(self, element, operation='remove'):
        """Iterates over the grid and sets the cell, which contains the given
        element, to None"""

        # If the given operation is to remove the element then subtract one
        # from the letter count. Other option is when a letter is moved on the
        # table, but not off it.
        if operation == 'remove':
            self.letters_on_board -= 1
        for row in range(self.row):
            for col in range(self.col):
                if self.grid[row][col] == element:
                    self.grid[row][col] = None


    def add_to_grid(self, x, y, element):
        """Add an element to the grid, also to the temp_letter list 
        and coordiante list"""

        self._set_tile_to_none(element, 'pre-append')
        self.grid[x][y] = element
        self.letters_on_board += 1
        self.temp_letters.append(element)
        self.coordinate_list.append((x,y))   # Append in a tuple

    
    def remove_from_grid(self, element):
        """Remove an element from the grid, also remove it from 
        the temp_letter list and coordinate list"""

        self._set_tile_to_none(element)
        if element in self.temp_letters:
            index = self.temp_letters.index(element)
            self.temp_letters.remove(element)
            self.coordinate_list.pop(index)


    def _is_aligned(self):
        """Checks if the temporary letters on the grid are aligned 
        horizontally or vertically, otherwise returns False"""

        # If there has nothing been added
        if not self.coordinate_list:
            return False

        # If there is only one element
        elif len(self.coordinate_list) == 1:
            return True

        horizontal = True
        vertical = True

        # Set the fundimental x,y coordinates for comparison
        x_0, y_0 = self.coordinate_list[0]

        # Then iterate over the other coordinates
        for x,y in self.coordinate_list:

            # If not aligned on the x axis
            if x != x_0:
                horizontal = False
            
            # If not aligned on the y axis
            if y != y_0:
                vertical = False

        return horizontal or vertical
    

    def _validate_words(self):
        """Check if new words on table exist in a given word list"""

        # Fill temp_words with newly played words (in form of sprites)
        self._filter_words()

        wrong_words = []
        
        # Get the letters from sprites to make word strings
        joined_words = ["".join([sprite.letter for sprite in word]) for word in self.temp_words]

        # Check if the newly played words exist
        for word in joined_words:
            if word not in self.word_list:
                wrong_words.append(word)
        
        return wrong_words
        

    def _check_first(self):
        """Check if first play is valid"""

        # If center is empty
        if self.grid[7][7] == None:
            return False

        # If a single letter is played, check if it exists
        if len(self.temp_letters) == 1:
            if self.temp_letters[0].letter in self.word_list:
                return True
            else:
                # Return the wrong "word"
                return [self.temp_letters[0].letter]


    def check(self):
        """Check if move to be played is valid on grounds of 
        word existing, words connecting and words being aligned 
        horizontally or vertically"""

        # Initialize a list for connection algorithm
        checked_list = []
        nr_connected = self._check_connected(7,7, checked_list)
        is_connected = nr_connected >= self.letters_on_board

        if not is_connected:
            return False
        
        # If first play is true, check validity of first play
        if self.first_play:
            first_check = self._check_first()
            if first_check != None:
                return first_check
        
        if not self._is_aligned():
            return False
        
        # Get wrong words, if any
        wrong_words = self._validate_words()
        if wrong_words:
            return wrong_words

        # If everything checks out the move is allowed
        return True

    def _get_words(self, grid, transposed=False):
        """Get words from each row and column of the grid"""

        # To get words from columns easily the grid is transposed
        if transposed:
            grid = np.array(grid).transpose()

        words = []

        # Iterate over rows (or columns)
        for row in grid:
            # For each row/column initialize a string (but really a list)
            string = []
            for letter in row:

                # When a None cell is found, append the string to the word list.
                # If there is only one letter in string skip that letter and clear
                # the string list (we don't need single letter words since it's
                # only possible to play them as a first move)
                if letter == None:
                    if len(string) > 1:
                        words.append(string)
                    string = []
                else:
                    string.append(letter)
            if len(string) > 1:
                words.append(string)
        
        # We then return the words list without the empty lists
        return [letter for letter in words if letter != []]


    def _filter_words(self):
        """Filters out already played words from the temporary words
        in play (words for the current move)"""

        words = self._get_words(self.grid)
        words.extend(self._get_words(self.grid, transposed=True))
        self.temp_words = words

        # Iterate over the already played words and remove
        # them from the temp_words until you only have the words
        # for the current move
        for word in self.played_words:
            if word in self.temp_words:
                self.temp_words.remove(word)


    def _calculate_bonus(self, score):
        """Calculate the bonus points, if any, for the played move"""

        # Get the temporary letters on the grid along with their coordinates 
        indexed_letters = list(zip(self.temp_letters, self.coordinate_list))
        bonus_score = 0
        
        # Iterate over each letter and its coordinates
        for letter, (x, y) in indexed_letters:
            
            # and modify the bonus score accordingly if the coordinates
            # match any of the bonus coordinates
            if (x, y) in BONUSES['3l']:
                bonus_score += letter.score * 2
            elif (x, y) in BONUSES['2l']:
                bonus_score += letter.score
            elif (x, y) in BONUSES['3w']:
                bonus_score = 2*score
            elif (x, y) in BONUSES['2w']:
                bonus_score = score
        
        # If the letters in play are 7 then apply the +50 bonus score
        if len(self.temp_letters) == 7:
            bonus_score += 50
        
        return bonus_score


    def play(self, player):
        """Play the current move. Adding score to player and clearing
        temporary lists"""

        # Add this moves words to played words
        self.played_words.extend(self.temp_words)

        score = 0

        if self.first_play:

            # For the first play we use the temp_letters and not temp_words
            # since temp_words does not allow one letter words
            words = [[letter for letter in self.temp_letters]]
            self.first_play = False

        else:
            words = self.temp_words

        # Iterate over each new word played and add the letters score
        # to the temporary score counter
        for word in words:
            for letter in word:
                score += letter.score

        bonus_score = self._calculate_bonus(score)

        # Then add bonus score to score counter and add
        # the sum to the current players score amount
        score += bonus_score
        player.score += score

        # Clear temorary lists for further use
        self.temp_words.clear()
        self.temp_letters.clear()
        self.coordinate_list.clear()
        
        return score



    def _check_connected(self, x, y, checked:list, banned_direction=None):
        """Recursive algorithm for counting connected letters on the grid.
        Takes in a list """

        # If the coordinates go out of the grid then return 0
        if (x >= self.row) or (x < 0) or (y >= self.col) or (y < 0):
            return 0

        # If there is no letter on the current coordinate or the coordinates
        # have been checked before return 0
        if (self.grid[x][y] == None) or ((x,y) in checked):
            return 0

        checked.append((x,y))

        # Check left letter
        left = self._check_connected(x,y-1, checked)

        # Check right letter
        right = self._check_connected(x,y+1,checked)

        # Check above letter
        up = self._check_connected(x-1,y,checked)

        # Check below letter
        down = self._check_connected(x+1,y,checked)


        return 1 + up + down + left + right

            

if __name__ == '__main__':
    pass

