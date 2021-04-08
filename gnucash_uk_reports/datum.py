
class Datum:
    def describe(self):
        print("%-20s: %s" % (self.id, str(self.value)))

class MoneyDatum(Datum):
    def __init__(self, id, value, context):
        self.id = id
        self.value = value
        self.context = context

class StringDatum(Datum):
    def __init__(self, id, value, context):
        self.id = id
        self.value = value
        self.context = context

class CountDatum(Datum):
    def __init__(self, id, value, context):
        self.id = id
        self.value = value
        self.context = context

class BoolDatum(Datum):
    def __init__(self, id, value, context):
        self.id = id
        self.value = value
        self.context = context

class DateDatum(Datum):
    def __init__(self, id, value, context):
        self.id = id
        self.value = value
        self.context = context
