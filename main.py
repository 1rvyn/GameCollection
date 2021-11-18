import _tkinter
import sys
import tkinter
from tkinter import messagebox
from models import CFrame
from games import xo, reaction, number_matching
from saves import Saves


class MainMenuFrame(CFrame):
    def init(self, *args, **kwargs):
        self.instance.tk.title("Irvyn Hall Games")
        username = tkinter.Entry(self, font=("Helvetica", 10))
        username.insert(0, self.instance.username)
        username.pack()
        self.instance.storage['username_label'] = username
        title = tkinter.Label(self, text="Irvyn Hall Games", font=("Helvetica", 20), fg="red")
        title.pack(padx=10, pady=20)
        xo_game_btn = tkinter.Button(self, text="Xs and Os", command=lambda: self.instance.start_game("xo"))
        xo_game_btn.pack(padx=6, pady=2)
        rt_game_btn = tkinter.Button(self, text="Reaction Times", command=lambda: self.instance.start_game("reaction_time"))
        rt_game_btn.pack(padx=6, pady=2)
        other_game_btn = tkinter.Button(self, text="Number Matching", command=lambda: self.instance.start_game("number_match"))
        other_game_btn.pack(padx=6, pady=2)
        self.pack(padx=100, pady=50)
        # all the needed tkinter settings + setting the button commands to launch their specified games
    def __init__(self, instance):
        try:
            self.instance = instance
            super().__init__(instance.tk)
        except:
            messagebox.showerror("Error", "An error occurred while trying to load the main menu, please restart the application.")
            sys.exit(1)
        # a little error handler

    def on_frame_exit(self):
        self.instance.username = self.instance.storage['username_label'].get()
        # when leaving it sets the text in the instance.storage field to their username
class Instance:
    """Initializing the main instance class"""
    def __init__(self):
        try:
            self.tk = tkinter.Tk()
            fp = r'assets/icon.ico'
            try:
                self.tk.iconbitmap(fp)
            except _tkinter.TclError:
                messagebox.showerror("Error!", f"File not found: '{fp}'")
                return
            # error handling for my little I H G logo :)
            self.current_frame = None
            self.saves = Saves("saves.json")
            self.username = "username"
            self.storage = dict()
            self.frames = dict()
            self.frame_classes = dict()
            self.register_frame("main_menu", MainMenuFrame)
            self.swap_frame("main_menu")
        except:
            sys.exit(1)
        # larger error handler for loading the instance and settings related to all games

    """Displays/switches to the specified registered frame"""
    def swap_frame(self, frame_name):
        frame_class = self.frame_classes.get(frame_name)
        if frame_class:
            if self.current_frame:
                self.current_frame.on_frame_exit()
                self.current_frame.destroy()
            self.current_frame = frame_class(self)
            self.frames[frame_name] = self.current_frame

    """Registers the Frame for use by swap_frame()"""
    def register_frame(self, frame_name, frame_class):
        self.frame_classes[frame_name] = frame_class

    """Starts the specified game"""
    def start_game(self, game:str):
        try:
            if game == "xo":
                xo.XandOsGame(self)
                # print("starting XandO's")
            elif game == "reaction_time":
                reaction.ReactionTimeGame(self)
                # print("starting Reaction time game")
            elif game == "number_match":
                number_matching.NumberMatchingGame(self)
                # print("starting the number matchin game")
            else:
                raise ValueError("Invalid game name specified.")
                # print("testing the error handling for new games that are named incorrectly")
        # error handler for if i want to add more games in the future
        except Exception as e:
            messagebox.showerror("Error", str(e))
        # will print the exception out in a nice windows error box if one is found

i = Instance()
i.tk.mainloop()
