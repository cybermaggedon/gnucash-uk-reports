
import json
import copy
from . period import Period
from . datum import *
from . context import Context

class Fact:
    def use(self, fn):
        return fn(self)

class MoneyFact(Fact):
    def __init__(self, context, name, value, reverse=False, unit="GBP"):
        self.name = name
        self.value = value
        self.context = context
        self.unit = unit
        self.reverse = reverse
    def describe(self):
        if self.name:
            name = self.name
            context = self.context
            print("        {0} {1} {2}".format(
                str(self.value), name, context
            ))
        else:
            print("        {0}".format(str(self.value)))
    def append(self, doc, par):
        value = self.value
        if self.reverse: value *= -1
        if hasattr(self, "name"):
            elt = doc.createElement("ix:nonFraction")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
            elt.setAttribute("unitRef", self.unit)
            elt.setAttribute("decimals", "2")
            if value < 0:
                elt.setAttribute("sign", "-")
            elt.appendChild(doc.createTextNode(str(value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(str(value)))
    def copy(self):
        return copy.copy(self)
    def rename(self, id, context, tx):
        self.name = tx.get_tag_name(id)
        self.context = context
        self.reverse = tx.get_sign_reversed(id)

class CountFact(Fact):
    def __init__(self, value, context, unit="pure"):
        self.value = value
        self.context = context
        self.reverse = False
        self.unit = unit
    def describe(self):
        if self.name:
            name = self.name
            context = self.context.id
            print("        {0} {1} {2}".format(
                str(self.value), name, context
            ))
        else:
            print("        {0}".format(str(self.value)))
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonFraction")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context.id)
            elt.setAttribute("unitRef", self.unit)
            elt.setAttribute("decimals", "0")
            elt.appendChild(doc.createTextNode(str(self.value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(str(self.value)))

class NumberFact(Fact):
    def __init__(self, value, context, unit="pure"):
        self.value = value
        self.context = context
        self.reverse = False
        self.unit = unit
    def describe(self):
        if self.name:
            name = self.name
            context = self.context.id
            print("        {0} {1} {2}".format(
                str(self.value), name, context
            ))
        else:
            print("        {0}".format(str(self.value)))
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonFraction")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context.id)
            elt.setAttribute("unitRef", self.unit)
            elt.setAttribute("decimals", "2")
            elt.appendChild(doc.createTextNode(str(self.value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(str(self.value)))

class StringFact(Fact):
    def __init__(self, context, name, value):
        self.value = value
        self.context = context
        self.name = name
    def describe(self):
        if self.name:
            name = self.name
            context = self.context
            print("        {0} {1} {2}".format(
                self.value, name, context
            ))
        else:
            print("        {0}".format(str(self.value)))
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonNumeric")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
            elt.appendChild(doc.createTextNode(self.value))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(self.value))

class BoolFact(Fact):
    def __init__(self, value, context):
        self.value = bool(value)
        self.context = context
    def describe(self):
        if self.name:
            name = self.name
            context = self.context.id
            print("        {0} {1} {2}".format(
                self.value, name, context
            ))
        else:
            print("        {0}".format(str(self.value)))
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonNumeric")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context.id)
            elt.appendChild(doc.createTextNode(json.dumps(self.value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(json.dumps(self.value)))

class DateFact(Fact):
    def __init__(self, context, name, value):
        self.context = context
        self.name = name
        self.value = value
    def describe(self):
        if self.name:
            name = self.name
            context = self.context.id
            print("        {0} {1} {2}".format(
                self.value, name, context
            ))
        else:
            print("        {0}".format(str(self.value)))
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonNumeric")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
            elt.setAttribute("format", "ixt2:datedaymonthyearen")
            elt.appendChild(doc.createTextNode(self.value.strftime("%d %B %Y")))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(self.value.strftime("%d %B %Y")))

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
                it.describe()
        if self.total:
            self.total.describe()

class Series:
    def __init__(self, desc, values):
        self.description = desc
        self.values = values
    def describe(self):
        print("      {0}:".format(self.description))
        for v in self.values:
            v.describe()

