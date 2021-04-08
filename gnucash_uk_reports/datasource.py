
from . period import Period
from . context import Context
from . computation import get_computations, Result
from . valueset import ValueSet
from . multi_period import MultiPeriodWorksheet
from . element import Element

class DataSource:
    def __init__(self, cfg, session):

        self.cfg = cfg
        self.session = session

        self.root_context = Context(None)
        self.business_context = self.root_context.with_entity(
            "http://www.companieshouse.gov.uk/",
            self.cfg.get("metadata.business.company-number")
        )
        self.computations = get_computations(cfg, self.business_context)
        self.results = {}

    def get_contact_information(self):

        c = self.business_context.with_segments({"country": "UK"})

        d = ValueSet(c)

        val = self.cfg.get("metadata.business.contact.name")
        d.add_string("contact-name", val)

        return d

    def get_report_period(self):

        return Period.load(self.cfg.get("metadata.report.periods.0"))

    def get_report_date(self):

        return self.cfg.get_date("metadata.report.date")

    def get_company_information(self):

        d = ValueSet()

        period = self.get_report_period()
        c = self.business_context.with_period(period)

        self.cfg.get("metadata.business.company-name").use(
            lambda val: d.add_string("company-name", val, c)
        )

        self.cfg.get("metadata.business.company-number").use(
            lambda val: d.add_string("company-number", val, c)
        )

        directors = self.cfg.get("metadata.business.directors")
        signed_by = self.cfg.get("metadata.report.signed-by")
        for i in range(0, len(directors)):
            dirc = c.with_segment("officer", "director" + str(i + 1))
            d.add_string("director" + str(i + 1), directors[i], dirc)
            if signed_by == directors[i]:
                d.add_string("signed-by", signed_by, dirc)

        return d

    def get_report_information(self):

        d = ValueSet()

        period = self.get_report_period()
        rpc = self.business_context.with_period(period)

        date = self.get_report_date()
        rdc = self.business_context.with_instant(date)

        self.cfg.get("metadata.report.title").use(
            lambda val: d.add_string("report-title", val, rpc)
        )

        self.cfg.get("metadata.report.periods.0").use(
            lambda val: (
                d.add_date("period-start", val.get_date("start"), rdc),
                d.add_date("period-end", val.get_date("end"), rdc)
            )
        )

        self.cfg.get_date("metadata.report.date").use(
            lambda val: d.add_date("report-date", val, rdc)
        )

        return d

    #director??? : ???
    # signer

    # approved for publication, issue date

    def get_contact_information(self):

        c = self.business_context.with_segments({"country": "UK"})

        d = ValueSet(c)

        val = self.cfg.get("metadata.business.contact.name")
        d.add_string("contact-name", val)

        return d

    def get_computation(self, id):
        if id in self.computations:
            return self.computations[id]
        raise RuntimeError("No such computation '%s'" % id)

    def perform_computations(self, period):

        c = self.business_context.with_period(period)

        if c not in self.results:
            res = Result()
            self.results[c] = res

            for comp in self.computations.values():
                comp.compute(self.session, period.start, period.end, res)

        return self.results[c]

    def get_results(self, ids, period):

        res = perform_computations(period)

        res = self.results[c]

        d = ValueSet(c)
        for id in ids:
            d.add_money(id, res.get(id).value)

        return d

    def get_periods(self):
        return [
            Period.load(period)
            for period in self.cfg.get("metadata.report.periods")
        ]

    def get_worksheet(self, id):

        for ws_def in self.cfg.get("worksheets"):

            if ws_def.get("id") == id:

                kind = ws_def.get("kind")

                if kind == "multi-period":
                    return MultiPeriodWorksheet.load(ws_def, self)

                raise RuntimeError("Don't know worksheet type '%s'" % kind)

        raise RuntimeError("Could not find worksheet '%s'" % id)

    def get_element(self, id):

        elt_defs = self.cfg.get("elements")

        for elt_def in elt_defs:

            if elt_def.get("id") == id:
                return Element.load(elt_def, self)

        raise RuntimeError("Could not find element '%s'" % id)

    def get_config(self, key):
        return self.cfg.get(key)

