from random import randint
from constants import MAT_X, MAT_Y, WIDTH

class Player:


    def __init__(self, player_name) -> None:
        self.name = player_name
        self.score = 0
        self.held_letters = []
        self.nr_of_letters = 0

    def draw_letters(self, pouch):
        for i in range(self.nr_of_letters+1, 8):
            if not pouch:
                return
            j = randint(0, len(pouch)-1)
            letter = pouch.pop(j)
            self.held_letters.append(letter)
        self.nr_of_letters = len(self.held_letters)
        self.position_letters()

    
    def position_letters(self):
        for i in range(1, self.nr_of_letters + 1):
            letter = self.held_letters[i-1]
            letter.position = MAT_X + (WIDTH * i) + (i * 8), MAT_Y
    
    def switch_letters(self, pouch, letters_to_switch):
        original_letters = [letter for letter in self.held_letters]
        for sprite in original_letters:
            if sprite.letter in letters_to_switch:
                letters_to_switch.remove(sprite.letter)
                x, y = sprite.position
                self.held_letters.remove(sprite)
                j = randint(0, len(pouch)-1)
                pouch_letter = pouch.pop(j)
                pouch_letter.position = x, y
                self.held_letters.append(pouch_letter)
                pouch.append(sprite)