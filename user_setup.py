
from tkinter import StringVar, Tk
import tkinter.ttk as ttk

class UserSettings:


    def __init__(self, master) -> None:
        self.master = master
        self.user_frame = ttk.Frame(self.master)
        self.user_frame.pack()

        self.user_nr = StringVar(value="Leikmaður 1")

        self.user_nr_label = ttk.Label(textvariable=self.user_nr)
        self.user_nr_label.pack(padx=5, ipady=10)
        self.input_box = ttk.Entry()
        self.input_box.pack(padx=50, pady=10)
        self.get_button = ttk.Button(self.master, text="Áfram", command=self.get_username)
        self.get_button.pack(padx=5, pady=5)
        self.next_player = False
        self.player_1 = None
        self.player_2 = None

    def get_username(self):
        text = self.input_box.get()
        if not self.next_player:
            self.player_1 = text if text else None
            self.input_box.delete(0, 'end')
            self.get_button.config(text="Spila")
            self.user_nr.set("Leikmaður 2")
            self.next_player = True
        else:
            self.player_2 = text if text else None
            self.master.destroy()

class BlankLetterSet:

    def __init__(self, master) -> None:
        self.master = master
        self.blank_frame = ttk.Frame(self.master)
        self.blank_frame.pack()

        self.info_label = ttk.Label(text="Veldu eitt stafgildi fyrir\n auða stafaflís", justify='center')
        self.info_label.pack(padx=10, pady=5)
        self.input_box = ttk.Entry()
        self.input_box.pack(padx=50, pady=10)
        self.get_button = ttk.Button(self.master, text="Staðfesta", command=self.get_letter_val)
        self.get_button.pack(padx=5, pady=5)
        self.letter_val = None

    def get_letter_val(self):
        letter = self.input_box.get()
        if len(letter) == 1:
            self.letter_val = letter.upper()
            self.master.destroy()
        else:
            self.input_box.delete(0, 'end')

        

if __name__ == '__main__':
    root = Tk() 
    e = UserSettings(root)  
    root.mainloop() 