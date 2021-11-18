import tkinter


class CFrame(tkinter.Frame):
    def init(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def on_frame_exit(self):
        pass

    def quit(self):
        return self.instance.swap_frame("main_menu")

class Game:
    def quit(self):
        self.instance.swap_frame("main_menu")