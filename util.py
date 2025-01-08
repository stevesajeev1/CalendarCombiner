import typing
import icalendar

# Wrapper class to allow for comparison of icalendar.Event objects
class EventWrapper:
    def __init__(self, event: icalendar.Event):
        self.event = event
    
    def __eq__(self, other):
        return remove_unique(self.event) == remove_unique(other.event)

    def __hash__(self):
        hash = 0
        for subcomponent in self.event.subcomponents:
            if isinstance(subcomponent, typing.Hashable):
                hash += subcomponent.__hash__()
        return hash

def remove_unique(event: icalendar.Event):
    copy = icalendar.Event.copy(event)
    copy.pop('DESCRIPTION')
    copy.pop('CATEGORIES')
    copy.pop('DTSTAMP')
    copy.pop('UID')
    return copy