
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
    def append(self, doc, par):
        value = self.value
        if self.reverse: value *= -1
        if self.name:
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
    def __init__(self, context, name, value, unit="pure"):
        self.context = context
        self.name = name
        self.value = value
        self.reverse = False
        self.unit = unit
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonFraction")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
            elt.setAttribute("unitRef", self.unit)
            elt.setAttribute("decimals", "0")
            elt.appendChild(doc.createTextNode(str(self.value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(str(self.value)))

class NumberFact(Fact):
    def __init__(self, context, name, value, unit="pure"):
        self.context = context
        self.name = name
        self.value = value
        self.reverse = False
        self.unit = unit
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonFraction")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
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
    def append(self, doc, par):
        print(self.name)
        if self.name:
            print("BUNCHY", self.name)
        if self.name:
            elt = doc.createElement("ix:nonNumeric")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
            elt.appendChild(doc.createTextNode(self.value))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(self.value))

class BoolFact(Fact):
    def __init__(self, context, name, value):
        self.value = bool(value)
        self.name = name
        self.context = context
    def append(self, doc, par):
        if self.name:
            elt = doc.createElement("ix:nonNumeric")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context)
            elt.appendChild(doc.createTextNode(json.dumps(self.value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(json.dumps(self.value)))

class DateFact(Fact):
    def __init__(self, context, name, value):
        self.context = context
        self.name = name
        self.value = value
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
    pass

class Section:
    pass

class Series:
    pass

