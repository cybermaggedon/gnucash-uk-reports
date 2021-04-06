
import json
import datetime
import uuid

from . worksheet_model import SimpleValue, Breakdown, NilValue, Total
from . fact import *

def create_uuid():
    return str(uuid.uuid4())

IN_YEAR = 1
AT_START = 2
AT_END = 3

class Computable:
    def compute(self, accounts, start, end, result):
        raise RuntimeError("Not implemented")

    @staticmethod
    def load(cfg, comps, taxonomy):

        kind = cfg.get("kind")

        if kind == "group":
            return Group.load(cfg, comps, taxonomy)

        if kind == "computation":
            return Computation.load(cfg, comps, taxonomy)

        if kind == "line":
            return Line.load(cfg, comps, taxonomy)

        if kind == "constant":
            return Constant.load(cfg, comps, taxonomy)

        raise RuntimeError("Don't understand computable type '%s'" % kind)

class Line(Computable):

    def __init__(self, id, description, accounts, taxonomy, period=AT_END):
        self.id = id
        self.description = description
        self.accounts = accounts
        self.taxonomy = taxonomy
        self.period = period

    def compute(self, session, start, end, result):

        total = 0

        cdef = ContextDefinition()

        # FIXME: If there are transactions preceding 1970, this won't work.
        if self.period == AT_START:
            cdef.set_instant(start)
            history = datetime.date(1970, 1, 1)
            start, end = history, start
        elif self.period == AT_END:
            cdef.set_instant(end)
            history = datetime.date(1970, 1, 1)
            start, end = history, end
        else:
            cdef.set_period(start, end)
            
        for acct_name in self.accounts:
            acct = session.get_account(session.root, acct_name)

            splits = session.get_splits(acct, start, end)

            acct_total = sum([v["amount"] for v in splits])

            if session.is_debit(acct.GetType()):
                acct_total *= -1

            total += acct_total

        cdef.add_segments(self.id, self.taxonomy)
        context = self.taxonomy.get_context(cdef)

        result.set(self.id, context.create_money_fact(self.id, total))

        return total

    def get_output(self, result):

        return SimpleValue(self, self.description, result.get(self.id))

        return output


    @staticmethod
    def load(cfg, comps, taxonomy):
        id = cfg.get("id")
        if id == None: id = create_uuid()

        pspec = cfg.get("period")

        pid = {
            "in-year": IN_YEAR,
            "to-start": AT_START,
            "to-end": AT_END
        }.get(pspec, AT_END)

        return Line(id, cfg.get("description"), cfg.get("accounts"),
                    taxonomy, pid)

class Constant(Computable):
    def __init__(self, id, description, values, taxonomy):
        self.id = id
        self.description = description
        self.values = values
        self.taxonomy = taxonomy

    def compute(self, session, start, end, result):

        cdef = ContextDefinition()
        cdef.set_period(start, end)
        cdef.add_segments(self.id, self.taxonomy)
        context = self.taxonomy.get_context(cdef)

        val = self.values[str(end)]
        result.set(self.id, context.create_money_fact(self.id, val))
        return val

    def get_output(self, result):

        output = SimpleValue(self, self.description, result.get(self.id))

        return output

    @staticmethod
    def load(cfg, comps, taxonomy):
        id = cfg.get("id")
        if id == None: id = create_uuid()

        return Constant(id, cfg.get("description"), cfg.get("values"),
                        taxonomy)

class Group(Computable):
    def __init__(self, id, description, taxonomy):
        self.id = id
        self.description = description
        self.lines = []
        self.taxonomy = taxonomy

    @staticmethod
    def load(cfg, comps, taxonomy):

        id = cfg.get("id")
        if id == None: id = create_uuid()

        g = Group(id, cfg.get("description"), taxonomy)

        for l in cfg.get("lines"):

            elt = Computable.load(l, comps, taxonomy)
            g.add(elt)

        def set_hide(x):
            g.hide_breakdown = x

        cfg.get("hide-breakdown", False).use(set_hide)
        
        return g

    def add(self, line):
        self.lines.append(line)

    def compute(self, accounts, start, end, result):

        cdef = ContextDefinition()
        cdef.set_period(start, end)
        cdef.add_segments(self.id, self.taxonomy)
        context = self.taxonomy.get_context(cdef)

        total = 0
        for line in self.lines:
            total += line.compute(accounts, start, end, result)
        result.set(self.id, context.create_money_fact(self.id, total))
        return total

    def get_output(self, result):

        if len(self.lines) == 0:
            output = NilValue(self, self.description, result.get(self.id))
            return output

        if self.hide_breakdown:

            # For a hidden breakdown, create a breakdown object which is not
            # returned, and a Total object which references it
            bd = Breakdown(
                self,
                self.description,
                result.get(self.id),
                items= [
                    item.get_output(result) for item in self.lines
                ]
            )

            output = Total(self, self.description, result.get(self.id),
                           items=[bd])

        else:

            output = Breakdown(
                self,
                self.description,
                result.get(self.id),
                items= [
                    item.get_output(result) for item in self.lines
                ]
            )

        return output

class AddOperation(Computable):
    def __init__(self, item):
        self.item = item
        self.description = item.description
    def compute(self, accounts, start, end, result):
        # Don't put this in result
        return self.item.compute(accounts, start, end, result)

class Result:
    def __init__(self):
        self.values = {}

    def set(self, id, value):
        self.values[id] = value

    def get(self, id):
        return self.values[id]

class Computation(Computable):
    def __init__(self, id, description, taxonomy):
        self.id = id
        self.description = description
        self.steps = []
        self.taxonomy = taxonomy

    def add(self, item):
        self.steps.append(AddOperation(item))

    def compute(self, accounts, start, end, result):

        total = 0

        for v in self.steps:
            total += v.compute(accounts, start, end, result)

        cdef = ContextDefinition()
        cdef.set_period(start, end)
        cdef.add_segments(self.id, self.taxonomy)
        context = self.taxonomy.get_context(cdef)

        result.set(self.id, context.create_money_fact(self.id, total))

        return total

    def get_output(self, result):

        if len(self.steps) == 0:
            
            output = NilValue(self, self.description, result.get(self.id))
            return output

        # Assume item contains AddOperations x.item provides value.
        # Needs rework if we do something more complicated.
        output = Total(self, self.description, result.get(self.id),
                       items=[
                           item.item for item in self.steps
                       ])

        return output

    @staticmethod
    def load(cfg, comps, taxonomy):

        id = cfg.get("id")
        if id == None: id = create_uuid()

        comp = Computation(id, cfg.get("description"), taxonomy)

        for item in cfg.get("inputs"):
            comp.add(comps[item])

        return comp

