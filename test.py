# Dependencies
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


class WIDGET:
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

    def draw_circle(self, loc_x, loc_y, r, fill=""):
        self.gomoku_widget.create_oval(
            loc_x - r,
            loc_y - r,
            loc_x + r,
            loc_y + r,
            fill=fill,
            width=1
        )


GOMOKU_WIDGET_OBJ = WIDGET(GOMOKU_GUI)
GOMOKU_WIDGET_OBJ.create_widget()
GOMOKU_WIDGET = GOMOKU_WIDGET_OBJ.widget()


class GOMOKUGUI:
    def __init__(self):
        self.board_grid = copy.deepcopy(np.zeros((MAX_GRID_SIZE + 1, MAX_GRID_SIZE + 1)))
        self.turn_order = 1
        self.player_turn = "red"
        self.winner = None
        self.list_x_coord_player_1 = []
        self.list_y_coord_player_1 = []
        self.list_x_coord_player_2 = []
        self.list_y_coord_player_2 = []

    def pick_location(self, loc_x, loc_y):
        if loc_x is None or loc_y is None:
            return False
        elif self.board_grid[loc_y - 1][loc_x - 1] == 0:
            return True

    def display_text_player(self):
        if self.player_turn == "black":
            player = 1
            fill_text = self.player_turn
        else:
            player = 2
            fill_text = "red"

        if self.winner is None:
            return GOMOKU_WIDGET.create_text(
                BOARD_WIDTH / 2,
                BOARD_HEIGHT - 20,
                text="Player " + str(player) + "'s next turn",
                font="Helvetica 15 bold",
                fill=fill_text
            )
        else:
            return GOMOKU_WIDGET.create_text(
                BOARD_WIDTH / 2,
                BOARD_HEIGHT - 20,
                text="Player " + str(player) + " WINS!",
                font="Helvetica 15 bold",
                fill=fill_text
            )

    def fill_grid(self):
        for m in range(1, MAX_GRID_SIZE + 2):
            for n in range(1, MAX_GRID_SIZE + 2):
                BOARD_X_COORD.append(m)
                BOARD_Y_COORD.append(n)
                CURRENT_X1_COORD.append((m - 1) * BOARD_GAP_X + MARGIN_X - RADIUS)
                CURRENT_Y1_COORD.append((n - 1) * BOARD_GAP_Y + MARGIN_Y - RADIUS)
                CURRENT_X2_COORD.append((m - 1) * BOARD_GAP_X + MARGIN_X + RADIUS)
                CURRENT_Y2_COORD.append((n - 1) * BOARD_GAP_Y + MARGIN_Y + RADIUS)

    def draw_grid(self):
        for f in range(MAX_GRID_SIZE + 1):
            # DRAW VERTICAL LINE
            GOMOKU_WIDGET.create_line(
                MARGIN_X + f * BOARD_GAP_X,
                MARGIN_Y,
                MARGIN_X + f * BOARD_GAP_X,
                MARGIN_Y + BOARD_GAP_Y * MAX_GRID_SIZE)

            # DRAW HORIZONTAL LINE
            GOMOKU_WIDGET.create_line(
                MARGIN_X,
                MARGIN_Y + f * BOARD_GAP_Y,
                MARGIN_X + BOARD_GAP_X * MAX_GRID_SIZE,
                MARGIN_Y + f * BOARD_GAP_Y
            )

    def run_game(self):
        self.fill_grid()
        self.draw_grid()

        text_displayed = self.display_text_player()

        # LIST_POSITION = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (5, 5)]

        c = 0
        while self.winner is None:
            GOMOKU_WIDGET.update()

            # User pick a location
            pos_x, pos_y = POSITION
            location_picked = self.pick_location(loc_x=pos_x, loc_y=pos_y)

            if location_picked:
                GOMOKU_WIDGET.delete(text_displayed)

                GOMOKU_WIDGET_OBJ.draw_circle(
                    MARGIN_X + BOARD_GAP_X * (pos_x - 1),
                    MARGIN_Y + BOARD_GAP_Y * (pos_y - 1),
                    r=RADIUS,
                    fill=self.player_turn
                )

                if self.turn_order % 2 == 1:
                    self.list_x_coord_player_2.append(pos_x)
                    self.list_y_coord_player_2.append(pos_y)
                    self.board_grid[pos_y - 1][pos_x - 1] = 2
                    self.player_turn = "black"

                elif self.turn_order % 2 == 0:
                    self.list_x_coord_player_1.append(pos_x)
                    self.list_y_coord_player_1.append(pos_y)
                    self.board_grid[pos_y - 1][pos_x - 1] = 1
                    self.player_turn = "red"

                text_displayed = self.display_text_player()

                self.turn_order += 1

                # Condition to stop
                c += 1
                if c == 10:
                    self.winner = self.player_turn

        GOMOKU_WIDGET.delete(text_displayed)


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
    global POSITION

    # Get the x-coord and y-coord
    x_value = event.x
    y_value = event.y
    POSITION = get_clicked_location(x_value, y_value)
    print(POSITION)


GOMOKU_WIDGET.bind("<Button-1>", on_mouse_click)

# RUN PROGRAM
main_gomoku = GOMOKUGUI()
main_gomoku.run_game()