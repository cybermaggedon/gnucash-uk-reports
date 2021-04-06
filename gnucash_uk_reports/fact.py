
class Fact:
    pass

class BooleanFact(Fact):
    def __init__(self, value):
        self.value = value

NONE=0
CREDIT=1
DEBIT=2

class MoneyFact(Fact):
    def __init__(self, value, balance=NONE):
        self.value = value
    def describe(self):
        return str(self.value)

class CountFact(Fact):
    def __init__(self, value):
        self.value = value

class StringFact(Fact):
    def __init__(self, value):
        self.value = value

class Taxonomy:
    def get_tag_name(self, id):
        return "tag:FIXME"
    def get_tag_context(self, id):
        return "ctxt-FIXME"
    def create_money_fact(self, id, value):
        # FIXME: Credit hard-coded
        m = MoneyFact(value, balance=CREDIT)
        m.tag = self.get_tag_name(id)
        m.context = self.get_tag_context(id)
        return m

class FRS101(Taxonomy):
    pass

class Context:
    pass

class Dataset:
    def describe(self):
        print("Dataset:")
        print("Periods: ", ", ".join([str(p) for p in self.periods]))
        for sec in self.sections:
            sec.describe()

class Section:
    def describe(self):
        print("  Series:")
        print("    Heading:", self.header)
        if self.items:
            for it in self.items:
                print("      ", it.description, ": ",
                      it.describe())
        if self.total:
            print("    Total: ", self.total.describe())

class Series:
    def __init__(self, desc, values):
        self.description = desc
        self.values = values
    def describe(self):
        return " ".join([v.describe() for v in self.values])


