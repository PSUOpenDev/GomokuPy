'''
CS 441 AI Spring 2022
Group: Tri Le , Phuoc Nguyen
Final Project : Gomoku Game
'''
from tkinter import *
import numpy as np
import copy

# DIMENSION OF BOARD
MAX_GRID_SIZE = 20
BOARD_WIDTH = 700
BOARD_HEIGHT = 700
FRAME_GAP = 35

# BOARD GRID CONSTANT
MAX_GRID_SIZE = MAX_GRID_SIZE - 1
MARGIN_X = BOARD_WIDTH / 10
MARGIN_Y = BOARD_HEIGHT / 10
BOARD_GAP_X = (BOARD_WIDTH - 2 * MARGIN_X) / MAX_GRID_SIZE
BOARD_GAP_Y = (BOARD_HEIGHT - 2 * MARGIN_Y) / MAX_GRID_SIZE

# PLAYER RADIUS
RADIUS = (BOARD_GAP_X * 0.9) / 2

# INITIALIZE
POSITION = [None, None]
INPUT_POS = [None, None]
BOARD_X_COORD = []
BOARD_Y_COORD = []
CURRENT_X1_COORD = []
CURRENT_Y1_COORD = []
CURRENT_X2_COORD = []
CURRENT_Y2_COORD = []

# Create GUI Object
GOMOKU_GUI = Tk()
GOMOKU_GUI.title("GOMOKU")
GOMOKU_GUI.config(bg="#f7f5ad")


class Widget:
    def __init__(self, tkinter_gui):
        self.gomoku_interface = tkinter_gui
        self.gomoku_widget = None

    def create_widget(self):

        # GOMOKU WIDGET
        self.gomoku_widget = Canvas(
            self.gomoku_interface,
            bd=2,
            background="#f7f5ad",
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
        )
        self.gomoku_widget.pack()

    def widget(self):
        return self.gomoku_widget

    def draw_circle(self, loc_x, loc_y, r, fill="",outline_color="",  w=1):
        self.gomoku_widget.create_oval(
            loc_x - r,
            loc_y - r,
            loc_x + r,
            loc_y + r,
            fill=fill,
            width=w,
            outline = outline_color
            
        )

    def draw_rec(self, x0, y0, x1, y1, fill=""):
        self.gomoku_widget.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            fill=fill,
            width=0
        )


class GomokuFrontEnd:
    def __init__(self):
        self.GOMOKU_WIDGET_OBJ = Widget(GOMOKU_GUI)
        self.GOMOKU_WIDGET_OBJ.create_widget()
        self.GomokuWidget = self.GOMOKU_WIDGET_OBJ.widget()
        

        self.board_grid = copy.deepcopy(
            np.zeros((MAX_GRID_SIZE + 1, MAX_GRID_SIZE + 1)))
        self.turn_order = 1
        self.player_last_turn = "red"
        self.player_turn = "red"
        self.player_new_turn = "pink"
        self.winner = None
        self.list_x_coord_player_1 = []
        self.list_y_coord_player_1 = []
        self.list_x_coord_player_2 = []
        self.list_y_coord_player_2 = []
        self.text_displayed = None
        self.last_pos_x = -1
        self.last_pos_y = -1

    def pick_location(self, loc_x, loc_y):
        if loc_x is None or loc_y is None:
            return False
        elif self.board_grid[loc_y - 1][loc_x - 1] == 0:
            return True

    def display_winner(self,mess):
        self.GOMOKU_WIDGET_OBJ.draw_rec(
            BOARD_WIDTH / 2 - 100,
            BOARD_HEIGHT - 40,
            BOARD_WIDTH / 2  + 100,
            BOARD_HEIGHT,
            fill="#f7f5ad"
        )

        self.text_displayed = self.GomokuWidget.create_text(
                BOARD_WIDTH / 2,
                BOARD_HEIGHT - 20,
                text=mess,
                font="Helvetica 15 bold",
                fill="blue"
            )
        self.GomokuWidget.update()

    def draw_winning_points(self,list_point):
        for point in list_point:
            self.GOMOKU_WIDGET_OBJ.draw_circle(
                MARGIN_X + BOARD_GAP_X * (point[0]),
                MARGIN_Y + BOARD_GAP_Y * (point[1]),
                r=RADIUS,
                fill="",
                outline_color = "blue", w = 3
            )
            self.GomokuWidget.update()

    def display_text_player(self):
        if self.player_turn == "black":
            player = 1
            fill_text = self.player_turn
        else:
            player = 2
            fill_text = "red"

        if self.winner is None:
            return self.GomokuWidget.create_text(
                BOARD_WIDTH / 2,
                BOARD_HEIGHT - 20,
                text="Player " + str(player) + "'s next turn",
                font="Helvetica 15 bold",
                fill=fill_text
            )
        else:
            return self.GomokuWidget.create_text(
                BOARD_WIDTH / 2,
                BOARD_HEIGHT - 20,
                text="Player " + str(player) + " WINS!",
                font="Helvetica 15 bold",
                fill=fill_text
            )

    def fill_grid(self):
        self.GOMOKU_WIDGET_OBJ.draw_rec(
            0,
            0,
            BOARD_WIDTH,
            BOARD_HEIGHT,
            fill="#f7f5ad"
        )
        for m in range(1, MAX_GRID_SIZE + 2):
            for n in range(1, MAX_GRID_SIZE + 2):
                BOARD_X_COORD.append(m)
                BOARD_Y_COORD.append(n)
                CURRENT_X1_COORD.append(
                    (m - 1) * BOARD_GAP_X + MARGIN_X - RADIUS)
                CURRENT_Y1_COORD.append(
                    (n - 1) * BOARD_GAP_Y + MARGIN_Y - RADIUS)
                CURRENT_X2_COORD.append(
                    (m - 1) * BOARD_GAP_X + MARGIN_X + RADIUS)
                CURRENT_Y2_COORD.append(
                    (n - 1) * BOARD_GAP_Y + MARGIN_Y + RADIUS)

    def draw_grid(self):
        for f in range(MAX_GRID_SIZE + 1):
            # DRAW VERTICAL LINE
            self.GomokuWidget.create_text(
                 MARGIN_X + f * BOARD_GAP_X,
                MARGIN_Y- 30,
                text="{0}".format(f),
                font="Helvetica 15 bold",
                fill="black"
            )
            self.GomokuWidget.create_line(
                MARGIN_X + f * BOARD_GAP_X,
                MARGIN_Y,
                MARGIN_X + f * BOARD_GAP_X,
                MARGIN_Y + BOARD_GAP_Y * MAX_GRID_SIZE)

            # DRAW HORIZONTAL LINE
            self.GomokuWidget.create_text(
                MARGIN_X - 30,
                MARGIN_Y + f * BOARD_GAP_Y,
                text="{0}".format(f),
                font="Helvetica 15 bold",
                fill="black"
            )
            self.GomokuWidget.create_line(
                MARGIN_X,
                MARGIN_Y + f * BOARD_GAP_Y,
                MARGIN_X + BOARD_GAP_X * MAX_GRID_SIZE,
                MARGIN_Y + f * BOARD_GAP_Y
            )

    def add_action(self, point):
        global POSITION

        POSITION = point[0]+1, point[1]+1
        print('=>{0}'.format(point))
        self.show_game()
        POSITION = None

    def init(self):
        self.board_grid = copy.deepcopy(
            np.zeros((MAX_GRID_SIZE + 1, MAX_GRID_SIZE + 1)))
        self.turn_order = 1
        self.player_last_turn = "red"
        self.player_turn = "red"
        self.player_new_turn = "pink"
        self.winner = None
        self.list_x_coord_player_1 = []
        self.list_y_coord_player_1 = []
        self.list_x_coord_player_2 = []
        self.list_y_coord_player_2 = []
        self.text_displayed = None
        self.last_pos_x = -1
        self.last_pos_y = -1

        self.fill_grid()
        self.draw_grid()
        self.text_displayed = self.display_text_player()

        self.GomokuWidget.update()

    def show_game(self):
        global POSITION
        

        # User pick a location
        pos_x, pos_y = POSITION
        location_picked = self.pick_location(loc_x=pos_x, loc_y=pos_y)

        if location_picked:
            self.GomokuWidget.delete(self.text_displayed)

            if self.last_pos_x != -1 and self.last_pos_y != -1:
                self.GOMOKU_WIDGET_OBJ.draw_circle(
                    MARGIN_X + BOARD_GAP_X * (self.last_pos_x - 1),
                    MARGIN_Y + BOARD_GAP_Y * (self.last_pos_y - 1),
                    r=RADIUS,
                    fill=self.player_last_turn
                )

            self.GOMOKU_WIDGET_OBJ.draw_circle(
                MARGIN_X + BOARD_GAP_X * (pos_x - 1),
                MARGIN_Y + BOARD_GAP_Y * (pos_y - 1),
                r=RADIUS,
                fill=self.player_new_turn
            )
            self.last_pos_x = pos_x
            self.last_pos_y = pos_y
            self.player_last_turn = self.player_turn

            if self.turn_order % 2 == 1:
                self.list_x_coord_player_2.append(pos_x)
                self.list_y_coord_player_2.append(pos_y)
                self.board_grid[pos_y - 1][pos_x - 1] = 2
                self.player_turn = "black"
                self.player_new_turn = "gray"

            elif self.turn_order % 2 == 0:
                self.list_x_coord_player_1.append(pos_x)
                self.list_y_coord_player_1.append(pos_y)
                self.board_grid[pos_y - 1][pos_x - 1] = 1
                self.player_turn = "red"
                self.player_new_turn = "pink"

            self.text_displayed = self.display_text_player()

            self.turn_order += 1

            self.GomokuWidget.update()
            # Condition to stop
            #self.condition += 1
            # if self.condition == 10:
            #    self.winner = self.player_turn
        # else:
            # self.GomokuWidget.delete(self.text_displayed)
    def human_player_action(self):
        global INPUT_POS
        self.GomokuWidget.update()
        temp = INPUT_POS
        INPUT_POS = [None,None]
        return temp

    def init_human_player(self): 
        
        self.GomokuWidget.bind("<Button-1>", on_mouse_click)

def quit_game():
    GOMOKU_GUI.destroy()


quit_game_btn = Button(
    GOMOKU_GUI,
    text="QUIT",
    command=quit_game,
    bg="black",
    fg="white"
)
quit_game_btn.place(
    x=BOARD_WIDTH / 2 * 0.5,
    y=BOARD_HEIGHT,
    height=RADIUS * 2,
    width=RADIUS * 4
)
quit_game_btn.pack()


def get_clicked_location(x, y):
    x_value = None
    y_value = None

    for k in range(len(CURRENT_X1_COORD)):
        if CURRENT_X1_COORD[k] < x < CURRENT_X2_COORD[k]:
            x_value = BOARD_X_COORD[k]

        if CURRENT_Y1_COORD[k] < y < CURRENT_Y2_COORD[k]:
            y_value = BOARD_Y_COORD[k]

    return x_value, y_value


def on_mouse_click(event):
    global INPUT_POS

    # Get the x-coord and y-coord
    x_value = event.x
    y_value = event.y
    INPUT_POS = get_clicked_location(x_value, y_value)



#
# RUN PROGRAM
#main_gomoku = GomokuFrontend()
# main_gomoku.show_game()
