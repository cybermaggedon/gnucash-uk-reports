
from . datum import *

class ValueSet:
    def __init__(self, context):
        self.context = context
        self.values = {}
    def describe(self):
        self.context.describe()
        for v in self.values.values():
            v.describe()
    def add_money(self, id, value):
        self.values[id] = MoneyDatum(id, value, self.context)
    def add_string(self, id, value):
        self.values[id] = StringDatum(id, value, self.context)
    def add_count(self, id, value):
        self.values[id] = CountDatum(id, value, self.context)
    def add_bool(self, id, value):
        self.values[id] = BoolDatum(id, value, self.context)

