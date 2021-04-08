
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

        period = self.get_report_period()
        rpc = self.business_context.with_period(period)

        country = self.cfg.get("metadata.business.contact.country")

        c = rpc.with_segments({"countries-regions": country})

        d = ValueSet()

        val = self.cfg.get("metadata.business.contact.name")
        d.add_string("contact-name", val, c)

        # FIXME: Address type missing???
        val = self.cfg.get("metadata.business.contact.address")
        for i in range(0, 3):
            if len(val) > i:
                d.add_string("contact-address" + str(i + 1), val[i], c)

        val = self.cfg.get("metadata.business.contact.location")
        d.add_string("contact-location", val, c)

        val = self.cfg.get("metadata.business.contact.county")
        d.add_string("contact-county", val, c)

        val = self.cfg.get("metadata.business.contact.postcode")
        d.add_string("contact-postcode", val, c)

        val = self.cfg.get("metadata.business.contact.country")
        d.add_string("contact-country", val, c)

        val = self.cfg.get("metadata.business.contact.email")
        d.add_string("contact-email", val, rpc)

        pc = rpc

        phone_type = self.cfg.get("metadata.business.contact.phone.type")
        if phone_type:
            pc = rpc.with_segments({"phone-number-type": phone_type})

        self.cfg.get("metadata.business.contact.phone.country").use(
            lambda val: d.add_string("contact-phone-country", val, pc)
        )
        self.cfg.get("metadata.business.contact.phone.area").use(
            lambda val: d.add_string("contact-phone-area", val, pc)
        )
        self.cfg.get("metadata.business.contact.phone.number").use(
            lambda val: d.add_string("contact-phone-number", val, pc)
        )

        self.cfg.get("metadata.business.website.url").use(
            lambda val: d.add_string("website-url", val, c)
        )

        self.cfg.get("metadata.business.website.description").use(
            lambda val: d.add_string("website-description", val, c)
        )

        return d

    def get_report_period(self, i=0):

        return Period.load(self.cfg.get("metadata.report.periods." + str(i)))

    def get_report_date(self):

        return self.cfg.get_date("metadata.report.date")

    def get_company_information(self):

        d = ValueSet()

        period = self.get_report_period()
        c = self.business_context.with_period(period)

        date = self.get_report_date()
        rdc = self.business_context.with_instant(date)

        self.cfg.get("metadata.business.company-name").use(
            lambda val: d.add_string("company-name", val, c)
        )

        self.cfg.get("metadata.business.company-number").use(
            lambda val: d.add_string("company-number", val, c)
        )

        self.cfg.get("metadata.business.vat-registration").use(
            lambda val: d.add_string("vat-registration", val, c)
        )

        directors = self.cfg.get("metadata.business.directors")
        signed_by = self.cfg.get("metadata.report.signed-by")
        for i in range(0, len(directors)):
            dirc = c.with_segment("officer", "director" + str(i + 1))
            d.add_string("director" + str(i + 1), directors[i], dirc)
            if signed_by == directors[i]:
                d.add_string("signed-by", "", dirc)

        self.cfg.get("metadata.business.activities").use(
            lambda val: d.add_string("activities", val, c)
        )

        val = self.cfg.get("metadata.business.sic-codes")
        for i in range(0, 3):
            if len(val) > i:
                d.add_string("sic" + str(i + 1), val[i], c)

        self.cfg.get("metadata.business.industry-sector").use(
            lambda val:
            d.add_string(
                "industry-sector", "", c.with_segment("industry-sector", val)
            )
        )

        self.cfg.get_bool("metadata.business.is-dormant").use(
            lambda val: d.add_bool("is-dormant", val, c)
        )

        self.cfg.get("metadata.business.company-formation.form").use(
            lambda val:
            d.add_string(
                "entity-legal-form", "",
                c.with_segment("entity-legal-form", val)
            )
        )

        self.cfg.get("metadata.business.company-formation.country").use(
            lambda val:
            d.add_string(
                "entity-legal-country", "",
                c.with_segment("countries-regions", val)
            )
        )

        self.cfg.get_date("metadata.business.company-formation.date").use(
            lambda val:
            d.add_date("entity-legal-date", val, rdc)
        )

        return d

    def get_report_information(self):

        d = ValueSet()

        period = self.get_report_period()
        c = self.business_context.with_period(period)

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

        self.cfg.get_date("metadata.report.balance-sheet-date").use(
            lambda val: d.add_date("balance-sheet-date", val, rdc)
        )

        self.cfg.get("metadata.report.accounting-standards").use(
            lambda val:
            d.add_string(
                "accounting-standards", "",
                c.with_segment("accounting-standards", val)
            )
        )

        self.cfg.get("metadata.report.accounts-type").use(
            lambda val:
            d.add_string(
                "accounts-type", "",
                c.with_segment("accounts-type", val)
            )
        )

        self.cfg.get("metadata.report.accounts-status").use(
            lambda val:
            d.add_string(
                "accounts-status", "",
                c.with_segment("accounts-status", val)
            )
        )

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

