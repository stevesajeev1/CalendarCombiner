import os
import icalendar

# Add more categories as needed
OUTLOOK_EVENT_CATEGORIES = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']

# Get files in `ics` directory
files = os.listdir('ics')
# Use first file as base (to copy other properties)
first = files[0]
first_label = first[:first.rindex('.')]
with open(f'ics/{first}') as f:
    combined_calendar = icalendar.Calendar.from_ical(f.read())
for event in combined_calendar.walk('VEVENT'):
    event['SUMMARY'] = icalendar.vText(f"{event['SUMMARY']} ({first_label})")
    event['CATEGORIES'] = icalendar.prop.vCategory([f'{OUTLOOK_EVENT_CATEGORIES[0]} category'])

# Add remaining files
for i, file in enumerate(files[1:]):
    label = file[:file.rindex('.')]
    with open(f'ics/{file}') as f:
        calendar = icalendar.Calendar.from_ical(f.read())
    for event in calendar.walk('VEVENT'):
        event['SUMMARY'] = icalendar.vText(f"{event['SUMMARY']} ({label})")
        event['CATEGORIES'] = icalendar.prop.vCategory([f'{OUTLOOK_EVENT_CATEGORIES[i+1]} category'])
        combined_calendar.add_component(event)

# Create combined calendar file
with open('combined.ics', 'wb') as f:
    f.write(combined_calendar.to_ical())
