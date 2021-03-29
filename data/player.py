from random import randint
from .constants import MAT_X, MAT_Y, WIDTH

class Player:


    def __init__(self, player_name) -> None:

        # Initialize Player variables
        self.name = player_name
        self.score = 0
        self.held_letters = []
        self.nr_of_letters = 0

    def __str__(self) -> str:
        return f"{self.name}\nStig:{self.score}"

    def draw_letters(self, pouch):
        """Draw letters from the letter bag/pouch and to the player's rack"""

        # From the number of current held letters to the maximum
        for _ in range(self.nr_of_letters+1, 8):

            # If the pouch is empty break
            if not pouch:
                break

            # Get a random index from the pouch and pop the
            # letter at the given index. Then put it i the players
            # held letters
            j = randint(0, len(pouch)-1)
            letter = pouch.pop(j)
            self.held_letters.append(letter)

        self.nr_of_letters = len(self.held_letters)

        # Reposition letters on rack
        self.position_letters()

    
    def position_letters(self):
        """Repositions the letters on hand onto the player's rack"""

        # Make sure to iterate from 1 to 1+letters on hand so not to
        # multiply by zero later 
        for i in range(1, self.nr_of_letters + 1):
            letter = self.held_letters[i-1]

            # Put the letter onto the rack at given position
            letter.position = MAT_X + (WIDTH * i) + (i * 8), MAT_Y

    
    def switch_letters(self, pouch, letters_to_switch):
        """Switch a number of letters from the bag"""

        new_letters = []
        back_to_pouch = []

        # Get original letters by list comprehension for
        # the loop so not to iterate over the changing self.held_letters
        original_letters = [letter for letter in self.held_letters]

        # For each sprite in the held letters
        for sprite in original_letters:
            # If it maches a letter to be switched and if the pouch is
            # not empty
            if sprite.letter in letters_to_switch:
                if pouch:

                    # Then take a random index from the pouch and pop
                    # the element at that index
                    j = randint(0, len(pouch)-1)
                    pouch_letter = pouch.pop(j)

                    # Give the popped element the position of the element to switch
                    x, y = sprite.position
                    pouch_letter.position = x, y

                    # Then remove the element from the player's hand
                    letters_to_switch.remove(sprite.letter)
                    self.held_letters.remove(sprite)

                    # Add it to a list, later to be added to the pouch
                    back_to_pouch.append(sprite)

                    # And add the new letter both as a string to a list
                    # (to inform the user of the switch) and to the
                    # players held letters
                    new_letters.append(pouch_letter.letter)
                    self.held_letters.append(pouch_letter)

        # When all letters have been switched put the original player
        # letters into the bag. This makes sure that the letters are not
        # drawn again in the same turn.
        pouch.extend(back_to_pouch)
        
        return new_letters