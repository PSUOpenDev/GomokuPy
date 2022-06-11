'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
from GomokuPlayer import GomokuPlayer
from GomokuAI import GomokuAI
from GomokuAction import GomokuAction
import random
import pickle
from GomokuState import GomokuState
import os

class QLearningAIPlayer(GomokuPlayer, GomokuAI):

    def __init__(self):
        self.learning_rate: float = 1.0
        self.gamma: float = 0.9
        self.epsilon: float = 0.1
        self.__q_table = {}
        super().__init__()

    def training(self):
        r = 0.0
        max_q = 0.0
        current = self.current_state

        while current != None:
            s = 0
            a = 0
            if current.previous_state != None:
                s = current.previous_state.hash()

            if current.previous_action != None:
                a = current.previous_action.hash()

            if (s, a) not in self.__q_table:
                self.__q_table[(s, a)] = 0.0

            r = self.current_state.get_reward(self.get_id())

            self.__q_table[(s, a)] += self.learning_rate * \
                (r + self.gamma * max_q - self.__q_table[(s, a)])

            max_q = self.get_max_q(current)

            current = current.previous_state

    def get_max_q(self, c: GomokuState) -> float:
        max_val = 0

        if c != None and c.previous_state != None and c.previous_action:
            list_all_action = c.previous_state.get_all_available_pos()
            for point in list_all_action:
                action = GomokuAction(self.get_id(),point)
                s = c.previous_state.hash()
                a = action.hash()

                if (s, a) in self.__q_table and self.__q_table[(s, a)] > max_val:
                    max_val = self.__q_table[(s, a)]

        return max_val

    def deliver_action(self) -> GomokuAction:
        selected_point: tuple(int, int) = None

        all_next_points = self.current_state.get_all_available_pos()

        if self.training_mode:
            if random.uniform(0, 1) <= self.epsilon:
                selected_point = all_next_points[random.randint(
                    0, len(all_next_points)-1)]
                return GomokuAction(self.get_id(), selected_point)
        else:
            max_val = -100000000000
            selected_action: GomokuAction = None

            selected_action_list:list[GomokuAction] = []

            for point in all_next_points:
                selected_action = GomokuAction(self.get_id(), point)

                hp = (self.current_state.hash(), selected_action.hash())

                if hp in self.__q_table:
                    if self.__q_table[hp] == max_val:
                        selected_action_list.append(selected_action)
                    else:
                        selected_action_list.clear()
                        selected_action_list.append(selected_action)

                        max_val = self.__q_table[hp]

                if len(selected_action_list) > 0:
                    #return selected_action[random.randint(0, len(selected_action_list))]
                    list = [(self.current_state.get_point_evaluation(action.get_point(), self.get_id()), point) for point in selected_action]
                    list.sort(key=lambda x: x[0], reverse=True)
                    (val1, chose_point1) = list[0]

                    list = [(self.current_state.get_point_evaluation(action.get_point(), self.get_opponent_id()), point) for point in all_next_points]
                    list.sort(key=lambda x: x[0], reverse=True)
                    (val2, chose_point2) = list[0]
                    
                    if val1 < val2:
                        return GomokuAction(self.get_id(), chose_point2)
                    else:
                        return GomokuAction(self.get_id(), chose_point1)

                else:
                    selected_point = all_next_points[random.randint(
                        0, len(all_next_points)-1)]
                    return GomokuAction(self.get_id(), selected_point)



                
        return None
        

    def save_to_file(self,filename:str):
        filehandler = open(filename,"wb")
        pickle.dump(self.__q_table ,filehandler)
        filehandler.close()

    def load_file(self,filename:str):
        # dump : put the data of the object in a file
        if os.path.exists(filename) :
            file = open(filename,'rb')
            self.__q_table = pickle.load(file)
            file.close()