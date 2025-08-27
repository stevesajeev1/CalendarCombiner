import os
import icalendar
from util import ComponentWrapper

# Add more categories as needed
OUTLOOK_EVENT_CATEGORIES = ['Red category', 'Orange category', 'Yellow category', 'Green category', 'Blue category', 'Purple category']



# Get files in `ics` directory
files = os.listdir('ics')

# Map each file to a category
assert(len(files) <= len(OUTLOOK_EVENT_CATEGORIES), 'Please add more categories!') # type: ignore
category_map = {}
for i, file in enumerate(files):
    label = file[:file.rindex('.')]
    category_map[label] = OUTLOOK_EVENT_CATEGORIES[i]

# Get all components from all files
components = {}

for i, file in enumerate(files):
    label = file[:file.rindex('.')]
    with open(f'ics/{file}') as f:
        calendar = icalendar.Calendar.from_ical(f.read())
    for component in calendar.walk('VEVENT'):
        if ComponentWrapper(component) in components:
            components[ComponentWrapper(component)].append(label)
        else:
            components[ComponentWrapper(component)] = [label]

# Use first file as base to transfer other properties
with open(f'ics/{files[0]}') as f:
    calendar = icalendar.Calendar.from_ical(f.read())

# Remove existing components
for component in calendar.walk('VEVENT'):
    calendar.subcomponents.remove(component)

# Add gathered components
for wrapper, labels in components.items():
    component = wrapper.component
    label_text = '/'.join(labels)
    component['SUMMARY'] = icalendar.vText(f"{component['SUMMARY']} ({label_text})")
    component['CATEGORIES'] = icalendar.prop.vCategory([category_map[label] for label in labels])

    # Disable alarms
    for alarm in component.walk('VALARM'):
        component.subcomponents.remove(alarm);
    
    calendar.add_component(component)

# Create combined calendar file
with open('combined.ics', 'wb') as f:
    f.write(calendar.to_ical())
