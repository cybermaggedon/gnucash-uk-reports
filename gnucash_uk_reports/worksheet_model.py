
class WorksheetItem:
    pass

class SimpleValue(WorksheetItem):
    def __init__(self, desc, value):
        self.description = desc
        self.value = value

class Breakdown(WorksheetItem):
    def __init__(self, desc, value, items):
        self.description = desc
        self.value = value
        self.items = items

class NilValue(WorksheetItem):
    def __init__(self, desc):
        self.description = desc
        self.value = 0

class Total(WorksheetItem):
    def __init__(self, desc, value, items):
        self.description = desc
        self.value = value
        self.items = items

class Worksheet:
    pass
