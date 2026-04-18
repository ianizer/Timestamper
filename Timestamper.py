import datetime
import pyperclip  # for clipboard functions.

curDateTime = datetime.datetime.now()
unixTime = int(curDateTime.timestamp())
timestampR = f"<t:{unixTime}:R>"

print(f'"{curDateTime.strftime("%Y-%m-%d %H:%M:%S")}" has a Relative Discord timestamp of: {timestampR}\nCopying to clipboard...')
pyperclip.copy(timestampR)
