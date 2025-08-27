import typing
import icalendar

# Wrapper class to allow for comparison of icalendar.Component objects
class ComponentWrapper:
    def __init__(self, component: icalendar.Component):
        self.component = component
    
    def __eq__(self, other):
        return remove_unique(self.component) == remove_unique(other.component)

    def __hash__(self):
        hash = 0
        for subcomponent in self.component.subcomponents:
            if isinstance(subcomponent, typing.Hashable):
                hash += subcomponent.__hash__()
        return hash

def remove_unique(component: icalendar.Component):
    copy = icalendar.Component.copy(component)
    copy.pop('DESCRIPTION')
    copy.pop('CATEGORIES')
    copy.pop('DTSTAMP')
    copy.pop('UID')
    return copy