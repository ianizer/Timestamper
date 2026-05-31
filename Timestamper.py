import sys
from time import localtime  # To give exit codes.
from PySide6.QtCore import Qt, QDateTime, QDate  # For alignment and other flags.
from PySide6.QtGui import QCursor  # For tooltips.
from PySide6.QtWidgets import *  # Main GUI components.
import datetime as dt  # For dates, times, and timezones.
import pyperclip  # Clipboard functions.
from typing import cast  # To prevent false red underlines by VS Code.


# QWidget used as QMainWindow's features are unnecessary for this app.
class TimestamperUI(QWidget):
    DEFAULT_MIN_DATE = QDate(1970, 1, 1)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Builds UI and initializes properties."""

        self.setWindowTitle("Timestamper")
        self.setMinimumSize(300, 300)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        ### Properties and frequently-used local variables ###

        # .astimezone(), when called without args, gives a datetime object with
        # the computer's local timezone.
        now = dt.datetime.now().astimezone()

        # Let seconds be 0 since the QDateTimeEdit widget doesn't support seconds.
        now_as_QDateTime = QDateTime(
            now.year, now.month, now.day, now.hour, now.minute, 0
        )

        self.local_utc_offset = now.utcoffset()

        ### Create Widgets ###

        # Date/time selector widget, default to current date/time.
        self.datetime_edit = QDateTimeEdit(
            now_as_QDateTime,
            minimumDate=TimestamperUI.DEFAULT_MIN_DATE,
        )
        self.datetime_edit.setCalendarPopup(True)

        # Copy to Clipboard button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.on_copy_to_clipboard_clicked)

        # Timezone dropdown label
        timezone_dropdown_label = QLabel(
            "Select a timezone below. You're OS's timezone is automatically selected at launch."
        )
        timezone_dropdown_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Timezone dropdown
        self.timezone_dropdown = QComboBox()
        self.timezone_dropdown.addItems(self.generate_utc_offset_strings())

        # Set selected timezone to local timezone.
        if self.local_utc_offset is not None:
            local_timezone = dt.timezone(self.local_utc_offset)
            self.timezone_dropdown.setCurrentText(f"{local_timezone}")

        # Checkboxes

        checkbox_layout = QHBoxLayout()

        self.checkbox1 = QCheckBox("Check box1?")
        self.checkbox2 = QCheckBox("Check box2?")

        checkbox_layout.addWidget(self.checkbox1)
        checkbox_layout.addWidget(self.checkbox2)

        ### Place widgets on main layout ###
        main_layout.addWidget(
            self.datetime_edit, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        main_layout.addWidget(timezone_dropdown_label)
        main_layout.addWidget(self.timezone_dropdown)
        main_layout.addWidget(self.copy_button)

        main_layout.addLayout(checkbox_layout)

    ### Helpers ###
    def generate_utc_offset_strings(self) -> list[str]:
        """Returns a list of all possible UTC offsets (in 15 minute increments)."""

        offset_strings = []

        # Minutes used for easy timedelta creation.
        min_minutes = -12 * 60  # UTC-12:00
        max_minutes = 14 * 60  # UTC+14:00

        # timedelta/timezone used so that strings will match datetime objects exactly
        # (even if the format changes one day).
        for current_minutes in range(min_minutes, max_minutes + 15, 15):
            current_timedelta = dt.timedelta(minutes=current_minutes)

            # Make timezone object to get the form "UTC±HH:MM"
            timezone_from_delta = dt.timezone(current_timedelta)
            offset_strings.append(str(timezone_from_delta))

        return offset_strings

    ### "Slots", the event handling methods ###
    def on_copy_to_clipboard_clicked(self):
        """Creates a Discord timestamp based on the selected mode, date, and time, and copies it to the clipboard."""

        # cast() used here to remove the red underline in code editors.
        # (Because .toPython()'s type hints return type "Object", not datetime,
        # even though it *is* a datetime object.)
        chosen_date_time: dt.datetime = cast(
            dt.datetime, self.datetime_edit.dateTime().toPython()
        )

        # int() used to remove fractional part of timestamp.
        unix_timestamp = int(chosen_date_time.timestamp())

        # TODO: Copy selected type of timestamp (mode), not only Relative.
        formatted_timestamp = f"<t:{unix_timestamp}:R>"

        print(
            f'"{chosen_date_time}" has a Relative Discord timestamp of: {formatted_timestamp}\nCopying to clipboard...'
        )

        pyperclip.copy(formatted_timestamp)

        print("Copied!")


# NOTE: This block will only be run if the module (file) is run directly, not imported.
# __name__ is a built-in variable that says the name of what is using the module [file].
# i.e. __name__ == "__main__" if run from cmd/double-clicked files.
# Otherwise, __name__ will equal whatever the import statement is, like:
#  import timestamper  -->  __name__ == "timestamper"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimestamperUI()
    window.show()
    sys.exit(app.exec())


##### NOTES #####
# for hotkeys use QKeySequenceEdit()


##### IDEAS (arbitrarily numbered) #####
# 1. Add option to override minimum date of jan 1 1970.
# 2. Add a "Reset timezone" button that resets the timezone choice to the local/OS timezone.
