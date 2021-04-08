
from . datum import *

class Context:
    def __init__(self, parent):
        self.parent = parent
        self.entity = None
        self.scheme = None
        self.segments = {}
        self.period = None
        self.instant = None
        self.children = {}

    def with_segments(self, segments):

        # entity, scheme, segments, period, instant
        seghash = "//".join([
            "%s=%s" % (k, segments[k])
            for k in sorted(segments.keys())
        ])
        k = (None, None, seghash, None, None)
        if k in self.children:
            return self.children[k]

        c = Context(self)
        self.children[k] = c
        c.segments = segments
        return c

    def with_period(self, period):

        # entity, scheme, segments, period, instant
        k = (None, None, None, str(period), None)
        if k in self.children:
            return self.children[k]

        c = Context(self)
        self.children[k] = c
        c.period = period
        return c

    def with_instant(self, instant):

        # entity, scheme, segments, period, instant
        k = (None, None, None, None, str(instant))
        if k in self.children:
            return self.children[k]

        c = Context(self)
        self.children[k] = c
        c.instant = instant
        return c

    def with_entity(self, scheme, id):

        # entity, scheme, segments, period, instant
        k = (id, scheme, None, None, None)
        if k in self.children:
            return self.children[k]

        c = Context(self)
        self.children[k] = c
        c.entity = id
        c.scheme = scheme
        return c

    def describe(self):
        if self.parent:
            self.parent.describe()
        if self.entity:
            print("Entity: %s (%s)" % (self.entity, self.scheme))
        if self.segments:
            for k, v in self.segments.items():
                print("Segment: %s (%s)" % (k, v))
        if self.period:
            print("Period: %s" % self.period)

    def create_money_datum(self, id, value):
        return MoneyDatum(id, value, self)

