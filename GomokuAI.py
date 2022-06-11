'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
class GomokuAI:
    WIN_REWARD = 1.0
    LOSE_REWARD = 0.0
    DRAW_REWARD = 0.5

    def __init__(self):
        self.training_mode: bool = False
        super().__init__()

    def is_training_mode(self) -> bool:
        return self.training_mode

    def set_training_mode(self):
        self.training_mode = True

    def set_playing_mode(self):
        self.training_mode = False

    def training(self):
        pass
