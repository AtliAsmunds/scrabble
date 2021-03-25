from tkinter import Tk
import arcade

from arcade.sprite_list import SpriteList
from sprites import *
from player import Player
from user_setup import UserSettings, BlankLetterSet, DrawLetterWindow
from grid import Grid
from random import randint
from constants import *



class MyGame(arcade.Window):

    def __init__(self, width, height, title, word_list):
        super().__init__(width, height, title)

        self.word_list = word_list
        self.pouch = None
        self.tile_list = None
        self.letter_rack = None
        self.held_letters = None
        self.held_letter_position = None
        self.button_list = None
        self.table_temp = None
        self.table_perm = None
        self.turn_over = False
        self.root = Tk()
        self.root.title('Player Settings')
        self.user_setup = UserSettings(self.root)
        self.root.mainloop()
        self.player_1_name = self.user_setup.player_1 if self.user_setup.player_1 is not None else "Leikmaður 1"
        self.player_2_name = self.user_setup.player_2 if self.user_setup.player_2 is not None else "Leikmaður 2"
        self.player_1 = Player(self.player_1_name)
        self.player_2 = Player(self.player_2_name)
        print(self.player_1.name)
        print(self.player_2.name)





    def _make_tile(self, x, y, key):
        tile = BonusTile(key, x, y, SCALE)
        tile.position = (GRID_MARGIN+HEIGHT) * y + GRID_MARGIN + HEIGHT // 2 + MARGIN,\
                        ((GRID_MARGIN+WIDTH) * (ROW_COUNT-1-x) + GRID_MARGIN + WIDTH // 2 + PLAYER_SPACE-MARGIN)

        self.tile_list.append(tile)
    
    def setup(self):

        self.player_1_turn = True

        self.grid = Grid(ROW_COUNT, COLUMN_COUNT, self.word_list)
        arcade.set_background_color(arcade.color.SAP_GREEN)

        self.held_letters = []
        self.held_letter_position = []

        self.pouch = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()
        self.letter_rack = arcade.SpriteList()
        self.table_temp = arcade.SpriteList()
        self.table_perm = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.held_letter = arcade.SpriteList()

        # Text variables

        for letter, (score, amount) in LETTERS.items():
            for _ in range(amount):
                letter_sprite = Letter(letter, score, scale=SCALE)
                letter_sprite.position = MARGIN+GRID_WIDTH+INFO_SPACE//2,\
                                         GRID_HEIGHT//2+PLAYER_SPACE-MARGIN
                self.pouch.append(letter_sprite)

        # Populate scrabble board
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
        
        for i in range(1,8):
            tile = BonusTile('mat', scale=SCALE)
            tile.position = MARGIN+GRID_WIDTH//4+WIDTH*i+i*8,\
                            MARGIN*1.5
            self.letter_rack.append(tile)
        
        self.player_1.held_letters = SpriteList()
        self.player_2.held_letters = SpriteList()

        for i in range(1,8):
            j = randint(0, len(self.pouch)-1)
            letter = self.pouch.pop(j)
            letter.position = MARGIN+GRID_WIDTH//4+WIDTH*i+i*8,\
                                MARGIN*1.5
            self.player_1.held_letters.append(letter)
        
        for i in range(1,8):
            j = randint(0, len(self.pouch)-1)
            letter = self.pouch.pop(j)
            letter.position = MARGIN+GRID_WIDTH//4+WIDTH*i+i*8,\
                                MARGIN*1.5
            self.player_2.held_letters.append(letter)
        
        print([letter.letter for letter in self.player_1.held_letters])

        # TODO: Put button positions into BUTTON_NAMES
        #       and maybe initialize in __init__

        for name, (x, y) in BUTTON_NAMES.items():
            button = Button(name)
            button.position = x, y
            self.button_list.append(button)


    
    def on_draw(self):
        
        arcade.start_render()

        players_turn_text = "{} á leik".format(self.player_1_name if self.player_1_turn else self.player_2_name)


        self.letter_rack.draw()
        self.tile_list.draw()
        self.table_temp.draw()
        self.table_perm.draw()
        self.button_list.draw()
        #self.pouch.draw()
        if self.player_1_turn:
            self.player_1.held_letters.draw()
        else:
            self.player_2.held_letters.draw()
        self.held_letter.draw()
        arcade.draw_text(players_turn_text, 300, 120, arcade.color.YELLOW, 20)

    def pull_to_top(self, card, player_letters):
        try:
            index = player_letters.index(card)
            for i in range(index, len(player_letters) - 1):
                player_letters[i] = player_letters[i+1]
            player_letters[len(player_letters) - 1] = card
        except ValueError:
            index = self.table_temp.index(card)
            for i in range(index, len(self.table_temp) - 1):
                self.table_temp[i] = self.table_temp[i+1]
            self.table_temp[len(self.table_temp) - 1] = card



    def on_mouse_press(self, x, y, button, modifiers):
        player_letters = self.player_1.held_letters if self.player_1_turn else self.player_2.held_letters
        temp_sprite_list = SpriteList()
        for sprite in player_letters:
            if sprite not in temp_sprite_list:
                temp_sprite_list.append(sprite)
        for sprite in self.table_temp:
            if sprite not in temp_sprite_list:
                temp_sprite_list.append(sprite)
        if not self.turn_over:
            letters = arcade.get_sprites_at_point((x,y), temp_sprite_list)



            print([letter.letter for letter in letters])

            if len(letters) > 0:
                primary_letter = letters[-1]

                self.held_letters = moved = [primary_letter]
                self.held_letter_position = [self.held_letters[0].position]
                self.pull_to_top(self.held_letters[0], player_letters)

                if moved[0] in player_letters:
                    self.origin = player_letters
                    player_letters.remove(moved[0])
                if moved[0] in self.table_temp:
                    self.origin = self.table_temp
                    self.table_temp.remove(moved[0])
                self.held_letter.append(moved[0])
                
                
            

        
        button = arcade.get_sprites_at_point((x,y), self.button_list)

        if len(button) > 0:
            if (button[0].name == 'reset'):
                self.setup()
            elif (button[0].name == 'check'):
                # self.grid.check()
                self.grid.check()
            elif (button[0].name == 'confirm'):
                self.play_game()
            elif (button[0].name == 'draw'):
                if not self.turn_over:
                    self._switch_letters(player_letters)
            elif (button[0].name == 'pass'):
                self.player_1_turn = not self.player_1_turn


    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for letter in self.held_letters:
            letter.center_x += dx
            letter.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if len(self.held_letters) == 0:
            return
        
        tile, distance = arcade.get_closest_sprite(self.held_letters[0], self.tile_list)
        rack, distance = arcade.get_closest_sprite(self.held_letters[0], self.letter_rack)

        if self.player_1_turn:
            player_letters = self.player_1.held_letters
        else:
            player_letters = self.player_2.held_letters


        print(list(self.held_letter))

        if self.table_temp:
            table_letter, distance = arcade.get_closest_sprite(self.held_letters[0], self.table_temp)
        if self.table_perm:
            perm_letter, distance = arcade.get_closest_sprite(self.held_letters[0], self.table_perm)

        if not player_letters:
            player_letters = self.table_temp
        rack_letter, distance = arcade.get_closest_sprite(self.held_letters[0], player_letters)

        reset_position = True
 
        if arcade.check_for_collision(self.held_letters[0], rack_letter):
            if self.held_letters[0] in self.table_temp:
                # player_letters.remove(self.held_letters[0])
                reset_position = False
                print("bla")
            else:
                reset_position = True
            self.held_letter.remove(self.held_letters[0])
            player_letters.append(self.held_letters[0])
            print('1')
            print([letter.letter for letter in player_letters])
        
        elif self.table_temp and arcade.check_for_collision(self.held_letters[0], table_letter):
            reset_position = True
            self.held_letter.remove(self.held_letters[0])
            player_letters.append(self.held_letters[0])
            print('2')

        elif self.table_perm and arcade.check_for_collision(self.held_letters[0], perm_letter):
            reset_position = True
            self.held_letter.remove(self.held_letters[0])
            player_letters.append(self.held_letters[0])
            print('2.5')



        elif arcade.check_for_collision(self.held_letters[0], tile):

            for i, dropped_letter in enumerate(self.held_letters):
                dropped_letter.position = tile.center_x, tile.center_y
                if dropped_letter in self.grid.word:
                    self.grid.remove_from_grid(dropped_letter)
                if dropped_letter.blank:
                    print("This is blank")
                    self.root = Tk()
                    self.user_setup = BlankLetterSet(self.root)
                    self.root.mainloop()
                    applied_letter = self.user_setup.letter_val
                    dropped_letter.letter = applied_letter if applied_letter else 'BLANK'
                self.grid.add_to_grid(tile.row, tile.col, dropped_letter)
            self.held_letter.remove(self.held_letters[0])
            self.table_temp.append(self.held_letters[0])
            print('3')

            
            reset_position = False
        elif arcade.check_for_collision(self.held_letters[0], rack):
            print(self.held_letters[0].letter)

            for i, dropped_letter in enumerate(self.held_letters):
                dropped_letter.position = rack.center_x, rack.center_y
                self.grid.remove_from_grid(dropped_letter)
            self.held_letter.remove(self.held_letters[0])
            player_letters.append(self.held_letters[0])
            print('4')

            
            reset_position = False


        if reset_position:
            for tile_index, letter in enumerate(self.held_letters):
                letter.position = self.held_letter_position[tile_index]
                if letter in self.held_letter:
                    self.held_letter.remove(letter)
                self.origin.append(letter)

        print(list(self.held_letter))
        print(list(self.table_temp))
        self.held_letters = []
    
    def play_game(self):
        player = self.player_1 if self.player_1_turn else self.player_2
        if self.grid.check() == True:
            self.table_perm.extend([sprite for sprite in self.table_temp])
            player.nr_of_letters -= len(self.table_temp)
            self.table_temp = SpriteList()
            self.grid.play(player)
            self.grid.word.clear()
            self.grid.index_list.clear()

            for _ in range(player.nr_of_letters, 7):
                if self.pouch:
                    j = randint(0, len(self.pouch))
                    letter_to_add = self.pouch[j]
                    player.held_letters.append(letter_to_add)
                    self.pouch.remove(letter_to_add)

                else:
                    pass    # TODO: Skrifa út að pokinn sé tómur og BRAKE

            player.nr_of_letters = len(player.held_letters)

            for i in range(1, player.nr_of_letters+1):
                letter = player.held_letters[i-1]
                letter.position = MARGIN+GRID_WIDTH//4+WIDTH*i+i*8,\
                    MARGIN*1.5

            if player.nr_of_letters == 0:
                # GAME OVER
                pass

            else:
                self.player_1_turn = not self.player_1_turn
                self.turn_over = False
    
    def game_over(self):
        leftover_player = self.player_1 if self.player_1.nr_of_letters > 0 else self.player_2

        for letter in leftover_player.held_letters:
            leftover_player.score -= letter.score
    
    def _switch_letters(self, player_letters):

        self.root = Tk()
        original_letters = [letter for letter in player_letters]
        self.draw_window = DrawLetterWindow(self.root, player_letters)
        self.root.mainloop()
        if self.draw_window.letters_to_switch:
            for sprite in original_letters:
                if sprite.letter in self.draw_window.letters_to_switch:
                    self.draw_window.letters_to_switch.remove(sprite.letter)
                    x, y = sprite.position
                    player_letters.remove(sprite)
                    j = randint(0, len(self.pouch)-1)
                    pouch_letter = self.pouch[j]
                    pouch_letter.position = x, y
                    player_letters.append(pouch_letter)
                    self.pouch.remove(pouch_letter)
                    self.pouch.append(sprite)
            
            self.turn_over = True
            



def get_wordlist(file_name):
    with open(file_name, 'r') as f:
        word_set = [word.strip().upper() for word in f.readlines()]
        return word_set


def main():
    file_name = 'ordmyndir.txt'
    word_list = get_wordlist(file_name)
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, word_list)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
