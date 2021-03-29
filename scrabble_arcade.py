# Code on github: https://github.com/AtliAsmunds/scrabble.git

import os
import arcade
from arcade.sprite_list import SpriteList
from tkinter import Tk

from data.sprites import *
from data.player import Player
from data.user_setup import UserSettings, BlankLetterSet, DrawLetterWindow
from data.grid import Grid
from data.constants import *



class MyGame(arcade.Window):

    def __init__(self, width, height, title, word_list):
        super().__init__(width, height, title)

        # Word list to validate words
        self.word_list = word_list

        # Initialize sprite lists as None (further initialization in setup())
        self.pouch = None
        self.tile_list = None
        self.letter_rack = None
        self.held_letter_position = None
        self.button_list = None
        self.table_temp = None
        self.table_perm = None

        # Start up window prompting for player names
        self.root = Tk()
        self.root.title('Player Settings')
        self.user_setup = UserSettings(self.root)
        self.root.mainloop()

        # Initailize player classes with given names
        self.players = [Player(name) for name in self.user_setup.player_names]\
                        if self.user_setup.player_names\
                        else [Player("Leikmaður 1"), Player("Leikmaður 2")]     # Or with presets if name window is closed



    
    def setup(self):

        # Booleans set for game status
        self.is_game_over = False
        self.turn_over = False

        # Set up list for held letter position
        self.held_letter_position = []

        # Set/reset integers
        self.pass_count = 0
        self.player_index = 0

        # Initialize Sprite Lists
        self.pouch = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()
        self.letter_rack = arcade.SpriteList()
        self.table_temp = arcade.SpriteList()
        self.table_perm = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.held_letter = arcade.SpriteList()


        # Some text variables initialized
        self.error_text = ""
        self.wrong_words_text = ""
        self.winner_text = ""

        # Background color set
        arcade.set_background_color(arcade.color.SAP_GREEN)

        # Populate the scrabble board, fill the letter pouch
        # and make the player mat
        self._make_scrabble_board()
        self._make_letters()
        self._make_buttons()
        self._make_mat()

        # Set/reset each player
        for player in self.players:
            player.held_letters = SpriteList()
            player.nr_of_letters = 0
            player.score = 0
            player.draw_letters(self.pouch)



    def _make_mat(self):
        """Create the player rack/mat for letters to be placed on"""

        for i in range(1, LETTERS_ON_HAND + 1):
            tile = BonusTile('mat', scale=SCALE)
            tile.position = MAT_X + (WIDTH * i) + (i * 8), MAT_Y
            self.letter_rack.append(tile)

    
    def _make_buttons(self):
        """Create clickable buttons"""
        for name, (x, y) in BUTTON_NAMES.items():
            button = Button(name)
            button.position = x, y
            self.button_list.append(button)


    def _make_letters(self):
        """Create each letter and put into the letter pouch"""
        for letter, (score, amount) in LETTERS.items():
            for _ in range(amount):
                letter_sprite = Letter(letter, score, scale=SCALE)
                self.pouch.append(letter_sprite)


    def _make_scrabble_board(self):
        """Create the scrabble board with Bonus tiles"""

        # Initalize the functional grid (underlying functionality
        # of the visible board initialized below)
        self.grid = Grid(ROW_COUNT, COLUMN_COUNT, self.word_list)

        # Iterate over the row/col count and but tiles in correct places
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if (row, column) in BONUSES['3w']:
                    self._make_tile(row, column, '3w')
                elif (row, column) in BONUSES['2w']:
                    self._make_tile(row, column, '2w')
                elif (row, column) in BONUSES['3l']:
                    self._make_tile(row, column, '3l')
                elif (row, column) in BONUSES['2l']:
                    self._make_tile(row, column, '2l')
                elif (row, column) in BONUSES['center']:
                    self._make_tile(row, column, 'center')
                else:
                    self._make_tile(row, column, 'blank')


    def _make_tile(self, x, y, key):
        """Create a tile on the board, given a coordinate and a key"""
        tile = BonusTile(key, x, y, SCALE)

        # Here the x,y coordinates are switched since the values passed in are rows and columns
        # In a matrix the row number corresponds to a y-axis and the column number to a x-axis
        # thus y=column is treated like x and vice versa.
        tile.position = ((GRID_MARGIN+HEIGHT) * y) + GRID_MARGIN + (HEIGHT // 2) + MARGIN,\
                        ((GRID_MARGIN+WIDTH) * (ROW_COUNT-1-x)) + GRID_MARGIN + (WIDTH // 2) + PLAYER_SPACE - MARGIN

        self.tile_list.append(tile)

        
    
    def on_draw(self):
        
        arcade.start_render()

        # Draw player scores onn screen, stored in each player instance
        for i, player in enumerate(self.players):
            arcade.draw_text(str(player), 900, 580 + (i * 60), arcade.color.YELLOW, 16, align='center', anchor_x='center', anchor_y='center')

        player = self.get_current_player()
        players_turn_text = f"{player.name} á leik"

        # Draw whose player's turn it is
        arcade.draw_text(players_turn_text, 450, 130, arcade.color.YELLOW, 20, align='center', anchor_x='center', anchor_y='center')


        # Draw all of the active Sprite lists
        self.letter_rack.draw()
        self.tile_list.draw()
        self.table_temp.draw()
        self.table_perm.draw()
        self.button_list.draw()
        player.held_letters.draw()
        self.held_letter.draw()

        # Draw all other text on screen (some text variables might be empty)
        arcade.draw_text(self.error_text, 800, 100, arcade.color.WHITE, 16, align='left', anchor_x='center', anchor_y='center')
        arcade.draw_text(self.winner_text, 800, 100, arcade.color.ANTI_FLASH_WHITE, 20, align='center', anchor_x='center', anchor_y='center')
        arcade.draw_text(self.wrong_words_text, 800, 100, arcade.color.WHITE, 16, align='left', anchor_x='center', anchor_y='center')


    def pull_to_top(self, letter, letter_class):
        """Pull the given letter to the top of the screen"""

        # Find the letters index in its given sprite list
        # and move the letter to the end of the list, making
        # it render last
        index = letter_class.index(letter)
        for i in range(index, len(letter_class) - 1):
            letter_class[i] = letter_class[i+1]
        letter_class[len(letter_class) - 1] = letter


    def _get_active_letters(self, player):
        """Combine all active letters, on rack and on board,
        into one sprite list"""

        active_letters = SpriteList()

        # In case, if a letter is in both held letters
        # and on the board, we only add it to the sprite list if
        # it isn't already there
        for sprite in player.held_letters:
            if sprite not in active_letters:
                active_letters.append(sprite)
        for sprite in self.table_temp:
            if sprite not in active_letters:
                active_letters.append(sprite)
        return active_letters


    def _hold_letter(self, player, letters):
        """Put selected letter in a sprite list for hold letters"""

        # We only want the top sprite in case we select more than one
        moved_letter = letters[-1]

        # Append that sprite and its coordinates to the approriate lists
        self.held_letter.append(moved_letter)
        self.held_letter_position = moved_letter.position

        # Pull the letter to the top of the appropriate sprite list
        if moved_letter in player.held_letters:
            self.pull_to_top(moved_letter, player.held_letters)
        else:
            self.pull_to_top(moved_letter, self.table_temp)

        # Remove the selected letter from original sprite list
        # but keeping the origin in a variable
        if moved_letter in player.held_letters:
            self.origin = player.held_letters
            player.held_letters.remove(moved_letter)
        elif moved_letter in self.table_temp:
            self.origin = self.table_temp
            self.table_temp.remove(moved_letter)


    def _select_letter(self, player:Player, x, y):
        """Select a letter from all active letters"""
        active_letters = self._get_active_letters(player)

        # If the turn is over it wont be possible to select a letter
        if not self.turn_over:

            # Get a letter at the x, y position given (from the mouse pointer)
            letters = arcade.get_sprites_at_point((x,y), active_letters)
            
            # If a letter got selected, grab that letter
            if len(letters) > 0:
                self._hold_letter(player, letters)
    

    def _press_check(self):
        """Show the appropriate information on screen for checking
        the validity of a word"""

        checked_results = self.grid.check()
        if checked_results == True:
            self.wrong_words_text = "Orð er til!"
        elif checked_results == False:
            self.error_text = "Enginn stafur er á borði\neða staðsetning þeirra\ner vitlaus."
        else:

            # self.grid.check() returns a list of wrong words 
            # if they are positioned correctly
            self.wrong_words_text = "Eftirfarandi orð eru\nekki til:\n{}".format("\n".join(checked_results))
    
    def _select_button(self, player, x, y):
        """Select a button for the given x,y coordinate (from the mouse)"""

        # Get the button at that coordinate, if any
        button = arcade.get_sprites_at_point((x,y), self.button_list)


        if len(button) > 0:
            if (button[0].name == 'reset'):
                self.setup()

            elif (button[0].name == 'check') and not self.is_game_over:
                self._press_check()

            elif (button[0].name == 'confirm') and not self.is_game_over:
                self.play_game(player)

            elif (button[0].name == 'draw') and not self.is_game_over:
                if not self.turn_over:
                    if not self.pouch:
                        self.error_text += "\nStafapoki er tómur"
                    else:
                        self._switch_letters(player)

            elif (button[0].name == 'pass') and not self.is_game_over:
                if not self.turn_over:
                    self.pass_count += 1
                    self.pass_turn(player)


    def pass_turn(self, player):
        """Pass the turn"""

        # Make a copy of the temporary letters on the board
        letters_in_play = [letter for letter in self.table_temp]

        # Remove each temporary letter on the board
        # and put it back onto the player rack and into
        # the held letter list
        for letter in letters_in_play:
            player.held_letters.append(letter)
            self.table_temp.remove(letter)
            self.grid.remove_from_grid(letter)
        player.position_letters()
        
        # If all players have passed twice then the game is over
        if self.pass_count >= 2 * len(self.players):
            self.game_over()
        self.turn_over = False
        self.player_index += 1

    def on_mouse_press(self, x, y, button, modifiers):

        # Reset text variables so they become "invisible"
        self.error_text = ""
        self.wrong_words_text = ""
        player = self.get_current_player()

        # Click on a button if any
        self._select_button(player, x, y)

        # Get letter if any
        if not self.is_game_over:
            self._select_letter(player, x, y)


    def get_current_player(self):
        """Returns the player whose turn is"""
        index = self.player_index % len(self.players)
        return self.players[index]


    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        # Move the hold letter
        for letter in self.held_letter:
            letter.center_x += dx
            letter.center_y += dy



    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        # Do nothing if no letter is being held
        if len(self.held_letter) == 0:
            return

        # Get all necessary information for letter placement
        held_letter = self.held_letter[0]
        player = self.get_current_player()
        player_letters = player.held_letters
        
        # Get the possible tiles for collion with the held letter
        tile, rack, rack_letter, table_letter, perm_letter = self._get_objects(held_letter, player_letters)

        # Bool for repositioning held letter to its original place
        reset_position = True
 
        # If the held letter collides with a letter on the rack it should
        # move back to its original position unless it is a temp letter on the board
        if arcade.check_for_collision(held_letter, rack_letter):
            reset_position = False if held_letter in self.table_temp else True
        
        # The held letter should move to its original location if it collides
        # with a temporary table letter
        elif self.table_temp and arcade.check_for_collision(held_letter, table_letter):
            reset_position = True

        # The held letter should move to its original location if it collides
        # with a permanent table letter
        elif self.table_perm and arcade.check_for_collision(held_letter, perm_letter):
            reset_position = True

        # If the held letter collides with an empty tile it should be placed there
        elif arcade.check_for_collision(held_letter, tile):                
            self._place_on_board(held_letter, tile)
            reset_position = False

        # If the held letter collides with an empty rack/map tile it should be placed there
        elif arcade.check_for_collision(held_letter, rack):
            self._place_on_rack(held_letter, player_letters, rack)
            reset_position = False

        # To reset the position its original position is restored
        # and appended to its original sprites list
        if reset_position:
                held_letter.position = self.held_letter_position
                self.origin.append(held_letter)

        self.held_letter.remove(held_letter)

    def _get_objects(self, held_letter, player_letters):
        """Get sprites for collision check"""

        # Initialize variables
        tile = None
        rack = None
        rack_letter = None
        table_letter = None
        perm_letter = None

        # If the held player letters are empty they are all on the table
        # thus the temporary table letters are used instead
        if not player_letters:
            player_letters = self.table_temp
        
        # Next line get the closest sprites for the held letter
        rack_letter = arcade.get_closest_sprite(held_letter, player_letters)[0]
        if self.table_temp:
            table_letter = arcade.get_closest_sprite(held_letter, self.table_temp)[0]
        if self.table_perm:
            perm_letter = arcade.get_closest_sprite(held_letter, self.table_perm)[0]
        tile = arcade.get_closest_sprite(held_letter, self.tile_list)[0]
        rack = arcade.get_closest_sprite(held_letter, self.letter_rack)[0]

        # We then return all of the closest sprites, if any
        return tile, rack, rack_letter, table_letter, perm_letter


    def _place_on_board(self, held_letter, tile):
        """Place a held letter onto a certain tile"""

        # Set the held letter position to the one of the tile
        held_letter.position = tile.center_x, tile.center_y

        # If the letters origin was on the table we must
        # remove it from the underlying grid before adding it again
        if held_letter in self.grid.temp_letters:
            self.grid.remove_from_grid(held_letter)

        # If the held letter is a blank letter, prompt
        # the player for a letter value
        if held_letter.score == 0:
            self._set_blank(held_letter)

        # Then finally we add it to the underlying grid
        self.grid.add_to_grid(tile.row, tile.col, held_letter)
        self.table_temp.append(held_letter)
    

    def _place_on_rack(self, held_letter, player_letters, rack):
        """Place a held letter onto the player rack/mat"""
        
        held_letter.position = rack.center_x, rack.center_y

        # Remove the held letter from the grid before putting
        # it back on hand
        self.grid.remove_from_grid(held_letter)
        player_letters.append(held_letter)


    def _set_blank(self, held_letter):
        """Set a blank letter tiles value"""

        # Initialize a window root and open a window
        # prompting for a letter value
        self.root = Tk()    
        self.user_setup = BlankLetterSet(self.root) 
        self.root.mainloop()

        # If a value vas given, set the blank value to that
        # else keep it as "0"
        applied_letter = self.user_setup.letter_val 
        held_letter.letter = applied_letter if applied_letter else '0'

    def play_letters(self, player):
        """Consolidate the temporary letters on the table"""

        # Put the temporary letters into the permanent letter sprite list
        self.table_perm.extend([sprite for sprite in self.table_temp])

        # Subtract the number of letters on hand by the amount played
        player.nr_of_letters -= len(self.table_temp)

        # Clear the temporary list, update the score and display
        # the added score amount
        self.table_temp = SpriteList()
        score = self.grid.play(player)      # Here the player's score is added
        self.error_text = f"+{score} stig"

    
    def play_game(self, player:Player):
        """Confirm the move about to be play and play it if possible"""
        checked_results = self.grid.check()

        # If letters were drawn instead of passing
        # or playing a word then it's the next players turn
        if self.turn_over:
            self.player_index += 1
            self.turn_over = False
            self.pass_count = 0

        # If the words played are correct
        elif checked_results == True:

            # The pass count is set to zero and the
            # letters are consolidated
            self.pass_count = 0
            self.play_letters(player)

            # Then the player draws new letters
            player.draw_letters(self.pouch)

            if not self.pouch:
                self.error_text += "\nStafapoki er tómur"

            # The game is over if the player has no letters
            # on hand and the pouch is empty
            if player.nr_of_letters == 0:
                self.game_over()

            # Otherwise it's the next players turn
            else:
                self.player_index += 1
                self.turn_over = False

        elif checked_results == False:
            self.error_text = "Enginn stafur er á borði\neða staðsetning þeirra\ner vitlaus."

        else:
            self.wrong_words_text = "Eftirfarandi orð eru\nekki til:\n{}".format("\n".join(checked_results))

    
    def game_over(self):
        """Shows the game's result for its game over statistics"""
        self.is_game_over = True

        # Subtract the letter scores from the players
        # that still have letters on hand
        for player in self.players:
            if player.nr_of_letters > 0:
                for letter in player.held_letters:
                    player.score -= letter.score

        # Set the first player as winner for comparison
        winner = [self.players[0]]

        # If a player has a higher score than the comparison
        # then that player is set.
        for player in self.players[1:]:
            if player.score > winner[0].score:
                winner = [player]

            # Otherwise if they are equal they are added to
            # the list, to make a draw possible
            elif player.score == winner[0].score:
                winner.append(player)
            

        if len(winner) > 1:
            winners = "\n".join(winner)
            self.error_text = ""
            self.winner_text = "Jafntefli!\n" + winners
        else:
            self.winner_text = f"{winner[0].name}\ner sigurvegari!"      



    
    def _switch_letters(self, player:Player):
        """Switch letters from the player's hand and the letter pouch"""

        # Open a prompt window
        self.root = Tk()
        self.draw_window = DrawLetterWindow(self.root, player.held_letters)
        self.root.mainloop()

        if self.draw_window.letters_to_switch:
            
            # If letters were selected we switch them
            new_letters = player.switch_letters(self.pouch, self.draw_window.letters_to_switch)
            if new_letters:
                self.error_text = f'Dregnir stafir\n{", ".join(new_letters)}'
            if not self.pouch:
                self.error_text += "\nStafapoki er tómur"
            
            # And then the turn is over
            self.player_index += 1
            self.turn_over = False
            



def get_wordlist(file_name):
    """Get a wordlist from a file"""

    with open(file_name, 'r', encoding='utf-8') as f:
        word_set = [word.strip().upper() for word in f.readlines()]
        return set(word_set)


def main():
    """This is the main program"""

    subdir = "data"
    file_name = 'ordmyndir.txt'
    path = os.path.join(subdir, file_name)
    word_list = get_wordlist(path)
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, word_list)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
