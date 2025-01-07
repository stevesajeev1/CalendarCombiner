# Calendar Combiner

Python script to combine several calendars into a single calendar, color-coding and labeling them. The color-coding is intended for use in Microsoft Outlook Calendar.

> Note: Although the newest version of the ICS Specification ([RFC 7986](https://datatracker.ietf.org/doc/html/rfc7986)) provides support for a `COLOR` property, most mainstream calendars (Google, Microsoft Outlook) still only follow an older version ([RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545)). As a workaround, this script uses the default provided categories of Microsoft Outlook to color-code the calendars. To ensure that this color-coding is kept when the calendar is shared, viewers must be given editing permissions.

## Usage

Place the individual `.ics` files in an `ics` folder at the same level as the script. The label for each calendar is the filename of the `.ics` file. 

```console
pip install -r requirements.txt
python combiner.py
```

### Example Use Case

- Combine several people's schedules into a single calendar. Each person's schedule will be given a distinct color. By using each person's name as the filename for the `.ics` file, the schedules will also be labeled by their name.
