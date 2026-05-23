from datetime import datetime  # Self-explanatory.
import pyperclip  # Clipboard functions.
import customtkinter as ctk  # GUI.
from typing import Callable


# This function might be deleted later.
def list_years():
    # ISSUE: If current date is before epoch, then a negative value occurs.
    # However this shouldn't matter because times before the epoch are impossible
    # to display on discord (without integer overflow).
    numYears = datetime.now().year - datetime.fromtimestamp(0).year

    year_list = [str(datetime.fromtimestamp(0).year + i) for i in range(numYears + 50)]

    return year_list


# Example code from CTk docs.
class FloatSpinbox(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        step_size: int | float = 1,
        command: Callable | None = None,
        **kwargs,
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.subtract_button_callback,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(
            self, width=width - (2 * height), height=height - 6, border_width=0
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.add_button_callback,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> float | None:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))


# END CTk docs example


class TimestamperApp(ctk.CTk):
    def __init__(self):

        ### Instance variables ###
        self.mode: str
        self.chosen_date: datetime

        ### GUI Setup ###
        super().__init__()
        self.geometry("500x500")
        self.title("Discord Timestamper")
        self.grid_columnconfigure(0, weight=1)
        # weight = int, >= 0.
        # Determines how much widgets scale when window is resized.
        # Weight=1 = fill all extra space from resizing.
        # If a different row has a different number (say weight=2), then twice as much free space will be taken by the row with weight=2 as the row with weight=1.
        # Weight=0 = no filling extra space.
        # self.gui.grid_rowconfigure(0, weight=1)

        ## Date entry box ##
        # Create widget.
        self.entry_box = ctk.CTkEntry(
            self,
            placeholder_text="Enter date",
            width=200,
            height=40,
        )
        # Place widget (entry box) on grid, making it visible.
        self.entry_box.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=50,
            pady=10,
        )

        ## Year drop-down Menu (combobox, to be reworked) ##
        self.year_input = ctk.CTkComboBox(
            self,
            values=list_years(),
        )
        self.year_input.grid(
            row=1,
            column=0,
            sticky="w",
            padx=50,
            pady=10,
        )

        ## "Copy to Clipboard" button ##
        self.copy_button = ctk.CTkButton(
            self,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
        )
        self.copy_button.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        self.test_spinbox = FloatSpinbox(self)
        self.test_spinbox.grid(row=3, column=0, sticky="nsew")

        self.mainloop()

    def copy_to_clipboard(self):
        chosen_date = datetime.strptime(self.entry_box.get(), "%Y-%m-%d %H:%M:%S")
        unix_timestamp = int(chosen_date.timestamp())
        formatted_timestamp = f"<t:{unix_timestamp}:R>"

        print(
            f'"{chosen_date.strftime("%Y-%m-%d %H:%M:%S")}" has a Relative Discord timestamp of: {formatted_timestamp}\nCopying to clipboard...'
        )
        pyperclip.copy(formatted_timestamp)
        print("Copied!")

    def generate_timestamp(self):
        pass


print(datetime.fromtimestamp(0))
program = TimestamperApp()


##### IDEAS #####
# 1. Add entry boxes for year, month, day, hour, minute, and second.
# 2. Add checkboxes for each discord timestamp mode (:R, :F, etc).
# 3. Add a text box for the timestamp to be displayed.
# 4. EITHER: Add a checkbox for whether to copy to clipboard upon generating timestamp,
#    OR: Use the existing "Copy to Clipboard" button, placed by the timestamp text box.
# 5. Add a "Generate Timestamp" button that does at it says.
