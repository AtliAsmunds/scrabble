import arcade

class Letter(arcade.Sprite):

    def __init__(self, letter, score, scale=1):
        self.letter = letter
        self.score = score
        if letter == "0":
            self.blank = True
        else:
            self.blank = False

        self.image_file_name = f"tiles/letters_img/letter_{self.letter}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")
    
    def __str__(self) -> str:
        return self.letter

class BonusTile(arcade.Sprite):

    def __init__(self, bonus, row=None, col=None, scale=1):
        self.bonus = bonus
        self.row = row
        self.col = col

        self.image_file_name = f"tiles/bonus_tiles/{self.bonus}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class Button(arcade.Sprite):

    def __init__(self, name, scale=1):
        self.name = name

        self.image_file_name = f"tiles/buttons/{self.name}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")