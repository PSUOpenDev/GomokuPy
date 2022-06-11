'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
import time
from GomokuPlayer import GomokuPlayer
from GomokuFrontEnd import GomokuFrontEnd
from GomokuState import GomokuState
from GomokuAction import GomokuAction

class HumanPlayer(GomokuPlayer):
    def __init__(self, frontend:GomokuFrontEnd= None):
        self.training_mode: bool = False
        self.__frontend = frontend
        self.__frontend.init_human_player()
        super().__init__()


    def deliver_action(self) -> GomokuAction:
         if self.__frontend != None:
            while True:
                x,y = self.__frontend.human_player_action()
                if x!= None and y != None and self.current_state.check_exist_pos(x-1,y-1) == False:
                    return GomokuAction(self.get_id(), (x-1,y-1))
                time.sleep(0.01)