import ctypes
import datetime
import random
import threading
import time
import tkinter
from functools import partial
from tkinter import messagebox
from models import CFrame, Game


# i want everything from  tkinter.Button to be inherited into ReactionButton
class ReactionButton(tkinter.Button):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.instance = args[
            0].instance  # sets the super class to have instance attributes/variables that the tkiner.Button class doesnt already have
        self.instance.current_game.buttons.append(
            self)  # i also want to add these button objects to the current games list of buttons
        self.id = len(self.instance.current_game.buttons)


class GameFrame(CFrame):
    def __init__(self, instance):  # init gameframe (buttons)
        self.instance = instance
        self.game = self.instance.current_game
        super().__init__(instance.tk)
        instance.tk.title("Reaction Time")

        hs = tkinter.Label(self, text=f"High Score: {self.game.get_high_score()}MS", font=("Helvetica", 10), fg="red")  # creates the high score label
        hs.grid(column=0, row=0)

        light = ReactionButton(self, height=6, width=12, bg="red", state=tkinter.DISABLED)  # sets the reactionButton to disabled on entry
        light.grid(column=0, row=1)

        btn = ReactionButton(self, text="Click when\nthe left box\nturns GREEN", height=6, width=12, bg="SystemButtonFace", command=partial(self.on_click))
        btn.grid(column=1, row=1)
        # gives the button a little hint message on it
        self.pack(padx=100, pady=50)

    def on_click(self):
        now = datetime.datetime.utcnow().timestamp()  # creates a now variable which is the current time
        if not self.instance.current_game.is_safe():
            #  print("user clicked before is_safe method was called aka before the button turned green")
            return messagebox.showerror("Too early!", "The left box hasnt even turned green yet!")
        if self.game.timer_green_time:  # checks to see if the button was green on the click
            ms_float = round((now - self.game.timer_green_time) * 1000, 2)  # little math equation to find out the time from when it went green to when it was clicked
            ms = f"{ms_float} MS"
            if ms_float > self.game.WIN_AMOUNT:  # if the users current score was more than the win amount it wont take it in as it was too late
                messagebox.showerror("Try Again.", f"Your reaction time was {ms}. To win, try again until you achieve {self.game.WIN_AMOUNT}ms or faster.")
                return self.game.reset_game()
            if (ms_float < self.game.WIN_AMOUNT) and (ms_float < self.game.get_high_score()):
                # if the users score was less than the win amount AND it was less than the current high score
                # it will take it and set it to the current high score then quit the game
                self.instance.saves.save_score(self.game.SAVES_NAME, self.instance.username, ms_float)
                ctypes.windll.user32.MessageBoxW(0, f"Congratulations, your reaction time was {ms}!", "Winner!", 0)
                return self.quit()
            if self.game.get_high_score() == 0:
                # this is for the new usernames as the default high score value is 0
                self.instance.saves.save_score(self.game.SAVES_NAME, self.instance.username, ms_float)
                ctypes.windll.user32.MessageBoxW(0, f"This was your first score, setting your highscore to {ms}!", "Try to beat it!", 0)
                return self.quit()
            else:  # if all the above conditions arent met this runs
                messagebox.showerror("Try Again.", f"Your reaction time was {ms}. To win, try again until you achieve {self.game.get_high_score()}ms or faster.")
                return self.game.reset_game()


class ReactionTimeGame(Game):
    WIN_AMOUNT = 4000  # this is the minimum time for a score to be counted
    GREEN_LIGHT_HEX = '#0CFF00'
    SAVES_NAME = "reaction_game_scores"

    def __init__(self, instance):  # init game
        self.timer_green_time = 0
        self.buttons = list()
        self.instance = instance
        self.instance.current_game = self
        self.instance.register_frame("reaction_game", GameFrame)
        self.instance.swap_frame("reaction_game")
        self.start_light_runner()
        # game specific settings

    def _light_runner(self):  # this is a random delay from where the light goes from red to green
        time.sleep(random.randint(2, 4))
        self.buttons[0]['background'] = self.GREEN_LIGHT_HEX  # makes the button green once the random delay has happened
        self.timer_green_time = datetime.datetime.utcnow().timestamp()  # gets the time from when its green

    def start_light_runner(self):
        t = threading.Thread(target=self._light_runner)  # sets the _light_runner function to be ran on a seperate daemon thread
        # print("setting the light countdown function to run on a daemon thread")
        t.setDaemon(True)
        t.start()

    def is_safe(self):
        # print("is_safe is now true - allowing for a user to react/input")
        # this just checks if a player can click by seeing if the button is green
        return self.buttons[0]['background'] == self.GREEN_LIGHT_HEX

    def reset_game(self):
        # function to reset - makes the button red resets the green button timer and restarts light runner
        self.timer_green_time = 0
        self.buttons[0].config(bg="red")
        self.start_light_runner()
        # print("game is finished, restarting the countdown timer!")

    def get_high_score(self):
        # gets the current high score
        s = self.instance.saves.get([self.SAVES_NAME, self.instance.username])
        if not s:
            return 0
        return s
