'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
from GomokuState import GomokuState
from GomokuAction import GomokuAction


class GomokuPlayer:
    ALL_ID = [1, -1]

    def __init__(self):
        self.__id: int = 0
        self.__total_points = 0
        self.current_state: GomokuState = None
        super().__init__()

    def set_id(self, id: int):
        self.__id = id

    def get_id(self) -> int:
        return self.__id

    def get_opponent_id(self) -> int:
        return - self.__id

    def update_state(self, currentState: GomokuState):
        self.current_state = currentState

    def deliver_action(self) -> GomokuAction:
        pass

    def reset(self):
        self.current_state = None

    def update_point(self, point: float):
        self.__total_points += point
