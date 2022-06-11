'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
from __future__ import annotations
from __future__ import print_function

import copy
import sys
from GomokuAI import GomokuAI
from GomokuAction import GomokuAction


MAX_INT = sys.maxsize


class GomokuState:

    WINNING_SAMPLES = [
        ('#XXXX', '#XXXX'.find('#')),
    ]

    LEVEL_SAMPLES = [
        ('#XXX', '#XXX'.find('#'), 1000),
        ('#XX', '#XX'.find('#'), 100),
        ('#X', '#X'.find('#'), 10),
    ]

    ATTACK_SAMPLES = [
        ('#XXXX', '#XXXX'.find('#'), 10000),
        ('X#XXX', 'X#XXX'.find('#'), 10000),
        ('XX#XX', 'XX#XX'.find('#'), 10000),

        ('_#XXX', '_#XXX'.find('#'), 1000),
        ('_X#XX', '_X#XX'.find('#'), 1000),
        ('_XX#X', '_XX#X'.find('#'), 1000),
        ('_XXX#', '_XXX#'.find('#'), 1000),

        ('#_XXX', '#_XXX'.find('#'), 1000),
        ('X_#XX', 'X_#XX'.find('#'), 1000),
        ('X_X#X', 'X_X#X'.find('#'), 1000),
        ('X_XX#', 'X_XX#'.find('#'), 1000),

        ('#X_XX', '#X_XX'.find('#'), 1000),
        ('X#_XX', 'X#_XX'.find('#'), 1000),
        ('XX_#X', 'XX_#X'.find('#'), 1000),
        ('XX_X#', 'XX_X#'.find('#'), 1000),      

        ('_#XX_', '_#XX_'.find('#'), 100),
        ('_X#X_', '_X#X_'.find('#'), 100),
        ('_XX#_', '_XX#_'.find('#'), 100),

        ('#_XX_', '#_XX_'.find('#'), 100),
        ('X_#X_', 'X_#X_'.find('#'), 100),
        ('X_X#_', 'X_X#_'.find('#'), 100),

        ('#X_X_', '#X_X_'.find('#'), 100),
        ('X#_X_', 'X#_X_'.find('#'), 100),
        ('XX_#_', 'XX_#_'.find('#'), 100),

        ('_#X__', '_#X__'.find('#'), 10),
        ('_X#__', '_X#__'.find('#'), 10),

    ]

    MAX_LENGTH: int = 20
    TOTAL_STATE: int = 3
    WIN_NUM_POST: int = 5

    WIN_REWARD: float = 100.0
    LOSE_REWARD: float = -100.0
    DRAW_REWARD: float = 0.0

    DISTANCE_FROM_CHECKED_POS: int = 2

    MAX_POSSIBLE_POINTS = 300

    def __init__(self):
        self.__board = {}
        self.previous_state: GomokuState = None
        self.previous_action: GomokuAction = None
        self.previous_player_id: int = 0
        self.current_player_id: int = 0
        self.__the_winner_id: int = 0
        self.__the_loser_id: int = 0
        self.__hash = MAX_INT
        self.__reward = {-1: 0.0, 1: 0.0}
        self.winning_points = []

    def next_state(self, action: GomokuAction) -> GomokuState:
        new_state = copy.deepcopy(self)

        if (action.get_x(), action.get_y()) not in self.__board:
            new_state.previous_state = self
            new_state.__board[action.get_point()] = action.get_id()
            new_state.previous_action = action
            new_state.previous_player_id = action.get_id()
            new_state.current_player_id = - action.get_id()
            new_state.__hash = MAX_INT

        return new_state

    def print_state(self):
        print('=========================================================================')
        for i in range(GomokuState.MAX_LENGTH):
            for j in range(GomokuState.MAX_LENGTH):
                val = self.get_pos_val((i, j))
                if val == 0:
                    print(" _ ", end="")
                elif val == 1:
                    print(" X ", end="")
                elif val == -1:
                    print(" O ", end="")

            print('')

    def get_pos_val(self, point: tuple(int, int)) -> int:
        if point in self.__board:
            return self.__board[point]

        return 0

    def hash(self):
        if self.__hash != MAX_INT:
            self.__hash = 0
            for i in range(GomokuState.MAX_LENGTH):
                for j in range(GomokuState.MAX_LENGTH):

                    pos_val = self.get_pos_val(i, j)
                    if pos_val == -1:
                        pos_val = 2

                    self.__hash = GomokuState.TOTAL_STATE*self.__hash + pos_val

        return self.__hash

    def __move_back(self, point: tuple(int, int), c: int, direction: int) -> tuple(tuple(int, int), bool):
        x = point[0]
        y = point[1]

        match direction:
            # Horizon
            case 1:
                if y - c >= 0:
                    return ((x, y - c), True)

            # Vertical
            case 2:
                if x - c >= 0:
                    return ((x - c, y), True)

            # Cross down
            case 3:
                if x - c >= 0 and y - c >= 0:
                    return ((x - c, y - c), True)

            # Cross up
            case 4:
                if x + c < GomokuState.MAX_LENGTH and y - c >= 0:
                    return ((x + c, y - c), True)

        return ((x, y), False)

    def __move_forward(self, point: tuple(int, int), c: int, direction: int) -> tuple(tuple(int, int), bool):
        x = point[0]
        y = point[1]

        match direction:
            # Horizon
            case 1:
                if y + c < GomokuState.MAX_LENGTH:
                    return ((x, y + c), True)

            # Vertical
            case 2:
                if x + c < GomokuState.MAX_LENGTH:
                    return ((x + c, y), True)

            # Cross down
            case 3:
                if x + c < GomokuState.MAX_LENGTH and y + c < GomokuState.MAX_LENGTH:
                    return ((x + c, y + c), True)

            # Cross up
            case 4:
                if x - c >= 0 and y + c < GomokuState.MAX_LENGTH:
                    return ((x - c, y + c), True)

        return ((x, y), False)

    def __check_backward(self, pattern: str, starting_in_pattern: int, begin_pos: tuple(int, int), player_id: int,  direction: int):
        list_point = []
        for c in reversed(range(0, starting_in_pattern)):
            (new_point, can) = self.__move_back(
                begin_pos, starting_in_pattern - c, direction)
            
            list_point.append(new_point)

            if can == False:
                return False,[]

            if pattern[c] == 'X' and player_id != self.get_pos_val(new_point):
                return False,[]

            if pattern[c] == '_' and 0 != self.get_pos_val(new_point):
                return False,list_point

        return True,list_point

    def __check_forward(self, pattern: str, starting_in_pattern: int, begin_pos: tuple(int, int), player_id: int,  direction: int):
        list_point = []
        for c in range(1, len(pattern)-starting_in_pattern):
            (new_point, can) = self.__move_forward(begin_pos, c, direction)

            list_point.append(new_point)

            if can == False:
                return False,[]

            if pattern[starting_in_pattern+c] == 'X' and player_id != self.get_pos_val(new_point):
                return False,[]

            if pattern[starting_in_pattern+c] == '_' and 0 != self.get_pos_val(new_point):
                return False,[]

        return True,list_point

    def __is_pattern_match(self, player_id: int, pattern: tuple([str, int]), direction: int, point: tuple(int, int)):

        result1,list_point1 = self.__check_backward(pattern[0], pattern[1], point, player_id, direction)
        result2,list_point2 = self.__check_forward(pattern[0], pattern[1], point, player_id, direction)
        
        list_point1 = list_point1 + list_point2
        list_point1.append(point)
        
        if result1  and result2:
            return True,list_point1

        rev_pattern = pattern[0][::-1]
        rev_pattern_pos = len(pattern[0]) - pattern[1] - 1

        result1,list_point1 = self.__check_backward(rev_pattern, rev_pattern_pos, point, player_id, direction)
        result2,list_point2 = self.__check_forward(rev_pattern, rev_pattern_pos, point, player_id, direction)
        
        list_point1 = list_point1 + list_point2
        list_point1.append(point)

        if rev_pattern != pattern[0]:
            if result1 and result2:
                return True,list_point1
        
        return False,[]

    def is_running(self) -> False:

        key_list = list(self.__board.keys())

        self.__the_winner_id = 0
        self.__the_loser_id = 0
        
        result = None

        for point in key_list:
            val = self.get_pos_val(point)
            for pattern in GomokuState.WINNING_SAMPLES:
                for direction in range(1, 5):
                    check,result = self.__is_pattern_match(val, pattern, direction, point)
                    if check:
                        self.__the_winner_id = val
                        self.__the_loser_id = -val

                        self.__reward[self.__the_winner_id] = GomokuAI.WIN_REWARD
                        self.__reward[self.__the_loser_id] = GomokuAI.LOSE_REWARD
                        self.winning_points = result
                        return False

        if len(key_list) >= GomokuState.MAX_POSSIBLE_POINTS:
            self.__reward[self.current_player_id] = GomokuAI.DRAW_REWARD
            self.__reward[self.previous_player_id] = GomokuAI.DRAW_REWARD
            return False

        return True

    def get_point_evaluation(self, coordinator: tuple(int, int), player_id: int) -> float:
        result = 0.0

        for (pattern, pattern_pos, point) in GomokuState.ATTACK_SAMPLES:
            for direction in range(1, 5):
                check,list = self.__is_pattern_match(player_id, (pattern, pattern_pos), direction, coordinator)
                if check:
                    result += point

        return result

    def get_state_evaluation(self, player_id):
        key_list = list(self.__board.keys())
        current_reward = 0

        for point in key_list:
            val = self.get_pos_val(point)
            if val == player_id:
                for (pattern, pattern_pos, reward) in GomokuState.ATTACK_SAMPLES:
                    for direction in range(1, 5):
                        check, _ = self.__is_pattern_match(player_id, (pattern, pattern_pos), direction, point)
                        if check:
                            if current_reward < reward:
                                current_reward = reward

        return current_reward

    def get_all_available_pos(self) -> list[Point]:
        key_list = list(self.__board.keys())
        list_available_point = []
        list_available_point_dict = {}

        if len(list(self.__board.keys())) <= GomokuState.MAX_POSSIBLE_POINTS:
            if len(key_list) > 0:
                for point in key_list:
                    for direction in range(1, 5):
                        for c in range(1, GomokuState.DISTANCE_FROM_CHECKED_POS+1):
                            (new_point, can) = self.__move_forward(
                                point, c, direction)
                            if can and self.get_pos_val(new_point) == 0 and new_point not in list_available_point_dict:
                                list_available_point.append(new_point)
                                list_available_point_dict[new_point] = True

                            (new_point, can) = self.__move_back(
                                point, c, direction)
                            if can and self.get_pos_val(new_point) == 0 and new_point not in list_available_point_dict:
                                list_available_point.append(new_point)
                                list_available_point_dict[new_point] = True

            else:
                p = round(GomokuState.MAX_LENGTH/2)
                list_available_point.append((p, p))

        return list_available_point

    def the_winner_id(self) -> int:
        return self.__the_winner_id

    def the_loser(self) -> int:
        return self.__the_loser_id

    def h_point(self) -> tuple(int, int):
        return (self.previous_state.hash(), self.previous_action.hash())

    def get_reward(self, player_id) -> float:
        return self.__reward[player_id]

    def check_exist_pos(self, x,y):
        return (x,y) in self.__board