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

        self.word_list = word_list  # Word list to validate words

        # Initialize sprite lists as None (further initialization in setup())
        self.pouch = None
        self.tile_list = None
        self.letter_rack = None
        self.held_letters = None
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
        # self.player_1_turn = True

        self.held_letters = []
        self.held_letter_position = []

        self.pass_count = 0
        self.player_index = 0

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

        self._make_scrabble_board()
        self._make_letters()
        self._make_buttons()
        self._make_mat()

        for player in self.players:
            player.held_letters = SpriteList()
            player.nr_of_letters = 0
            player.score = 0
            player.draw_letters(self.pouch)



    def _make_mat(self):
        for i in range(1, LETTER_ON_HAND + 1):
            tile = BonusTile('mat', scale=SCALE)
            tile.position = MAT_X + (WIDTH * i) + (i * 8), MAT_Y
            self.letter_rack.append(tile)

    
    def _make_buttons(self):
        for name, (x, y) in BUTTON_NAMES.items():
            button = Button(name)
            button.position = x, y
            self.button_list.append(button)


    def _make_letters(self):
        for letter, (score, amount) in LETTERS.items():
            for _ in range(amount):
                letter_sprite = Letter(letter, score, scale=SCALE)
                self.pouch.append(letter_sprite)


    def _make_scrabble_board(self):
        self.grid = Grid(ROW_COUNT, COLUMN_COUNT, self.word_list)

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
        tile = BonusTile(key, x, y, SCALE)
        tile.position = ((GRID_MARGIN+HEIGHT) * y) + GRID_MARGIN + (HEIGHT // 2) + MARGIN,\
                        ((GRID_MARGIN+WIDTH) * (ROW_COUNT-1-x)) + GRID_MARGIN + (WIDTH // 2) + PLAYER_SPACE - MARGIN

        self.tile_list.append(tile)

        
    
    def on_draw(self):
        
        arcade.start_render()
        player = self.get_current_player()
        players_turn_text = f"{player.name} á leik"
        for i, player in enumerate(self.players):
            arcade.draw_text(str(player), 900, 580 + (i * 60), arcade.color.YELLOW, 16, align='center', anchor_x='center', anchor_y='center')

        

        arcade.draw_text(players_turn_text, 450, 130, arcade.color.YELLOW, 20, align='center', anchor_x='center', anchor_y='center')

        
        self.letter_rack.draw()
        self.tile_list.draw()
        self.table_temp.draw()
        self.table_perm.draw()
        self.button_list.draw()
        #self.pouch.draw()
        player = self.get_current_player()
        player.held_letters.draw()

        self.held_letter.draw()

        arcade.draw_text(self.error_text, 800, 100, arcade.color.WHITE, 16, align='left', anchor_x='center', anchor_y='center')
        arcade.draw_text(self.winner_text, 800, 100, arcade.color.ANTI_FLASH_WHITE, 20, align='center', anchor_x='center', anchor_y='center')
        arcade.draw_text(self.wrong_words_text, 800, 100, arcade.color.WHITE, 16, align='left', anchor_x='center', anchor_y='center')

    def pull_to_top(self, letter, letter_class):
        index = letter_class.index(letter)
        for i in range(index, len(letter_class) - 1):
            letter_class[i] = letter_class[i+1]
        letter_class[len(letter_class) - 1] = letter


    def _get_active_letters(self, player):
        active_letters = SpriteList()
        for sprite in player.held_letters:
            if sprite not in active_letters:
                active_letters.append(sprite)
        for sprite in self.table_temp:
            if sprite not in active_letters:
                active_letters.append(sprite)
        return active_letters


    def _hold_letter(self, player, letters):
        moved_letter = letters[-1]

        self.held_letter.append(moved_letter)
        self.held_letter_position = moved_letter.position

        if moved_letter in player.held_letters:
            self.pull_to_top(moved_letter, player.held_letters)
        else:
            self.pull_to_top(moved_letter, self.table_temp)

        if moved_letter in player.held_letters:
            self.origin = player.held_letters
            player.held_letters.remove(moved_letter)
        elif moved_letter in self.table_temp:
            self.origin = self.table_temp
            self.table_temp.remove(moved_letter)


    def _select_letter(self, player:Player, x, y):
        active_letters = self._get_active_letters(player)

        if not self.turn_over:
            letters = arcade.get_sprites_at_point((x,y), active_letters)

            if len(letters) > 0:
                self._hold_letter(player, letters)
    

    def _press_check(self):
        checked_results = self.grid.check()
        if checked_results == True:
            self.wrong_words_text = "Orð er til!"
        elif checked_results == False:
            self.error_text = "Enginn stafur er á borði\neða staðsetning þeirra\ner vitlaus."
        else:
            self.wrong_words_text = "Eftirfarandi orð eru\nekki til:\n{}".format("\n".join(checked_results))
    
    def _select_button(self, player, x, y):

        button = arcade.get_sprites_at_point((x,y), self.button_list)
        if len(button) > 0:
            if (button[0].name == 'reset'):
                self.setup()

            elif (button[0].name == 'check') and not self.is_game_over:
                self._press_check()

            elif (button[0].name == 'confirm') and not self.is_game_over:
                self.play_game()

            elif (button[0].name == 'draw') and not self.is_game_over:
                if not self.turn_over:
                    self._switch_letters(player)

            elif (button[0].name == 'pass') and not self.is_game_over:
                if not self.turn_over:
                    self.pass_count += 1
                    self.pass_turn(player)


    def pass_turn(self, player):
        letters_in_play = [letter for letter in self.table_temp]
        for letter in letters_in_play:
            player.held_letters.append(letter)
            self.table_temp.remove(letter)
            self.grid.remove_from_grid(letter)
        player.position_letters()
        

        if self.pass_count >= 2 * len(self.players):
            self.game_over()
        self.turn_over = False
        self.player_index += 1

    def on_mouse_press(self, x, y, button, modifiers):
        self.error_text = ""
        self.wrong_words_text = ""
        player = self.get_current_player()

        self._select_button(player, x, y)

        if not self.is_game_over:
            self._select_letter(player, x, y)


    def get_current_player(self):
        index = self.player_index % len(self.players)
        return self.players[index]


    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for letter in self.held_letter:
            letter.center_x += dx
            letter.center_y += dy



    # TODO: REALLY need to refactor!

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if len(self.held_letter) == 0:
            return

        held_letter = self.held_letter[0]
        player = self.get_current_player()
        player_letters = player.held_letters
        tile, rack, rack_letter, table_letter, perm_letter = self._get_objects(held_letter, player_letters)

        reset_position = True
 
        if arcade.check_for_collision(held_letter, rack_letter):
            reset_position = False if held_letter in self.table_temp else True
        
        elif self.table_temp and arcade.check_for_collision(held_letter, table_letter):
            reset_position = True

        elif self.table_perm and arcade.check_for_collision(held_letter, perm_letter):
            reset_position = True

        elif arcade.check_for_collision(held_letter, tile):     # TODO: Keep changing self.held_letters[0] to held_letter            
            self._place_on_board(held_letter, tile)
            reset_position = False

        elif arcade.check_for_collision(held_letter, rack):
            self._place_on_rack(held_letter, player_letters, rack)
            reset_position = False


        if reset_position:
                held_letter.position = self.held_letter_position
                self.origin.append(held_letter)

        self.held_letter.remove(held_letter)

    def _get_objects(self, held_letter, player_letters):

        tile = None
        rack = None
        rack_letter = None
        table_letter = None
        perm_letter = None

        if not player_letters:
            player_letters = self.table_temp
        rack_letter = arcade.get_closest_sprite(held_letter, player_letters)[0]
        if self.table_temp:
            table_letter = arcade.get_closest_sprite(held_letter, self.table_temp)[0]
        if self.table_perm:
            perm_letter = arcade.get_closest_sprite(held_letter, self.table_perm)[0]
        tile = arcade.get_closest_sprite(held_letter, self.tile_list)[0]
        rack = arcade.get_closest_sprite(held_letter, self.letter_rack)[0]

        return tile, rack, rack_letter, table_letter, perm_letter


    def _place_on_board(self, held_letter, tile):
        held_letter.position = tile.center_x, tile.center_y
        if held_letter in self.grid.temp_letters:
            self.grid.remove_from_grid(held_letter)
        if held_letter.blank:
            self._set_blank(held_letter)

        self.grid.add_to_grid(tile.row, tile.col, held_letter)
        self.table_temp.append(held_letter)
    
    def _place_on_rack(self, held_letter, player_letters, rack):
            held_letter.position = rack.center_x, rack.center_y
            self.grid.remove_from_grid(held_letter)
            player_letters.append(held_letter)


    def _set_blank(self, held_letter):
        self.root = Tk()    
        self.user_setup = BlankLetterSet(self.root) 
        self.root.mainloop()    
        applied_letter = self.user_setup.letter_val 
        held_letter.letter = applied_letter if applied_letter else '0'

    def play_letters(self, player):
        self.table_perm.extend([sprite for sprite in self.table_temp])
        player.nr_of_letters -= len(self.table_temp)
        self.table_temp = SpriteList()
        score = self.grid.play(player)
        self.error_text = f"+{score} stig"
        self.grid.temp_letters.clear()
        self.grid.index_list.clear()

    
    def play_game(self):
        player = self.get_current_player()
        checked_results = self.grid.check()
        if self.turn_over:
            self.player_index += 1
            self.turn_over = False
            self.pass_count = 0
        elif checked_results == True:
            self.pass_count = 0
            self.play_letters(player)
            player.draw_letters(self.pouch)

            if not self.pouch:
                self.error_text = "Stafapoki er tómur"
                return

            if player.nr_of_letters == 0:
                # GAME OVER
                self.game_over()

            else:
                # self.player_1_turn = not self.player_1_turn
                self.player_index += 1
                self.turn_over = False

        elif checked_results == False:
            self.error_text = "Enginn stafur er á borði\neða staðsetning þeirra\ner vitlaus."
        else:
            self.wrong_words_text = "Eftirfarandi orð eru\nekki til:\n{}".format("\n".join(checked_results))

    
    def game_over(self):
        self.is_game_over = True

        for player in self.players:
            if player.nr_of_letters > 0:
                for letter in player.held_letters:
                    player.score -= letter.score

        winner = [self.players[0]]
        for player in self.players[1:]:
            if player.score > winner[0].score:
                winner = [player]
            elif player.score == winner[0].score:
                winner.append(player)
            

        if len(winner) > 1:
            winners = "\n".join(winner)
            self.winner_text = "Jafntefli!\n" + winners
        else:
            self.winner_text = f"{winner[0].name}\ner sigurvegari!"      



    
    def _switch_letters(self, player:Player):

        self.root = Tk()
        self.draw_window = DrawLetterWindow(self.root, player.held_letters)
        self.root.mainloop()
        if self.draw_window.letters_to_switch:
            new_letters = player.switch_letters(self.pouch, self.draw_window.letters_to_switch)
            self.error_text = f'Dregnir stafir\n{", ".join(new_letters)}'
            self.player_index += 1
            self.turn_over = False
            



def get_wordlist(file_name):
    with open(file_name, 'r') as f:
        word_set = [word.strip().upper() for word in f.readlines()]
        return word_set


def main():
    subdir = "data"
    file_name = 'ordmyndir.txt'
    path = os.path.join(subdir, file_name)
    word_list = get_wordlist(path)
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, word_list)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
