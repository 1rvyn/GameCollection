import ctypes
import math
import random
import string
import tkinter
from functools import partial
from tkinter import messagebox
from models import CFrame, Game

# gets the models for the game
class NumberButton(tkinter.Button):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.instance = args[0].instance
        self.instance.current_game.buttons.append(self)
        self.id = len(self.instance.current_game.buttons)


class GameFrame(CFrame):
    def __init__(self, instance): # init frame
        self.instance = instance
        self.game = self.instance.current_game
        super().__init__(instance.tk)
        instance.tk.title("Number Matching")
        # creates the matrix size and sets the buttons commands
        for i in range(self.game.ROWS*self.game.COLUMNS):
            button = NumberButton(self, font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=partial(self.on_click, i))
            grid = self.instance.current_game.int_x_y_convert(i)
            button.grid(column=grid[0], row=grid[1])
        self.pack(padx=100, pady=50)
        # allows for one button to be shown then the next button to be shown has to be the same number otherwise they all turn over
    def on_click(self, loc):
        btn = self.game.buttons[loc]
        btn['text'] = self.game.map[loc]
        self.game.active_button_counter += 1
        btn.config(state=tkinter.DISABLED)
        if self.game.active_button_counter % 2 == 0:
            if self.game.previous_button['text'] != btn['text']:
                messagebox.showinfo("Wrong!", f"Incorrect Match. Resetting.")
                # print ("incorrect match")
                return self.game.reset_game()
            self.game.pairs.append([self.game.previous_button, btn])
            # print("correct match")
            self.game.previous_button = None
        else:
            self.game.previous_button = btn
        if len(self.game.pairs)*2 == len(self.game.buttons): # checks if the amount of pairs there are = total amount of buttons and if true you win
            ctypes.windll.user32.MessageBoxW(0, f"Congratulations, you have won!", "Winner!", 0)
            return self.quit()
        # settings for generating the buttons and their correlating digits
class NumberMatchingGame(Game): # init game
    ROWS = 3
    COLUMNS = 4
    DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    def __init__(self, instance):
        self.map = random.sample(string.digits, int(self.ROWS * self.COLUMNS/2))
        self.map.extend(self.map)
        random.shuffle(self.map)
        self.buttons = list()
        self.instance = instance
        self.instance.current_game = self
        self.instance.register_frame("number_matching", GameFrame)
        self.instance.swap_frame("number_matching")
        self.active_button_counter = 0
        self.previous_button = None
        self.pairs = list()
        # game specific settings
    def int_x_y_convert(self, integer:int):
        y = math.floor(integer/self.COLUMNS)
        x = integer - (y*self.COLUMNS)
        return x, y
    # re-draw the buttons and re-create the pairs
    def reset_game(self):
        for b in self.buttons:
            b.config(state=tkinter.ACTIVE)
            b["text"] = str()
        self.pairs = list()

    def get_simple_matrix(self):
        return [x['text'] for x in self.buttons]
