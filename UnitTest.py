'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''

from GomokuRunner import GomokuRunner
from GomokuState import GomokuState
from GomokuPlayer import GomokuPlayer
from GomokuAction import GomokuAction
import unittest

from QLearningAIPlayer import QLearningAIPlayer


class TestGomokuState(unittest.TestCase):

    def test_check_stop(self):

        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 4)))
        state = state.next_state(GomokuAction(1, (2, 3)))
        state = state.next_state(GomokuAction(1, (3, 2)))
        state = state.next_state(GomokuAction(1, (4, 1)))
        state = state.next_state(GomokuAction(1, (5, 0)))
        self.assertEqual(state.the_winner_id(), 0)
        self.assertFalse(state.is_running())
        self.assertEqual(state.the_winner_id(), 1)

        state = GomokuState()
        state = state.next_state(GomokuAction(-1, (1, 1)))
        state = state.next_state(GomokuAction(-1, (2, 2)))
        state = state.next_state(GomokuAction(-1, (3, 3)))
        state = state.next_state(GomokuAction(-1, (4, 4)))
        state = state.next_state(GomokuAction(-1, (5, 5)))
        self.assertFalse(state.is_running())
        self.assertEqual(state.the_winner_id(), -1)

        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 1)))
        state = state.next_state(GomokuAction(1, (2, 1)))
        state = state.next_state(GomokuAction(1, (3, 1)))
        state = state.next_state(GomokuAction(1, (4, 1)))
        state = state.next_state(GomokuAction(1, (5, 1)))
        self.assertFalse(state.is_running())

        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 1)))
        state = state.next_state(GomokuAction(1, (1, 2)))
        state = state.next_state(GomokuAction(1, (1, 3)))
        state = state.next_state(GomokuAction(1, (1, 4)))
        state = state.next_state(GomokuAction(1, (1, 5)))
        self.assertFalse(state.is_running())

        # True
        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 4)))
        state = state.next_state(GomokuAction(1, (2, 3)))
        state = state.next_state(GomokuAction(1, (3, 2)))
        state = state.next_state(GomokuAction(1, (4, 1)))
        self.assertTrue(state.is_running())

        state = GomokuState()
        state = state.next_state(GomokuAction(1, (2, 2)))
        state = state.next_state(GomokuAction(1, (3, 3)))
        state = state.next_state(GomokuAction(1, (4, 4)))
        state = state.next_state(GomokuAction(1, (5, 5)))
        self.assertTrue(state.is_running())

        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 1)))
        state = state.next_state(GomokuAction(1, (3, 1)))
        state = state.next_state(GomokuAction(1, (4, 1)))
        state = state.next_state(GomokuAction(1, (5, 1)))
        self.assertTrue(state.is_running())

        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 1)))
        state = state.next_state(GomokuAction(1, (1, 2)))
        state = state.next_state(GomokuAction(1, (1, 3)))
        state = state.next_state(GomokuAction(1, (1, 5)))
        self.assertTrue(state.is_running())

    def test_get_all_available_pos(self):
        state = GomokuState()
        state = state.next_state(GomokuAction(1, (1, 1)))
        state = state.next_state(GomokuAction(1, (1, 2)))
        state = state.next_state(GomokuAction(1, (1, 5)))

        print(state.get_point_evaluation((1, 4), 1))


# class TestGomokuRunner(unittest.TestCase):
#     def test_create_game(self):
#         player1 = QLearningAIPlayer()
#         player2 = QLearningAIPlayer()
#         game = GomokuRunner(player1,player2)

#         game.play()

if __name__ == '__main__':

    unittest.main()
