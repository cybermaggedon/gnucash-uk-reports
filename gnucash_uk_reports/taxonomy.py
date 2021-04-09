
from . datum import (
    StringDatum, DateDatum, MoneyDatum, BoolDatum, CountDatum, NumberDatum
)
from . fact import (
    StringFact, DateFact, MoneyFact, BoolFact, CountFact, NumberFact
)

from . period import Period
from . config import NoneValue

from datetime import datetime

class Taxonomy:
    def __init__(self, cfg, name):
        self.cfg = cfg
        self.name = name
        self.contexts = {}
        self.next_context_id = 0
        self.contexts_used = set()

    def get_context_id(self, ctxt):
        if ctxt in self.contexts:
            return self.contexts[ctxt]

        self.contexts[ctxt] = "ctxt-" + str(self.next_context_id)
        self.next_context_id += 1
        return self.contexts[ctxt]

    def create_fact(self, val):

        if isinstance(val, StringDatum):
            return self.create_string_fact(val)

        if isinstance(val, DateDatum):
            return self.create_date_fact(val)

        if isinstance(val, MoneyDatum):
            return self.create_money_fact(val)

        if isinstance(val, BoolDatum):
            return self.create_bool_fact(val)

        if isinstance(val, CountDatum):
            return self.create_count_fact(val)

        if isinstance(val, NumberDatum):
            return self.create_number_fact(val)

        raise RuntimeError("Not implemented: " + str(type(val)))

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

    def observe_fact(self, fact):
        # Keep track of which contexts are used.  Contexts which are
        # used by facts with no names don't need to be describe in the
        # output.
        if fact.name:
            self.contexts_used.add(fact.context)

    def create_money_fact(self, val):
        fact = MoneyFact(self.get_context_id(val.context),
                         self.get_tag_name(val.id), val.value,
                         self.get_sign_reversed(val.id))
        fact.dimensions = self.get_tag_dimensions(val.id)
        self.observe_fact(fact)
        return fact

    def create_count_fact(self, val):
        fact = CountFact(self.get_context_id(val.context),
                         self.get_tag_name(val.id), val.value)
        fact.dimensions = self.get_tag_dimensions(val.id)
        self.observe_fact(fact)
        return fact

    def create_number_fact(self, val):
        fact = NumberFact(self.get_context_id(val.context),
                          self.get_tag_name(val.id), val.value,
                          self.get_sign_reversed(val.id))
        fact.dimensions = self.get_tag_dimensions(val.id)
        self.observe_fact(fact)
        return fact

    def create_string_fact(self, val):
        fact = StringFact(self.get_context_id(val.context),
                          self.get_tag_name(val.id), val.value)
        fact.dimensions = self.get_tag_dimensions(val.id)
        self.observe_fact(fact)
        return fact

    def create_bool_fact(self, val):
        fact = BoolFact(self.get_context_id(val.context),
                        self.get_tag_name(val.id), val.value)
        fact.dimensions = self.get_tag_dimensions(val.id)
        self.observe_fact(fact)
        return fact

    def create_date_fact(self, val):
        fact = DateFact(self.get_context_id(val.context),
                        self.get_tag_name(val.id), val.value)
        fact.dimensions = self.get_tag_dimensions(val.id)
        self.observe_fact(fact)
        return fact

    def create_context(self, cdef):

        key = cdef.get_key()

        if key in self.contexts:
            return self.contexts[key]

        ctxt = Context(self, cdef)
        ctxt.id = "ctxt-" + str(self.next_context_id)
        self.next_context_id += 1
        self.contexts[key] = ctxt
        return ctxt

    def get_namespaces(self):
        key = "taxonomy.{0}.namespaces".format(self.name)
        return self.cfg.get(key)

    def get_schema(self):
        key = "taxonomy.{0}.schema".format(self.name)
        return self.cfg.get(key)

    def get_predefined_contexts(self, data):

        contexts = {}

        for c in self.cfg.get("taxonomy.{0}.contexts".format(self.name)):

            ctxt = None

            if c.get("from"):
                ctxt = contexts[c.get("from")]
            else:
                ctxt = data.get_root_context()

            if c.get("entity"):
                scheme_def = c.get("scheme")
                scheme = data.get_config(scheme_def, scheme_def)
                entity_def = c.get("entity")
                entity = data.get_config(entity_def, entity_def)
                ctxt = ctxt.with_entity(scheme, entity)

            if c.get("period"):
                period_def = c.get("period")
                period = Period.load(data.get_config(period_def))
                ctxt = ctxt.with_period(period)

            if c.get("instant"):
                instant_def = c.get("instant")
                instant = data.get_config_date(instant_def)
                ctxt = ctxt.with_instant(instant)

            if c.get("segments"):
                segments = c.get("segments")

                for k, v in segments.items():
                    v = data.get_config(v, v)
                    segments[k] = v
                    
                ctxt = ctxt.with_segments(segments)

            contexts[c.get("id")] = ctxt

        return contexts

    def get_metadata(self, data):

        ctxts = self.get_predefined_contexts(data)

        meta = []

        key = "taxonomy.{0}.document-metadata".format(self.name)
        for c in self.cfg.get(key):

            id = c.get("id")
            context = ctxts[c.get("context")]

            if c.get("config"):
                value_def = c.get("config")
                value = data.get_config(value_def)
            else:
                value = c.get("value")

            # Ignore missing values
            if isinstance(value, NoneValue):
                continue

            kind = c.get("kind")
            if kind == "date":
                value = datetime.fromisoformat(value).date()
                datum = DateDatum(id, value, context)
            elif kind == "bool":
                value = bool(value)
                datum = BoolDatum(id, value, context)
            elif kind == "money":
                datum = MoneyDatum(id, value, context)
            elif kind == "count":
                datum = CountDatum(id, value, context)
            elif kind == "number":
                datum = NumberDatum(id, value, context)
            else:
                datum = StringDatum(id, value, context)
            fact = self.create_fact(datum)

            meta.append(fact)

        return meta

    def get_context(self, id, cfg, instant=None, period=None):
        key = "taxonomy.{0}.contexts.{1}".format(self.name, id)
        ccfg = self.cfg.get(key)

        cdef = ContextDefinition()

        def use_instant(val):
            f = val.get("from")
            if f == "config":
                key = val.get("key")
                cdef.set_instant(cfg.get_date(val.get("key")))
            elif f == "defined":
                if instant == None:
                    raise RuntimeError("Required instant not supplied")
                cdef.set_instant(instant)
            else:
                raise RuntimeError("Instant from '%s' means nothing" % f)
            
        ccfg.get("instant").use(use_instant)

        def use_period(val):
            f = val.get("from")
            if f == "config":
                key = val.get("key")
                period = Period.load(cfg.get(val.get("key")))
                cdef.set_period(period.start, period.end)
            elif f == "defined":
                if period == None:
                    raise RuntimeError("Required period not supplied")
                cdef.set_instant(period.start, period.end)
            else:
                raise RuntimeError("Period from '%s' means nothing" % f)
            
        ccfg.get("period").use(use_period)

        def use_entity(val):
            f = val.get("from")
            if f == "config":
                key = val.get("key")
                scheme = val.get("scheme")
                cdef.set_entity(cfg.get(val.get("key")))
            else:
                raise RuntimeError("Entity from '%s' means nothing" % f)
            
        ccfg.get("entity").use(use_entity)

        ctxt = self.create_context(cdef)

        return ctxt
        
#class FRS101(Taxonomy):
#    def __init__(self, cfg):
#        super().__init__(cfg, "frs-101")
