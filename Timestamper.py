import sys  # To give exit codes.
from PySide6.QtCore import Qt, QDateTime, QDate  # For alignment and other flags.
from PySide6.QtGui import QCursor  # For tooltips.
from PySide6.QtWidgets import *  # Main GUI components.
import datetime as dt  # For dates, times, and timezones.
from typing import cast  # To prevent false red underlines by code editors.


class TimestampDisplay(QWidget):
    """A QLabel up top, and a horizontally-aligned read-only QLineEdit and QButton.

    The QLabel contains the name and flag of the timestamp type, e.g. "Relative (:R)"

    The QLineEdit will display the generated timestamp for use on Discord.

    The QButton will simply copy the generated timestamp to the clipboard on click."""

    def __init__(self, name: str, flag: str, example: str, initial_timestamp: int):
        """Create and combine the widgets.

        :param name: Name of timestamp type, like "Relative".
        :param flag: Flag for the timestamp type, like 'R' for Relative.
        :param example: Example of timestamp type placed in label, like "in 5 days".
        """

        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.timestamp_name: str = name
        self.timestamp_flag: str = flag
        self.formatted_timestamp: str

        self.label = QLabel(
            f"<b><u>{self.timestamp_name}</u></b> <i>e.g.</i> <b>{example}</b>"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        main_layout.addWidget(self.label)

        # Make horizontal layout for text box and copy button.
        sub_layout = QHBoxLayout()

        self.display_box = QLineEdit(readOnly=True)
        sub_layout.addWidget(self.display_box)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.on_copy_clicked)
        sub_layout.addWidget(self.copy_button)

        main_layout.addLayout(sub_layout)

        self.display_new_timestamp(initial_timestamp)

    def display_new_timestamp(self, timestamp: int):
        """Displays the given timestamp in the display box."""

        self.formatted_timestamp = (
            f"<t:{timestamp}:{self.timestamp_flag}>"
            if len(self.timestamp_flag) > 0
            else f"<t:{timestamp}>"
        )

        self.display_box.setText(self.formatted_timestamp)

    def on_copy_clicked(self):
        """Copies the Discord-ready timestamp to clipboard, if it exists.
        If it doesn't exist, nothing happens."""

        if self.formatted_timestamp is not None:
            QApplication.clipboard().setText(self.formatted_timestamp)
            print("Copied!")


# QWidget used as QMainWindow's features are unnecessary for this app.
class TimestamperUI(QWidget):
    """Main GUI."""

    STANDARD_TIME_FORMAT = "yyyy-MM-dd hh:mm:ss AP"
    MILITARY_TIME_FORMAT = "yyyy-MM-dd hh:mm:ss"
    # TIMESTAMP_TYPES FORMAT: ((name, flag, example),)
    TIMESTAMP_TYPES = (
        ("Default", "", "March 9, 2026 at 3:15 PM"),
        ("Relative Time", "R", "in 5 days"),
        ("Short Time", "t", "3:15 PM"),
        ("Medium Time", "T", "3:15:00 PM"),
        ("Short Date", "d", "3/9/2026"),
        ("Long Date", "D", "March 9, 2026"),
        ("Long Date, Short Time", "f", "March 9, 2026 at 3:15 PM"),
        ("Full Date, Short Time", "F", "Monday, March 9, 2026 at 3:15 PM"),
        ("Short Date, Short Time", "s", "3/9/2026, 3:15 PM"),
        ("Short Date, Medium Time", "S", "3/9/2026, 3:15:00 PM"),
    )  # Maybe turn this into a tuple of dictionaries, like ({"name" : "Relative", ...}, ...)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Builds UI and initializes properties."""

        self.setWindowTitle("Timestamper")

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        ### Properties and frequently-used local variables ###

        # .astimezone(), when called without args, gives a datetime object with
        # the computer's local timezone.
        # (Remove seconds for cleanliness)
        now = dt.datetime.now().astimezone().replace(second=0, microsecond=0)

        # Let seconds be 0
        now_as_QDateTime = QDateTime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        self.local_utc_offset = now.utcoffset()

        self.timestamp_displays: list[TimestampDisplay] = []

        ### Create Widgets ###

        # Date/time setter label

        date_selector_label = QLabel(
            "<b>Select the date/time to convert below</b> <i>(YYYY-MM-DD)</i>. Click the arrow for a calendar."
        )

        # NOTE: Alignment flags are 1-digit binary ints, so a bitwise OR (|) combines flags.
        date_selector_label.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        )
        main_layout.addWidget(date_selector_label)

        # Date/time selector widget, defaults to current date/time.

        dt_layout = QHBoxLayout()

        self.datetime_edit = QDateTimeEdit(now_as_QDateTime)
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat(self.STANDARD_TIME_FORMAT)
        # Set to minimum time possible with QDateTimeEdit
        self.datetime_edit.setMinimumDateTime(QDateTime(100, 1, 1, 0, 0, 0))

        self.datetime_edit.dateTimeChanged.connect(self.generate_timestamps)

        dt_layout.addWidget(self.datetime_edit, alignment=Qt.AlignmentFlag.AlignRight)

        # Checkbox for using 24-hour time.

        self.use_military_time_cb = QCheckBox(
            "Use military (24-hour) time?\n(does not affect timestamps)"
        )  # IDEA: Italicize "(does not affect timestamps)"
        self.use_military_time_cb.checkStateChanged.connect(
            self.on_military_time_cb_changed
        )

        dt_layout.addWidget(
            self.use_military_time_cb, alignment=Qt.AlignmentFlag.AlignLeft
        )

        main_layout.addLayout(dt_layout)

        # Timezone dropdown label

        timezone_dropdown_label = QLabel(
            "<b>Select a timezone below.</b>\n<i>(Your OS's timezone is automatically selected at launch.)</i>"
        )
        timezone_dropdown_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        main_layout.addWidget(timezone_dropdown_label)

        # Timezone dropdown

        self.timezone_dropdown = QComboBox()
        self.timezone_dropdown.addItems(self.generate_utc_offset_strings())
        self.timezone_dropdown.currentTextChanged.connect(self.on_timezone_change)

        # Set selected timezone to local timezone.
        if self.local_utc_offset is not None:
            local_timezone = dt.timezone(self.local_utc_offset)
            self.timezone_dropdown.setCurrentText(f"{local_timezone}")

        main_layout.addWidget(self.timezone_dropdown)

        # Timestamp displays

        DISPLAYS_PER_ROW = 2
        timestamp_layout = QGridLayout()

        current_ts = int(now.timestamp())
        current_row, current_column = 0, 0

        for name, flag, example in self.TIMESTAMP_TYPES:
            if len(self.timestamp_displays) % DISPLAYS_PER_ROW == 0:
                current_row += 1
                current_column = 0

            new_ts_display = TimestampDisplay(
                name=name,
                flag=flag,
                example=example,
                initial_timestamp=current_ts,
            )

            timestamp_layout.addWidget(new_ts_display, current_row, current_column)
            current_column += 1

            self.timestamp_displays.append(new_ts_display)

        main_layout.addLayout(timestamp_layout)

        self.adjustSize()  # Set min size dynamically after widgets placed.
        self.setMinimumSize(self.size())

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

    def get_selected_timezone(self) -> dt.timezone:
        """Returns the timezone selected from the timezone combobox."""
        # NOTE: This function is fragile.
        # If the format of the UTC offset changes one day, this will break.

        selected_timezone_str: str = self.timezone_dropdown.currentText()
        selected_timezone_str = (
            "00:00" if selected_timezone_str == "UTC" else selected_timezone_str[3:]
        )

        split_timezone_str: list = selected_timezone_str.split(":")

        selected_tz_hours: int = int(split_timezone_str[0])
        selected_tz_minutes: int = int(split_timezone_str[1])

        # If in a negative timezone, make minutes negative as well.
        if "-" in selected_timezone_str:
            selected_tz_minutes = -selected_tz_minutes

        selected_timezone: dt.timezone = dt.timezone(
            dt.timedelta(hours=selected_tz_hours, minutes=selected_tz_minutes)
        )

        return selected_timezone

    ### "Slots", the event handling methods ###

    def on_military_time_cb_changed(self):
        """Changes format (12H/24H) of the date/time entry box."""

        if self.use_military_time_cb.isChecked():
            self.datetime_edit.setDisplayFormat(self.MILITARY_TIME_FORMAT)
        else:
            self.datetime_edit.setDisplayFormat(self.STANDARD_TIME_FORMAT)

    def on_datetime_changed(self):
        self.generate_timestamps()

    def on_timezone_change(self):
        self.generate_timestamps()

    def generate_timestamps(self):
        """Computes the Unix timestamp for the selected date and time and updates the timestamp displays."""

        # cast() used here to remove the red underline in code editors.
        # (Because .toPython()'s type hints return type "Object", not datetime,
        # even though it *is* a datetime object.)
        chosen_date_time: dt.datetime = cast(
            dt.datetime, self.datetime_edit.dateTime().toPython()
        ).replace(tzinfo=self.get_selected_timezone())

        epoch = dt.datetime(
            year=1970,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=dt.UTC,
        )

        # int() used to remove fractional part of timestamp.
        # Manual subtraction to allow for negative timestamp generation on Windows.
        unix_timestamp = int((chosen_date_time - epoch).total_seconds())

        for display in self.timestamp_displays:
            display.display_new_timestamp(unix_timestamp)


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
# 1. Add a "Reset timezone" button that resets the timezone choice to the local/OS timezone.
# 2. Make "Generate Timestamps" button glow or have an outline or something like that when there is a change to the datetime_edit or timezone dropdown selection.
# 3. Split timestamp displays into two columns (place two boxes on same row).
# 4. Make displays dynamic i.e. actual display what current timestamp will look like on discord rather than a static example.
