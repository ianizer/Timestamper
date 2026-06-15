# Timestamper
A GUI-based app for quickly, easily, and unambiguously producing formatted timestamps for use on Discord.

## Installation
On **Windows**, simply run Timestamper.exe in the latest release.

On other systems _(or if you prefer not to run a sketchy executable)_, install Python and unzip this repo as a folder. 
Then, open a terminal window inside said folder and create a virtual environment (run this command):

`python -m venv .venv`

Then run the following two commands in the same terminal window:

`./.venv/Scripts/activate`

`python -m pip install -r requirements.txt`
## Running Timestamper
After running the installation commands once, you may now run Timestamper from the terminal as follows (in the folder of the repo):

`./.venv/Scripts/activate`

`python Timestamper.py`

## Features
**Instant timestamp generation:** The instant you enter a date, all 10 timestamp types are generated and displayed.

**Timezone selection:** Can set a timezone other than your PC's timezone (e.g. UTC-1:00 even if you're in New Zealand).

**24-hour (military time):** Allows using 24-hour time instead of traditional 12-hour ("AM PM") time.

**Copy to clipboard buttons:** Clicking "Copy" next to any timestamp display copies the formatted timestamp to the clipboard.

<img width="619" height="730" alt="image" src="https://github.com/user-attachments/assets/0ac5780f-fb7b-4d84-b6fc-61467c21b9d0" />
