
class Grid:

    def __init__(self, row, col, word_list) -> None:
        
        self.row = row
        self.col = col
        self.word = []
        self.index_list = []
        self.word_list = word_list
        self.grid = []
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
        self.word.append(element)
        self.index_list.append((x,y))
        # print([letter.letter for letter in self.word])
        # print(self.index_list)
    
    def remove_from_grid(self, element):
        for row in range(self.row):
            for col in range(self.col):
                if self.grid[row][col] == element:
                    self.grid[row][col] = None
        if element in self.word:
            index = self.word.index(element)
            self.word.remove(element)
            self.index_list.pop(index)
        print("test now:")
        print([letter.letter for letter in self.word])
        print(self.index_list)

    def _is_aligned(self):
        if not self.index_list:
            return False, False
        horizontal = True
        vertical = True
        x_0, y_0 = self.index_list[0]
        for x,y in self.index_list:
            if x != x_0:
                horizontal = False
            if y != y_0:
                vertical = False
        
        print(horizontal, vertical)
        return horizontal, vertical
    
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
    
    def check(self):
        indexed_letters = list(zip(self.word, self.index_list))
        print(indexed_letters)
        if not self._is_no_space():
            return False

        string = ""
        if self._is_aligned()[0]:
            hori_sorted = sorted(indexed_letters, key= lambda x : x[1][1]) # Sorted by alignment on x-axis
            print(hori_sorted)
            row_index, col_index = hori_sorted[0][1]
            row = self.grid[row_index]
            if col_index > 0:
                for i in row[col_index-1:0:-1]:
                    if i == None:
                        break
                    col_index -=1
            
            for i in row[col_index:]:
                if i == None:
                    break
                string += str(i.letter)  # TODO: Muna að breyta í x.letter
            
            print(string)

        elif self._is_aligned()[1]:
            vert_sorted = sorted(indexed_letters, key = lambda x : x[1][0]) # Sorted by alignment on y-axis
            print(vert_sorted)
            row_index, col_index = vert_sorted[0][1]
            if row_index > 0:
                for i in self.grid[row_index-1:0:-1]:
                    if i[col_index] == None:
                        break
                    row_index -=1
            
            for i in self.grid[row_index:]:
                if i[col_index] == None:
                    break
                string += i[col_index].letter  # TODO: Muna að breyta í x.letter
            print(string)
        
        if string in self.word_list:
            print("RÉTT")
        else:
            print('RANGT')
        


def get_wordlist(file_name):
    with open(file_name, 'r') as f:
        word_set = [word.strip().upper() for word in f.readlines()]
        return word_set
            
        



if __name__ == '__main__':
    file_name = 'ordmyndir.txt'
    word_list = get_wordlist(file_name)

    grid = Grid(15,15, word_list)
    grid.add_to_grid(6,0,'I')
    grid.add_to_grid(4,0,'T')
    grid.add_to_grid(5,0,'L')
    grid.grid[3][0] = 'A'
    print(grid.check())