'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
from GomokuAI import GomokuAI
from GomokuAction import GomokuAction
from GomokuFrontEnd import GomokuFrontEnd
from GomokuPlayer import GomokuPlayer
from GomokuState import GomokuState
from QLearningAIPlayer import QLearningAIPlayer

class GomokuRunner:
    def __init__(self, player1: GomokuPlayer, player2: GomokuPlayer, frontend: GomokuFrontEnd = None):
        self.__player1 = player1
        self.__player2 = player2

        self.__current_player: GomokuPlayer = None
        self.__current_state: GomokuState = None
        self.__current_action: GomokuAction = None

        self.__the_winner: GomokuPlayer = None
        self.__frontend: GomokuFrontEnd = frontend

    def __reset(self):
        self.__current_player: GomokuPlayer = None
        self.__current_state: GomokuState = GomokuState()
        self.__current_action: GomokuAction = None
        self.__current_state.current_player_id = self.__player1.get_id()
        self.__the_winner: GomokuPlayer = None

        if isinstance(self.__player1, GomokuAI):
            if self.__player1.is_training_mode():
                self.__player1.reset()

        if isinstance(self.__player2, GomokuAI):
            if self.__player2.is_training_mode():
                self.__player2.reset()

    def __update_state(self):
        self.__player1.update_state(self.__current_state)
        self.__player2.update_state(self.__current_state)

    def __apply_action(self):
        self.__current_state = self.__current_state.next_state(
            self.__current_action)

    def __training(self):

        if isinstance(self.__player1, GomokuAI):
            if self.__player1.is_training_mode():
                self.__player1.training()

        if isinstance(self.__player2, GomokuAI):
            if self.__player2.is_training_mode():
                self.__player2.training()

    def play(self, show_frontend=True):
        self.__player1.set_id(1)
        self.__player2.set_id(-1)

        self.__reset()
        self.__update_state()

        is_running = True
        
        if show_frontend and self.__frontend != None:
            self.__frontend.init()

        while is_running:

            if self.__current_player == self.__player1:
                self.__current_player = self.__player2
            elif self.__current_player == self.__player2:
                self.__current_player = self.__player1
            else:
                self.__current_player = self.__player1
                


            self.__current_action = self.__current_player.deliver_action()

            if self.__current_action != None:
                self.__apply_action()
                self.__update_state()

                if show_frontend and self.__frontend != None:
                    self.__frontend.add_action( self.__current_action.get_point())
                
            is_running = self.__current_state.is_running()

        if show_frontend and self.__frontend != None:
            if self.__current_state.the_winner_id() == -1:
                self.__frontend.display_winner('Black won!')
                self.__frontend.draw_winning_points(self.__current_state.winning_points)
            elif self.__current_state.the_winner_id() == 1:
                self.__frontend.display_winner('Red won!')
                self.__frontend.draw_winning_points(self.__current_state.winning_points)
            else:
                self.__frontend.display_winner('Draw!')
        #self.__current_state.print_state()

        self.__training()

    @staticmethod
    def q_learning_train(epoch = 100):
        player1 = QLearningAIPlayer()
        player2 = QLearningAIPlayer()

    
        player1.load_file("player1.db")
        player2.load_file("player2.db")

        game = GomokuRunner(player1, player2)

        for _ in range(0, epoch):
            game.play()
        

        player1.save_to_file("player1.db")
        player2.save_to_file("player2.db")