
class Player:


    def __init__(self, player_name) -> None:
        self.name = player_name
        self.score = 0
        self.held_letters = []

    def add_score(self, score):
        self.score += score