import arcade
import os

tiles_dir = os.path.join('data', 'tiles')

class Letter(arcade.Sprite):

    def __init__(self, letter, score, scale=1):

        # Initialize Letter variables
        self.letter = letter
        self.score = score

        # Get the appropriate image for the sprite
        path = os.path.join(tiles_dir, 'letters_img')        
        self.image_file_name = os.path.join(path, f"letter_{self.letter}.png")

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")
    
    def __str__(self) -> str:
        return self.letter


class BonusTile(arcade.Sprite):

    def __init__(self, bonus, row=None, col=None, scale=1):

        # Initialize Bonus tile variables
        self.bonus = bonus
        self.row = row
        self.col = col

        # Get the appropriate image for the sprite
        path = os.path.join(tiles_dir, 'bonus_tiles')        
        self.image_file_name = os.path.join(path, f"{self.bonus}.png")

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class Button(arcade.Sprite):

    def __init__(self, name, scale=1):

        # Get the name for the button
        self.name = name

        # Get the appropriate image for the sprite
        path = os.path.join(tiles_dir, 'buttons')        
        self.image_file_name = os.path.join(path, f"{self.name}.png")

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")