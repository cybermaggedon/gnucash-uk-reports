
from . datum import StringDatum, DateDatum, MoneyDatum, BoolDatum
from . fact import StringFact, DateFact, MoneyFact, BoolFact

class Taxonomy:
    def __init__(self, cfg, name):
        self.cfg = cfg
        self.name = name
        self.contexts = {}
        self.next_context_id = 0

    def get_context_id(self, ctxt):
        if ctxt in self.contexts:
            return self.contexts[ctxt]

        self.contexts[ctxt] = "ctxt-" + str(self.next_context_id)
        self.next_context_id += 1
        return self.contexts[ctxt]

    def create_fact(self, val):

        if isinstance(val, StringDatum):
            fact =  StringFact(
                self.get_context_id(val.context),
                self.get_tag_name(val.id),
                val.value
            )
            return fact

        if isinstance(val, DateDatum):
            fact =  DateFact(
                self.get_context_id(val.context),
                self.get_tag_name(val.id),
                val.value
            )
            return fact

        if isinstance(val, MoneyDatum):
            fact =  MoneyFact(
                self.get_context_id(val.context),
                self.get_tag_name(val.id),
                val.value
            )
            return fact

        if isinstance(val, BoolDatum):
            fact =  BoolFact(
                self.get_context_id(val.context),
                self.get_tag_name(val.id),
                val.value
            )
            return fact

        raise RuntimeError("Not implemented: " + str(type(val)))

    def get_tag_name(self, id):
        key = "taxonomy.{0}.tags.{1}".format(self.name, id)
        return self.cfg.get(key)

    def get_sign_reversed(self, id):
        key = "taxonomy.{0}.sign-reversed.{1}".format(self.name, id)
        return self.cfg.get_bool(key)

    def get_time_dimension(self, id):
        key = "taxonomy.{0}.time-dimension.{1}".format(self.name, id)
        return self.cfg.get(key)

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

    def create_number_fact(self, id, value, context):
        m = NumberFact(value, context)
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
        
class FRS101(Taxonomy):
    def __init__(self, cfg):
        super().__init__(cfg, "frs-101")
