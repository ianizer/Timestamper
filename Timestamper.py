import sys  # To give exit codes.
from PySide6.QtCore import Qt, QDateTime  # Qt for alignment flags and more.
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)  # Main GUI components.
import datetime as dt  # For dates, times, and timezones.
from typing import cast  # To prevent false red underlines by code editors.
import base64  # For storing the icon in this single file.

# Generated from a png file. Placed up here so as not to clog up the main class.
ICON_STRING = b"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"


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
        # Set margins to 0's for more control outside this class.
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)
        self.setLayout(main_layout)

        self.timestamp_name: str = name
        self.timestamp_flag: str = flag
        self.formatted_timestamp: str

        self.label = QLabel(
            f"<b><u>{self.timestamp_name}</b></u><br>Example: <i>{example}</i>",
            alignment=Qt.AlignmentFlag.AlignBottom,
        )

        main_layout.addWidget(self.label)

        # Make horizontal layout for text box and copy button.
        sub_layout = QHBoxLayout()
        sub_layout.setSpacing(5)
        sub_layout.setContentsMargins(0, 0, 0, 0)

        self.display_box = QLineEdit(readOnly=True)
        self.display_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_box.setMinimumHeight(30)
        sub_layout.addWidget(self.display_box)

        self.copy_button = QPushButton("Copy")
        self.copy_button.setMinimumHeight(30)
        self.copy_button.clicked.connect(self.on_copy_clicked)
        sub_layout.addWidget(self.copy_button)

        main_layout.addLayout(sub_layout)

        self.display_timestamp(initial_timestamp)

    def display_timestamp(self, timestamp: int):
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

    STANDARD_TIME_FORMAT = "yyyy-MM-dd, h:mm:ss AP"
    MILITARY_TIME_FORMAT = "yyyy-MM-dd, HH:mm:ss"
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
    DISPLAYS_PER_ROW = 2
    # Displayed in the timezone combobox, but only for the local timezone.
    LOCAL_TZ_STRING = " (local timezone)"  # (include preceding space)
    DEFAULT_SPACING = 5

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Builds UI and initializes properties."""

        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ICON_STRING))
        self.setWindowIcon(QIcon(pixmap))

        self.setWindowTitle("Timestamper")
        self.setFont("Verdana")
        default_font = self.font()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        ### Properties and frequently-used local variables ###

        # .astimezone(), when called without args, gives a datetime object with
        # the computer's local timezone.
        # (Remove seconds for cleanliness)
        now = dt.datetime.now().astimezone().replace(second=0, microsecond=0)

        now_as_QDateTime = QDateTime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        # Due to adding the timezone with the .astimezone() call above,
        # now.utcoffset() is guaranteed not to be None.
        # cast() used to please VS Code.
        self.local_utc_offset: dt.timedelta = cast(dt.timedelta, now.utcoffset())

        self.timestamp_displays: list[TimestampDisplay] = []

        ### Create Widgets ###

        # Welcome label
        welcome_label = QLabel(
            "<b>Welcome to Timestamper!</b><br>Choose a date, time, and timezone, and the timestamps will instantly appear!",
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        main_layout.addWidget(welcome_label)

        # Timezone section

        tz_layout = QVBoxLayout()
        tz_layout.setSpacing(self.DEFAULT_SPACING)

        # Timezone label
        timezone_dropdown_label = QLabel(
            "<b>Select a timezone below.</b><br><i>(Your OS's timezone is automatically selected at launch.)</i>",
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        )

        tz_layout.addWidget(timezone_dropdown_label)

        # Timezone dropdown

        self.timezone_dropdown = QComboBox()
        self.timezone_dropdown.setMinimumHeight(30)
        self.timezone_dropdown.addItems(
            self.generate_utc_offset_strings(dt.timezone(self.local_utc_offset))
        )
        # Set selected timezone to local timezone.
        local_timezone = dt.timezone(self.local_utc_offset)
        self.timezone_dropdown.setCurrentText(f"{local_timezone}{self.LOCAL_TZ_STRING}")

        self.timezone_dropdown.currentTextChanged.connect(self.on_timezone_change)

        tz_layout.addWidget(
            self.timezone_dropdown, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        main_layout.addLayout(tz_layout)

        # Date/time selector section
        dt_VBox_layout = QVBoxLayout()
        dt_VBox_layout.setSpacing(self.DEFAULT_SPACING)
        dt_HBox_layout = QHBoxLayout()

        # Date/time setter label

        # NOTE: Alignment flags are 1-digit binary ints, so a bitwise OR (|) combines flags.
        date_selector_label = QLabel(
            "<b>Select the date/time to convert below</b> <i>(YYYY-MM-DD)</i>. <u>Click the arrow for a calendar.</u>",
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        )

        dt_VBox_layout.addWidget(date_selector_label)

        # Date/time selector widget, defaults to current date/time (now).

        self.datetime_edit = QDateTimeEdit(now_as_QDateTime)
        self.datetime_edit.setMinimumHeight(40)
        # Center date text
        self.datetime_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat(self.STANDARD_TIME_FORMAT)
        # Set min time to earliest possible with QDateTimeEdit
        self.datetime_edit.setMinimumDateTime(QDateTime(100, 1, 1, 0, 0, 0))

        datetime_edit_font = default_font
        datetime_edit_font.setPointSize(default_font.pointSize() + 3)
        self.datetime_edit.setFont(datetime_edit_font)

        self.datetime_edit.dateTimeChanged.connect(self.generate_timestamps)

        dt_HBox_layout.addWidget(
            self.datetime_edit, alignment=Qt.AlignmentFlag.AlignRight
        )

        # Checkbox for using 24-hour time.

        self.use_military_time_cb = QCheckBox(
            "Use military (24-hour) time?\n(does not affect timestamps)"
        )  # IDEA: Italicize "(does not affect timestamps)"
        self.use_military_time_cb.checkStateChanged.connect(
            self.on_military_time_cb_changed
        )

        dt_HBox_layout.addWidget(
            self.use_military_time_cb, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Place the horizontally aligned widgets below the label.
        dt_VBox_layout.addLayout(dt_HBox_layout)

        main_layout.addLayout(dt_VBox_layout)

        # Timestamp displays

        timestamp_layout = QGridLayout()
        # Add blank space above timestamp displays.
        timestamp_layout.setContentsMargins(0, 10, 0, 0)
        timestamp_layout.setHorizontalSpacing(25)
        timestamp_layout.setVerticalSpacing(25)

        current_ts = int(now.timestamp())
        current_row, current_column = 0, 0

        for name, flag, example in self.TIMESTAMP_TYPES:
            if len(self.timestamp_displays) % self.DISPLAYS_PER_ROW == 0:
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

        self.setMinimumWidth(620)

    ### Helpers ###

    def generate_utc_offset_strings(self, local_time_zone=dt.UTC) -> list[str]:
        """Returns a list of all possible UTC offsets (in 15 minute increments)."""

        offset_strings = []

        # Minutes used for easy timedelta creation.
        min_minutes = -12 * 60  # UTC-12:00
        max_minutes = 14 * 60  # UTC+14:00

        # Start at most positive UTC offset, end at most negative offset
        # so that higher offsets appear above lower ones in the combobox.
        for current_minutes in range(max_minutes, min_minutes - 15, -15):
            # timedelta/timezone used so that strings will match datetime objects exactly
            # (even if the format changes one day).
            current_timedelta = dt.timedelta(minutes=current_minutes)

            # Make timezone object to get the form "UTC±HH:MM"
            timezone_from_delta = dt.timezone(current_timedelta)

            # Insert at beginning to place negative offsets before positive ones.
            if timezone_from_delta == local_time_zone:
                offset_strings.append(str(timezone_from_delta) + self.LOCAL_TZ_STRING)
            else:
                offset_strings.append(str(timezone_from_delta))

        return offset_strings

    def get_selected_timezone(self) -> dt.timezone:
        """Returns the timezone selected from the timezone combobox."""
        # NOTE: This function is fragile.
        # If the format of the UTC offset changes one day, this will break.

        # Get UTC offset string from combobox,
        # removing the "your timezone" message if present.
        selected_timezone_str: str = self.timezone_dropdown.currentText().replace(
            self.LOCAL_TZ_STRING, ""
        )

        # Remove the "UTC" from the combobox string, adding "00:00" if timezone is UTC.
        selected_timezone_str = (
            "00:00" if selected_timezone_str == "UTC" else selected_timezone_str[3:]
        )

        split_timezone_str: list = selected_timezone_str.split(":")

        selected_tz_hours = int(split_timezone_str[0])
        selected_tz_minutes = int(split_timezone_str[1])

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
        chosen_date_time = cast(
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
            display.display_timestamp(unix_timestamp)


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


##### FUTURE IDEAS (arbitrarily numbered) #####
# 1. Make displays dynamic i.e. actual display what current timestamp will look like on discord rather than a static example.
# 2. Add tooltip to date/time selector that says how to use it.
# 3. Create a custom date/time selection widget to get past the year 100 and year 9999 limitations.
# 4. "Compact mode" which collapses timestamp displays into one edit box, and you select the type of timestamp to show from a combobox.
# 5. Perhaps hard-code LESS values (padding, spacing).
