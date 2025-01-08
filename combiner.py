import os
import icalendar
from util import EventWrapper

# Add more categories as needed
OUTLOOK_EVENT_CATEGORIES = ['Red category', 'Orange category', 'Yellow category', 'Green category', 'Blue category', 'Purple category']



# Get files in `ics` directory
files = os.listdir('ics')

# Map each file to a category
assert(len(files) <= len(OUTLOOK_EVENT_CATEGORIES), 'Please add more categories!')
category_map = {}
for i, file in enumerate(files):
    label = file[:file.rindex('.')]
    category_map[label] = OUTLOOK_EVENT_CATEGORIES[i]

# Get all events from all files
events = {}

for i, file in enumerate(files):
    label = file[:file.rindex('.')]
    with open(f'ics/{file}') as f:
        calendar = icalendar.Calendar.from_ical(f.read())
    for event in calendar.walk('VEVENT'):
        if EventWrapper(event) in events:
            events[EventWrapper(event)].append(label)
        else:
            events[EventWrapper(event)] = [label]

# Use first file as base to transfer other properties
with open(f'ics/{files[0]}') as f:
    calendar = icalendar.Calendar.from_ical(f.read())

# Remove existing events
for event in calendar.walk('VEVENT'):
    calendar.subcomponents.remove(event)

# Add gathered events
for wrapper, labels in events.items():
    event = wrapper.event
    label_text = '/'.join(labels)
    event['SUMMARY'] = icalendar.vText(f"{event['SUMMARY']} ({label_text})")
    event['CATEGORIES'] = icalendar.prop.vCategory([category_map[label] for label in labels])
    calendar.add_component(event)

# Create combined calendar file
with open('combined.ics', 'wb') as f:
    f.write(calendar.to_ical())
