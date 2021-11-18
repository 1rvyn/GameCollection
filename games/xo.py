import math
import tkinter
from tkinter import messagebox
from functools import partial
from models import CFrame, Game

# gets the models for the game
class XOButton(tkinter.Button):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.instance = args[0].instance
        self.claimed = False
        self.instance.current_game.buttons.append(self)
        self.id = len(self.instance.current_game.buttons)

class GameFrame(CFrame): # init frame
    def __init__(self, instance):
        self.instance = instance
        super().__init__(instance.tk)
        instance.tk.title("Xs and Os")
        # creates the matrix size and sets the buttons commands
        for i in range(self.instance.current_game.GRID_SIZE * self.instance.current_game.GRID_SIZE):
            button = XOButton(self, font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=partial(self.on_click, i))
            grid = self.instance.current_game.int_x_y_convert(i)
            button.grid(column=grid[0], row=grid[1])
        self.pack(padx=100, pady=50)
    # allows the buttons to rotate player each click
    def on_click(self, loc):
        cur_game = self.instance.current_game
        button = cur_game.buttons[loc]
        if button.claimed:
            # print("invalid placement")
            return messagebox.showerror("Invalid choice!", "That box is already selected, select a different one!")
        button.claimed = True
        button['text'] = cur_game.get_player()
        button.instance.current_game.check_win()
        button.instance.current_game.flip_to_next_player()
        # print("successfully placed")

class XandOsGame(Game):
    GRID_SIZE = 3 # 3x3 matrix
    def __init__(self, instance): # init game
        self.instance = instance
        self.instance.current_game = self
        self.clicked = True
        self.player = True
        self.buttons = list()
        self.instance.register_frame("xo_game", GameFrame)
        self.instance.swap_frame("xo_game")
        # game specific settings
    def flip_to_next_player(self):
        self.player = not self.player

    def check_win(self):
        winner = False
        win_patterns = ["012", "345", "678", "036", "147", "258", "048", "246"] # neat way to check if its a win
        for pattern in win_patterns:
            print("checking all win patter types to see if present in current matrix instance")
            pattern_nums = [int(pattern[0]), int(pattern[1]), int(pattern[2])]
            matrix = self.get_simple_matrix()
            c = [ matrix[pattern_nums[0]], matrix[pattern_nums[1]], matrix[pattern_nums[2]] ]
            if len(set(c)) == 1 and c[0] != '':
                self.toggle_all_buttons()
                for pat_val in pattern_nums:
                    button = self.buttons[int(pat_val)]
                    button.config(bg="green")
                print("there was a winner found")
                messagebox.showinfo("Winner!", f"Congratulations to {self.get_player()} wins")
                winner = True
                self.quit()
                break
        if not winner and str() not in self.get_simple_matrix():
        # error handler to check if its a tie as none of the win_patterns will be matched
            self.quit()
            return messagebox.showerror("Tie", "This game resulted in a tie!")


    # getters

    def get_player(self):
        return "X" if self.player else "O"

    def get_simple_matrix(self):
        return [x['text'] for x in self.buttons]

    def toggle_all_buttons(self):
        for button in self.buttons:
            cur_state = button["state"]
            if cur_state == tkinter.ACTIVE:
                button.config(state=tkinter.DISABLED)
            elif cur_state == tkinter.DISABLED:
                button.config(state=tkinter.ACTIVE)

    def int_x_y_convert(self, integer:int):
        y = math.floor(integer/self.GRID_SIZE)
        x = integer - (y*self.GRID_SIZE)
        return x, y
