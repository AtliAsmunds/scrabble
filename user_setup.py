
from tkinter import StringVar, Tk
import tkinter.ttk as ttk

class UserSettings:

    def __init__(self, master) -> None:
        self.master = master
        self.user_frame = ttk.Frame(master)
        self.user_frame.pack()

        self.user_nr = StringVar(value="Leikmaður 1")

        self.user_nr_label = ttk.Label(textvariable=self.user_nr)
        self.user_nr_label.pack(padx=5, ipady=10)
        self.input_box = ttk.Entry()
        self.input_box.pack(padx=50, pady=10)
        self.get_button = ttk.Button(master, text="Áfram", command=self.get_username)
        self.get_button.pack(padx=5, pady=5)
        self.player_1 = None
        self.player_2 = None

    def get_username(self):
        text = self.input_box.get()
        if not self.player_1:
            self.player_1 = text
            self.input_box.delete(0, 'end')
            self.get_button.config(text="Spila")
            self.user_nr.set("Leikmaður 2")
        elif not self.player_2:
            self.player_2 = text
            self.master.destroy()
        return text
    

if __name__ == '__main__':
    root = Tk() 
    e = UserSettings(root)  
    root.mainloop() 