import datetime
import pyperclip  # for clipboard functions.
import customtkinter as ctk

class Timestamper:
    def __init__(self):
        self.chosen_time = -1
        self.mode = ""
        self.inputDate = ""
        self.gui = ctk.CTk()
        
        self.gui.geometry("500x500")
        self.gui.title("Discord Timestamper")

        self.gui.grid_columnconfigure(0, weight=1) # weight = int, >= 0.
        # Determines how much widgets scale when window is resized. 
        # Weight=1 = fill all extra space from resizing. 
        # If a different row has a different number (say weight=2), then twice as much free space will be taken by the row with weight=2 as the row with weight=1.
        # Weight=0 = no filling extra space.
        self.gui.grid_rowconfigure(0, weight=1)

        self.entry_box = ctk.CTkEntry(self.gui, placeholder_text="Enter date", width=200, height=40) # make it exist
        self.entry_box.grid(row=0, column=0, sticky="ew", padx=50, pady=10) # place on grid (make visible)

        self.copy_button = ctk.CTkButton(self.gui, text="Copy to Clipboard", command=self.bt_copy_to_clipboard)
        self.copy_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.gui.mainloop()

    def bt_copy_to_clipboard(self):
        chosen_date = datetime.datetime.strptime(self.entry_box.get(), "%Y-%m-%d %H:%M:%S")
        unix_timestamp = int(chosen_date.timestamp())
        formatted_timestamp = f"<t:{unix_timestamp}:R>"

        print(f'"{chosen_date.strftime("%Y-%m-%d %H:%M:%S")}" has a Relative Discord timestamp of: {formatted_timestamp}\nCopying to clipboard...')
        pyperclip.copy(formatted_timestamp)
        print("Copied!")

    def bt_generate_timestamp(self):
        self.chosen_time = 355 
        # current rough idea: convert date string from input box into a datetime object, then call .timestamp(), then add formatting based on mode selected from gui (:R, :F, etc)



program = Timestamper()