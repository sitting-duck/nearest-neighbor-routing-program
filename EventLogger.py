
class EventLogger:

    def _init__(self):
        self.events = []

    def add_package_event(self, event):
        self.events.append(event)