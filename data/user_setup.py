
from tkinter import StringVar, Tk
import tkinter.ttk as ttk


class UserSettings:


    def __init__(self, master) -> None:

        # Set the root/master for the window instance
        self.master = master
        self.user_frame = ttk.Frame(self.master)
        self.user_frame.pack()

        # Set a string variable for the user label
        self.user_nr = StringVar(value="Leikmaður 1")

        # Initalize window's functionality
        self.user_nr_label = ttk.Label(textvariable=self.user_nr)
        self.input_box = ttk.Entry()
        self.get_button = ttk.Button(self.master, text="Áfram", command=self.get_username)
        self.play_button = ttk.Button(self.master, text="Spila", command=self.play)

        # Pack functionality into the frame
        self.user_nr_label.pack(padx=5, ipady=10)
        self.input_box.pack(padx=50, pady=10)
        self.get_button.pack(padx=5, pady=5)

        # Initialize variables for player information 
        self.nr_players = 0
        self.player_names = []

    def get_username(self):
        """Gets information from the player entry"""

        text = self.input_box.get()

        # Add first player
        if self.nr_players == 0:
            
            # Get the user input for player #1 and set it to a default
            # if nothing is entered
            self.player_names.append(text if text else "Leikmaður 1")
            self.player_1 = text if text else None

            # Clear the input box and set the label variable to the next player
            self.input_box.delete(0, 'end')
            self.user_nr.set("Leikmaður 2")

            # Pack a new button for playing the game since 2 players are enough
            self.play_button.pack(pady=10)

            # Rename the initial button and increment the player number
            self.get_button.config(text="Bæta við leikmanni")
            self.nr_players += 1
    
        # Add second player
        elif self.nr_players == 1:

            # This block of code does the same as the last one except
            # it does not change any of the button properties
            self.player_names.append(text if text else "Leikmaður 2")
            self.player_2 = text if text else None
            self.input_box.delete(0, 'end')
            self.user_nr.set("Leikmaður 3")
            self.nr_players += 1

        # Add third player
        elif self.nr_players == 2:

            self.player_names.append(text if text else "Leikmaður 3")
            self.input_box.delete(0, 'end')
            self.nr_players += 1
            self.user_nr.set("Leikmaður 4")

            # If a third player has been added we destroy the 
            # "add more players" button
            self.get_button.destroy()
    

    def play(self):
        """Closes the current window and starts the game"""

        # This funtion adds the current user input to the player name
        # list and terminates the window. This button is not available
        # for the player 1 choice.
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

        # Set the root/master for the window instance
        self.master = master
        self.blank_frame = ttk.Frame(self.master)
        self.blank_frame.pack()

        # Initalize window's functionality
        self.info_label = ttk.Label(text="Veldu eitt stafgildi fyrir\n auða stafaflís", justify='center')
        self.input_box = ttk.Entry()
        self.get_button = ttk.Button(self.master, text="Staðfesta", command=self.get_letter_val)

        # Pack functionality into the frame
        self.info_label.pack(padx=10, pady=5)
        self.input_box.pack(padx=50, pady=10)
        self.get_button.pack(padx=5, pady=5)

        # Set the blank letter value to None
        self.letter_val = None


    def get_letter_val(self):
        """Get the chosen value from the input box"""

        letter = self.input_box.get()
        if len(letter) == 1:
            self.letter_val = letter.upper()
            self.master.destroy()

        else:
            # If nothing is in the input box or the string is longer
            # than 1 letter the input box resets
            self.input_box.delete(0, 'end')


class DrawLetterWindow:

    def __init__(self, master, player_letters) -> None:

        # Set the root/master for the window instance
        self.master = master
        self.draw_frame = ttk.Frame(self.master)
        self.draw_frame.grid()

        # Set a string variable for the instruction label
        self.label_var = StringVar(value="Veldu allt að sjö stafi\n til þess að skipta út\n(Skildir að með bili)")

        # Initalize window's functionality
        self.info_label = ttk.Label(textvariable=self.label_var, justify="center",)
        self.input_box = ttk.Entry()
        self.get_button = ttk.Button(self.master, text="Staðfesta", command=self.get_letters)
        self.cancel_button = ttk.Button(self.master, text="Hætta", command=self.master.destroy)

        # Position the functionality into the frame
        self.info_label.grid(row=0, columnspan=2, padx=10, pady=5)
        self.input_box.grid(row=1, columnspan=2, padx=10, pady=5)
        self.get_button.grid(row=2, column=0, padx=5, pady=5)
        self.cancel_button.grid(row=2, column=1, padx=5, pady=5)

        # Copy the player letters
        self.player_letters = [sprite.letter for sprite in player_letters]
        self.letters_to_switch = []

    def get_letters(self):
        """Get the letters to switch from the input box"""

        letters = self.input_box.get().upper().split(" ")
        
        if letters[0] == "":
            self.label_var.set("Ekkert valið")
        
        # If the number of letters chosen are in line with the number on hand
        elif 0 < len(letters) <= len(self.player_letters):
            for letter in letters:

                # If a letter that is not on hand is chosen an error pops up
                if letter not in self.player_letters:
                    self.label_var.set(f"Stafurinn {letter} er ekki á hendi")
                    self.input_box.delete(0, 'end')
                    self.letters_to_switch.clear()
                    return
                
                # Otherwise the letters are saved in a class variable
                # to be accessed later
                else:
                    self.letters_to_switch.append(letter)
            
            # The window is closed if everything goes right
            self.master.destroy()
        

        elif len(letters) >= 8:
            self.input_box.delete(0, 'end')
            self.label_var.set("Of margir stafir valdir")




        

if __name__ == '__main__':
    root = Tk() 
    e = DrawLetterWindow(root, ["I", "A", "B"])
    root.mainloop()
    print(e.letters_to_switch)