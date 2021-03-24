import numpy as np


class Grid:

    def __init__(self, row, col, word_list) -> None:
        
        self.row = row
        self.col = col
        self.word = []
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
        self.grid[x][y] = element
        self.letters_on_board += 1
        self.word.append(element)
        self.index_list.append((x,y))
        # print([letter.letter for letter in self.word])
        # print(self.index_list)
    
    def remove_from_grid(self, element):
        for row in range(self.row):
            for col in range(self.col):
                if self.grid[row][col] == element:
                    self.grid[row][col] = None
                    self.letters_on_board -= 1
        if element in self.word:
            index = self.word.index(element)
            self.word.remove(element)
            self.index_list.pop(index)
        print("test now:")
        print([letter.letter for letter in self.word])
        print(self.index_list)

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

        print(self.temp_words)
        
        wrong_words = []
        for word in self.temp_words:
            if word not in self.word_list:
                wrong_words.append(word)
        
        return wrong_words
        



    def check(self):
        indexed_letters = list(zip(self.word, self.index_list))
        print("Indexed letters")
        print(indexed_letters)
        # if not self._is_no_space():
        #     return False

        if self.first_play:
            if self.grid[7][7] == None:
                print("First play must be on center")
                return False
        
        else:
            nr_connected = self._check_connected(7,7)
            if nr_connected < self.letters_on_board:
                print("Must connect to letters on board")
        
        if not self._is_aligned():
            print(False)
            return False
        
        wrong_words = self._validate_words()
        if wrong_words:
            print(wrong_words)
            return wrong_words

        return True




        # if self._is_aligned()[0]:
        #     string = ""
        #     hori_sorted = sorted(indexed_letters, key= lambda x : x[1][1]) # Sorted by alignment on x-axis
        #     print(hori_sorted)
        #     row_index, col_index = hori_sorted[0][1]
        #     row = self.grid[row_index]
        #     if col_index > 0:
        #         for i in row[col_index-1:0:-1]:
        #             if i == None:
        #                 break
        #             col_index -=1
            
        #     for i in row[col_index:]:
        #         if i == None:
        #             break
        #         string += str(i.letter)  # TODO: Muna að breyta í x.letter
            
        #     print(string)
        #     string_list.append(string)

        # if self._is_aligned()[1]:
        #     string = ""
        #     vert_sorted = sorted(indexed_letters, key = lambda x : x[1][0]) # Sorted by alignment on y-axis
        #     print(vert_sorted)
        #     row_index, col_index = vert_sorted[0][1]
        #     if row_index > 0:
        #         for i in self.grid[row_index-1:0:-1]:
        #             if i[col_index] == None:
        #                 break
        #             row_index -=1
            
        #     for i in self.grid[row_index:]:
        #         if i[col_index] == None:
        #             break
        #         string += i[col_index].letter  # TODO: Muna að breyta í x.letter
        #     print(string)
        #     string_list.append(string)
        # for string in string_list:
        #     if string in self.word_list:
        #         print("RÉTT")
        #     else:
        #         print('RANGT')

    def _check_words(self):         # TODO: Gera mögulegt að spila út einn staf í byrjun
        words = []
        for row in self.grid:
            string = ""
            for col in row:
                if col == None:
                    if len(string) > 1:
                        words.append(string)
                    string = ""
                else:
                    string += col.letter
        transposed = np.array(self.grid).transpose()

        for row in transposed:
            string = ""
            for col in row:
                if col == None:
                    if len(string) > 1:
                        words.append(string)
                    string = ""
                else:
                    string += col.letter
        words = [letter for letter in words if letter != '']

        return words
        
    def play(self):
        if self.check() == True:
            self.played_words.extend(self.temp_words)
            self.temp_words = []
            if self.first_play:
                self.first_play = False

        

    def _check_connected(self, x, y, banned_direction=None):
        if self.grid[x][y] == None:
            return 0
        if not banned_direction:
            left = self._check_connected(x,y-1, "right")
            right = self._check_connected(x,y+1, "left")
            up = self._check_connected(x-1,y, "down")
            down = self._check_connected(x+1,y, "up")
        if banned_direction == 'right':
            left = self._check_connected(x,y-1, "right")
            right = 0
            up = self._check_connected(x-1,y, "down")
            down = self._check_connected(x+1,y, "up")
        if banned_direction == 'left':
            left = 0
            right = self._check_connected(x,y+1, "left")
            up = self._check_connected(x-1,y, "down")
            down = self._check_connected(x+1,y, "up")
        if banned_direction == 'up':
            left = self._check_connected(x,y-1, "right")
            right = self._check_connected(x,y+1, "left")
            up = 0
            down = self._check_connected(x+1,y, "up")
        if banned_direction == 'down':
            left = self._check_connected(x,y-1, "right")
            right = self._check_connected(x,y+1, "left")
            up = self._check_connected(x-1,y, "down")
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

    print(grid._check_connected(7,7))