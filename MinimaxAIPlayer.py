'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
from GomokuAI import GomokuAI
from GomokuPlayer import GomokuPlayer
from GomokuAction import GomokuAction
from GomokuState import GomokuState
import random

POSITIVE_INFINITIVE = 1000000.0
NEGATIVE_INFINITIVE = -1000000.0


class MinimaxAIPlayer(GomokuPlayer, GomokuAI):

    def __init__(self):
        GomokuState.DISTANCE_FROM_CHECKED_POS = 1
        super().__init__()
        
    def deliver_action(self) -> GomokuAction:
        val, selected_action = self.minimax(
            self.current_state,None, 0, self.get_id())

        if selected_action != None and val != 0:
            return selected_action
        else:
            all_points = self.current_state.get_all_available_pos()
            list = [(self.current_state.get_point_evaluation(
                point, self.get_id()), point) for point in all_points]
            list.sort(key=lambda x: x[0], reverse=True)
            (val, chose_point) = list[0]

            return GomokuAction(self.get_id(), chose_point)

    def minimax(self, state: GomokuState,next_action:GomokuAction, depth: int, home_id):
        if depth > 0:
            result_of_calculation = 0
            if next_action != None:
                result_of_calculation = max(state.get_point_evaluation(next_action.get_point(), state.previous_player_id),
                                    state.get_point_evaluation(next_action.get_point(), state.current_player_id))
            return result_of_calculation, None

        if state.current_player_id == home_id:
            all_points = state.get_all_available_pos()
            max_eval = NEGATIVE_INFINITIVE
            max_action_list = []
            for point in all_points:
                action = GomokuAction(state.current_player_id, point)
                #next_state = state.next_state(action)
                val, _ = self.minimax(state,action, depth+1, home_id)
                if max_eval <= val:
                    if max_eval == val:
                        max_action_list.append(action)
                    else:
                        max_eval = val
                        max_action_list.clear()
                        max_action_list.append(action)

            if len(max_action_list) > 0:
                return max_eval, max_action_list[random.randint(0, len(max_action_list)-1)]
            else:
                return max_eval, None
        else:
            all_points = state.get_all_available_pos()
            min_eval = POSITIVE_INFINITIVE
            min_action_list = []
            for point in all_points:
                action = GomokuAction(state.current_player_id, point)
                #next_state = state.next_state(action)
                val, _ = self.minimax(state,action, depth+1, home_id)

                if min_eval >= val:
                    if min_eval == val:
                        min_action_list.append(action)
                    else:
                        min_eval = val
                        min_action_list.clear()
                        min_action_list.append(action)

            if len(min_action_list) > 0:
                return min_eval, min_action_list[random.randint(0, len(min_action_list)-1)]
            else:
                return min_eval, None
    # def deliver_action(self) -> GomokuAction:
    #     val, selected_action = self.minimax(
    #         self.current_state, 0, self.get_id())

    #     if selected_action != None and val != 0:
    #         return selected_action
    #     else:
    #         all_points = self.current_state.get_all_available_pos()
    #         list = [(self.current_state.get_point_evaluation(
    #             point, self.get_id()), point) for point in all_points]
    #         list.sort(key=lambda x: x[0], reverse=True)
    #         (val, chose_point) = list[0]

    #         return GomokuAction(self.get_id(), chose_point)

    # def minimax(self, state: GomokuState, depth: int, home_id):
    #     result_of_calculation = state.get_point_evaluation(state.previous_action.get_point(), state.previous_player_id)
    #     if depth > 2 or result_of_calculation >= 1000:
    #         if state.current_player_id == home_id:
    #             return result_of_calculation ,None
    #         else:
    #             return  - result_of_calculation, None
        
    #     if state.current_player_id == home_id:
    #         all_points = state.get_all_available_pos()
    #         max_eval = NEGATIVE_INFINITIVE
    #         max_action_list = []
    #         for point in all_points:
    #             action = GomokuAction(state.current_player_id, point)
    #             next_state = state.next_state(action)
    #             val, _ = self.minimax(next_state, depth+1, home_id)
    #             if max_eval <= val:
    #                 if max_eval == val:
    #                     max_action_list.append(action)
    #                 else:
    #                     max_eval = val
    #                     max_action_list.clear()
    #                     max_action_list.append(action)

    #         if len(max_action_list) > 0:
    #             return max_eval, max_action_list[random.randint(0, len(max_action_list)-1)]
    #         else:
    #             return max_eval, None
    #     else:
    #         all_points = state.get_all_available_pos()
    #         min_eval = POSITIVE_INFINITIVE
    #         min_action_list = []
    #         for point in all_points:
    #             action = GomokuAction(state.current_player_id, point)
    #             next_state = state.next_state(action)
    #             val, _ = self.minimax(next_state, depth+1, home_id)

    #             if min_eval >= val:
    #                 if min_eval == val:
    #                     min_action_list.append(action)
    #                 else:
    #                     min_eval = val
    #                     min_action_list.clear()
    #                     min_action_list.append(action)

    #         if len(min_action_list) > 0:
    #             return min_eval, min_action_list[random.randint(0, len(min_action_list)-1)]
    #         else:
    #             return min_eval, None
