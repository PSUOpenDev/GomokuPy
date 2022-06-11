from GomokuRunner import GomokuRunner
from GomokuState import GomokuState
from GomokuPlayer import GomokuPlayer
from GomokuAction import GomokuAction
from HumanPlayer import HumanPlayer
from QLearningAIPlayer import QLearningAIPlayer
from AlphaBetaProneAIPlayer import AlphaBetaProneAIPlayer
from MinimaxAIPlayer import MinimaxAIPlayer
from GomokuFrontEnd import GomokuFrontEnd

if __name__ == '__main__':
    print("    GOMOKU GAME")
    print("#####################")
    frontend = GomokuFrontEnd()
    algo1 = 0 
    while not (algo1 == 1 or algo1 == 2 or algo1 ==3 or algo1 == 4):
        print("Choose  player 1")
        print(" 1) Minimax")
        print(" 2) Alpha Beta")
        print(" 3) Q-Learning")
        print(" 4) Human")
        try:
            algo1 = int(input('Choose a number: '))
        except ValueError:
            algo1 = 0
            print('Please only input digits')
    
    match algo1:
        case 1:
            player1 = MinimaxAIPlayer()
        case 2:
            player1 = AlphaBetaProneAIPlayer()
        case 3:
            player1 = QLearningAIPlayer()
            player1.load_file('player1.db')
        case 4:
            player1 = HumanPlayer(frontend)

    print("")
    
    algo2 = 0 
    while not (algo2 == 1 or algo2 == 2 or algo2 ==3 or algo2 ==4):
        print("Choose player 2")
        print(" 1) Minimax")
        print(" 2) Alpha Beta")
        print(" 3) Q-Learning")
        print(" 4) Human")
        try:
            algo2 = int(input('Choose a number: '))
        except ValueError:
            algo2 = 0
            print('Please only input digits')
    
    match algo2:
        case 1:
            player2 = MinimaxAIPlayer()
        case 2:
            player2 = AlphaBetaProneAIPlayer()
        case 3:
            player2 = QLearningAIPlayer()
            player2.load_file('player1.db')
        case 4:
            player2 = HumanPlayer(frontend)
    print("")
    
    number_of_game = -1 
    while number_of_game == -1:
        print("Choose number of game:")
        try:
            number_of_game = int(input('Type a number: '))
        except ValueError:
            number_of_game = -1
            print('Please only input digits')



    game = GomokuRunner(player1, player2, frontend)


    for _ in range(0,number_of_game):
        game.play(True)
        #input('Press any key to continue...')
    
