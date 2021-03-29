
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
        self.play_button = ttk.Button(self.master, text="Spila", command=self.play)
        self.get_button.pack(padx=5, pady=5)
        self.nr_players = 0
        self.player_1 = None
        self.player_2 = None
        self.player_names = []

    def get_username(self):
        text = self.input_box.get()
        if self.nr_players == 0:
            self.player_names.append(text if text else "Leikmaður 1")
            self.player_1 = text if text else None
            self.input_box.delete(0, 'end')
            self.user_nr.set("Leikmaður 2")
            self.play_button.pack()
            self.get_button.config(text="Bæta við leikmanni")
            self.nr_players += 1
        elif self.nr_players == 1:
            self.player_names.append(text if text else "Leikmaður 2")
            self.player_2 = text if text else None
            self.input_box.delete(0, 'end')
            self.user_nr.set("Leikmaður 3")
            self.nr_players += 1
        elif self.nr_players == 2:
            self.player_names.append(text if text else "Leikmaður 3")
            self.input_box.delete(0, 'end')
            self.nr_players += 1
            self.user_nr.set("Leikmaður 4")
            self.get_button.destroy()
    
    def play(self):
        text = self.input_box.get()
        if self.nr_players == 1:
            self.player_names.append(text if text else "Leikmaður 2")
        elif self.nr_players == 2:
            self.player_names.append(text if text else "Leikmaður 3")
        else:
            self.player_names.append(text if text else "Leikmaður 4")
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


class DrawLetterWindow:

    def __init__(self, master, player_letters) -> None:
        self.master = master
        self.draw_frame = ttk.Frame(self.master)
        self.draw_frame.grid()
        self.label_var = StringVar(value="Veldu allt að sjö stafi\n til þess að skipta út\n(Skildir að með bili)")
        self.info_label = ttk.Label(textvariable=self.label_var, justify="center",)
        self.info_label.grid(row=0, columnspan=2, padx=10, pady=5)
        self.input_box = ttk.Entry()
        self.input_box.grid(row=1, columnspan=2, padx=10, pady=5)
        self.get_button = ttk.Button(self.master, text="Staðfesta", command=self.get_letters).grid(row=2, column=0, padx=5, pady=5)
        self.cancel_button = ttk.Button(self.master, text="Hætta", command=self.master.destroy).grid(row=2, column=1, padx=5, pady=5)
        self.player_letters = [sprite.letter for sprite in player_letters]
        self.letters_to_switch = []

    def get_letters(self):
        letters = self.input_box.get().upper().split(" ")
        if letters[0] == "":
            self.label_var.set("Ekkert valið")
        elif 0 < len(letters) < 8:
            for letter in letters:
                if letter not in self.player_letters:
                    self.label_var.set(f"Stafurinn {letter} er ekki á hendi")
                    self.input_box.delete(0, 'end')
                    self.letters_to_switch.clear()
                    return
                else:
                    self.letters_to_switch.append(letter)
            self.master.destroy()
        elif len(letters) >= 8:
            self.input_box.delete(0, 'end')
            self.label_var.set("Of margir stafir valdir")




        

if __name__ == '__main__':
    root = Tk() 
    e = DrawLetterWindow(root, ["I", "A", "B"])
    root.mainloop()
    print(e.letters_to_switch)