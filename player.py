
class Player:


    def __init__(self, player_name) -> None:
        self.name = player_name
        self.score = 0
        self.held_letters = []
        self.nr_of_letters = 7

    def add_score(self, score):
        self.score += score