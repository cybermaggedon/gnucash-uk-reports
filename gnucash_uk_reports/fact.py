
import json

class Fact:
    def use(self, fn):
        return fn(self)

class MoneyFact(Fact):
    def __init__(self, value, context, reverse=False, unit="GBP"):
        self.value = value
        self.context = context
        self.unit = unit
        self.reverse = reverse
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
        value = self.value
        if self.reverse: value *= -1
        if self.name:
            elt = doc.createElement("ix:nonFraction")
            elt.setAttribute("name", self.name)
            elt.setAttribute("contextRef", self.context.id)
            elt.setAttribute("unitRef", self.unit)
            elt.setAttribute("decimals", "2")
            if self.reverse:
                elt.setAttribute("sign", "-")
            elt.appendChild(doc.createTextNode(str(value)))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(str(value)))

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

class StringFact(Fact):
    def __init__(self, value, context):
        self.value = value
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
    def __init__(self, value, context):
        self.value = value
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
            elt.setAttribute("format", "ixt2:datedaymonthyearen")
            elt.appendChild(doc.createTextNode(self.value.strftime("%d %B %Y")))
            par.appendChild(elt)
        else:
            par.appendChild(doc.createTextNode(self.value.strftime("%d %B %Y")))

class Taxonomy:
    def __init__(self, cfg, name):
        self.cfg = cfg
        self.name = name
        self.contexts = {}
        self.next_context_id = 0

    def get_tag_name(self, id):
        key = "taxonomy.{0}.tags.{1}".format(self.name, id)
        return self.cfg.get(key)

    def get_sign_reversed(self, id):
        key = "taxonomy.{0}.sign-reversed.{1}".format(self.name, id)
        return self.cfg.get_bool(key)

    def get_tag_dimensions(self, id):
        key = "taxonomy.{0}.segments.{1}".format(self.name, id)
        return self.cfg.get(key)

    def lookup_dimension(self, id, val):
        k1 = "taxonomy.{0}.lookup.{1}.dimension".format(self.name, id)
        k2 = "taxonomy.{0}.lookup.{1}.map.{2}".format(self.name, id, val)
        return self.cfg.get(k1), self.cfg.get(k2)

    def create_money_fact(self, id, value, context):

        m = MoneyFact(value, context)
        m.name = self.get_tag_name(id)
        m.reverse = self.get_sign_reversed(id)
        m.context = context
        return m

    def create_count_fact(self, id, value, context):

        m = CountFact(value, context)
        m.name = self.get_tag_name(id)
        m.reverse = self.get_sign_reversed(id)
        m.context = context
        return m

    def create_string_fact(self, id, value, context):

        m = StringFact(value, context)
        m.name = self.get_tag_name(id)
        m.context = context
        return m

    def create_bool_fact(self, id, value, context):

        m = BoolFact(value, context)
        m.name = self.get_tag_name(id)
        m.context = context
        return m

    def create_date_fact(self, id, value, context):

        m = DateFact(value, context)
        m.name = self.get_tag_name(id)
        m.context = context
        return m

    def get_context(self, cdef):

        key = cdef.get_key()

        if key in self.contexts:
            return self.contexts[key]

        ctxt = Context(self, cdef)
        ctxt.id = "ctxt-" + str(self.next_context_id)
        self.next_context_id += 1
        self.contexts[key] = ctxt
        return ctxt

class FRS101(Taxonomy):
    def __init__(self, cfg):
        super().__init__(cfg, "frs-101")

class ContextDefinition:
    def __init__(self):
        self.period = None
        self.instant = None
        self.entity = None
        self.segments = {}
    def set_period(self, start, end):
        self.period = (start, end)
    def set_instant(self, instant):
        self.instant = instant
    def set_entity(self, id):
        self.entity = id
    def add_segments(self, id, tx):
        segs = tx.get_tag_dimensions(id)
        if segs:
            for k in segs:
                self.segments[k] = segs[k]
    def lookup_segment(self, id, val, tx):
        dim, seg = tx.lookup_dimension(id, val)
        self.segments[dim] = seg
    def get_key(self):
        segs = [
            "{0}:{1}".format(k, self.segments[k])
            for k in self.segments
        ]
        segs.sort()
        return (self.entity, self.period, self.instant, "//".join(segs))

class Context:
    def __init__(self, taxonomy, cdef):
        self.period = None
        self.taxonomy = taxonomy
        self.definition = cdef
    def create_money_fact(self, id, value):
        return self.taxonomy.create_money_fact(id, value, self)
    def create_count_fact(self, id, value):
        return self.taxonomy.create_count_fact(id, value, self)
    def create_string_fact(self, id, value):
        return self.taxonomy.create_string_fact(id, value, self)
    def create_bool_fact(self, id, value):
        return self.taxonomy.create_bool_fact(id, value, self)
    def create_date_fact(self, id, value):
        return self.taxonomy.create_date_fact(id, value, self)
    def describe(self):
        print("    Context:", self.id, ",", self.definition.get_key())

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

