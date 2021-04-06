
from . period import Period

from . fact import *

from xml.dom.minidom import getDOMImplementation
from xml.dom import XHTML_NAMESPACE
import json
from datetime import datetime

software = "gnucash-uk-reports"
software_version = "0.0.1"

accounting_standards = {
    "frsse": "uk-bus:FRSSE",
    "frs101": "uk-bus:FRS101",
    "frs102": "uk-bus:FRS102",
    "full-irs": "uk-bus:FullIFRS",
    "small-entities-regime": "uk-bus:SmallEntities",
    "micro-entities": "uk-bus:Micro-entities",
    "other-standards": "uk-bus:OtherStandards"
}

accounts_status = {
    "audited": "uk-bus:Audited",
    "audit-exempt-no-accountants-report": "uk-bus:AuditExempt-NoAccountantsReport",
    "audit-exempt-with-accountants-report": "uk-bus:AuditExemptWithAccountantsReport",
    "independent-examination": "uk-bus:IndependentExaminationCharity",
    "other-reporting-regime": "uk-bus:OtherReportingRegime"
}

accounts_type = {
    "full-accounts": "uk-bus:FullAccounts",
    "abbreviated-accounts": "uk-bus:AbbreviatedAccounts",
    "abridged-accounts": "uk-bus:AbridgedAccounts"
}

country_names = {
    "UK": "uk-geo:UnitedKingdom",
    "england-and-wales": "uk-geo:EnglandWales"
}

formation_forms = {
    "private-limited-company": "Private limited company, Ltd",
    "public-limited-company-plc": "Public limited company, PLC",
    "public-limited-company-not-quoted": "Public limited company, PLC, not quoted on any exchange",
    "company-limited-by-guarantee": "Company limited by guarantee",
    "unlimited-company": "Unlimited company",
    "limited-liability-partnership": "Limited liability partnership, LLP",
    "registered-charity": "Registered charity",
    "community-interest-company": "Community interest company, CIC",
    "industrial-and-provident-society": "Industrial and provident society",
    "friendly-society": "Friendly society",
    "incorporated-by-act-of-parliament": "Incorporated by Act of Parliament",
    "incorporated-by-royal-charter": "Incorporated by Royal Charter",
    "scottish-partnership": "Scottish partnership",
    "other-incorporated-association": "Other incorporated association",
    "branch-trading-in-uk": "Branch trading in UK",
    "other-uk": "Other UK",
    "other-non-uk": "Other non-UK"
}

formation_form_name = {
    "private-limited-company": "uk-bus:PrivateLimitedCompanyLtd",
    "public-limited-company-plc": "uk-bus:PublicLimitedCompanyPLC",
    "public-limited-company-not-quoted": "uk-bus:PublicLimitedCompanyPLCNotQuotedOnAnyExchange",
    "company-limited-by-guarantee": "uk-bus:CompanyLimitedByGuarantee",
    "unlimited-company": "uk-bus:UnlimitedCompany",
    "limited-liability-partnership": "uk-bus:LimitedLiabilityPartnershipLLP",
    "registered-charity": "uk-bus:RegisteredCharity",
    "community-interest-company": "uk-bus:CommunityInterestCompanyCIC",
    "industrial-and-provident-society": "uk-bus:IndustrialProvidentSociety",
    "friendly-society": "uk-bus:FriendlySociety",
    "incorporated-by-act-of-parliament": "uk-bus:IncorporatedByActParliament",
    "incorporated-by-royal-charter": "uk-bus:IncorporatedByRoyalCharter",
    "scottish-partnership": "uk-bus:ScottishPartnership",
    "other-incorporated-association": "uk-bus:OtherIncorporatedAssociation",
    "branch-trading-in-uk": "uk-bus:BranchTradingInUK",
    "other-uk": "uk-bus:OtherUK",
    "other-non-uk": "uk-bus:OtherNon-UK"
}

industry_sectors = {
    "a": "Agriculture, forestry and fishing",
    "b": "Mining and quarrying",
    "c": "Manufacturing",
    "d": "Electricity, gas, steam and air conditioning supply",
    "e": "Water supply, sewerage, waste management and remediation activities",
    "f": "Construction",
    "g": "Wholesale and retail trade, repair of motor vehicles and motorcycles",
    "h": "Transportation and storage",
    "i": "Accommodation and food service activities",
    "j": "Information and communication",
    "k": "Financial and insurance activities",
    "l": "Real estate activities",
    "m": "Professional, scientific and technical activities",
    "n": "Administrative and support service activities",
    "o": "Public administration and defence, compulsory social security",
    "p": "Education",
    "q": "Human health and social work activities",
    "r": "Arts, entertainment and recreation",
    "s": "Other service activities"
}

industry_sector_names = {
    "a": "uk-bus:A-AgricultureForestryFishing",
    "b": "uk-bus:B-MiningQuarrying",
    "c": "uk-bus:C-Manufacturing",
    "d": "uk-bus:D-ElectricityGasSteamAirConditioningSupply",
    "e": "uk-bus:E-WaterSupplySewerageWasteManagementRemediationActivities",
    "f": "uk-bus:F-Construction",
    "g": "uk-bus:G-WholesaleRetailTradeRepairMotorVehiclesMotorcycles",
    "h": "uk-bus:H-TransportationStorage",
    "i": "uk-bus:I-AccommodationFoodServiceActivities",
    "j": "uk-bus:J-InformationCommunication",
    "k": "uk-bus:K-FinancialInsuranceActivities",
    "l": "uk-bus:L-RealEstateActivities",
    "m": "uk-bus:M-ProfessionalScientificTechnicalActivities",
    "n": "uk-bus:N-AdministrativeSupportServiceActivities",
    "o": "uk-bus:O-PublicAdministrationDefenceCompulsorySocialSecurity",
    "p": "uk-bus:P-Education",
    "q": "uk-bus:Q-HumanHealthSocialWorkActivities",
    "r": "uk-bus:R-ArtsEntertainmentRecreation",
    "s": "uk-bus:S-OtherServiceActivities"
}

class BasicElement:

    def __init__(self, metadata, tx):
        self.metadata = metadata
        self.taxonomy = tx

    @staticmethod
    def load(elt_def, cfg, session, tx):

        kind = elt_def.get("kind")

        if kind == "composite":
            from . composite import Composite
            return Composite.load(elt_def, cfg, session, tx)

        if kind == "title":
            from . title import Title
            return Title.load(elt_def, cfg, tx)

        if kind == "worksheet":
            from . worksheetelement import WorksheetElement
            return WorksheetElement.load(elt_def, cfg, session, tx)

        if kind == "notes":
            from . notes import NotesElement
            return NotesElement.load(elt_def, cfg, tx)

        if kind == "ct600":
            from . ct600 import CT600
            return CT600.load(elt_def, cfg, session, tx)

        raise RuntimeError("Don't know element kind '%s'" % kind)

    def add_style(self, elt):

        return

        doc = self.doc
        
        style = doc.createElement("style")
        style.setAttribute("type", "text/css")
        elt.appendChild(style)
            
        style_text = """

h2 {
  page-break-before: always;
}

@media screen, projection, tv {

  body {
    margin: 2% 4% 2% 4%;
    background-color: gray;
  }

  DIV.page {

    background-color: white;
    padding: 2em;

    /* CSS hack for cross browser minimum height */
    min-height: 29.7cm;

    height: 29.7cm;
    width: 21cm;

    margin: 2em 0;

  }

  DIV.title.page h1 {
    margin: 4rem 4rem 0.5rem 4rem;
    padding: 0;
  }

  DIV.title.page DIV.subheading {
    font-weight: bold;
    margin: 0.5rem 4em 2rem 4em;
    padding: 0;
  }

  DIV.title.page DIV.information {
    margin: 0.2em 4em 0.2em 4em;
    padding: 0;
  }

  DIV.title.page DIV.signature {
    padding: 4rem;
  }

}

.sheet {
  display: grid;
  grid-template-columns: 20rem repeat(10, 10rem);
  grid-template-rows: auto;
  column-gap: 1rem;
  row-gap: 0.2rem;
  padding: 1rem;
}

.header {
  font-weight: bold;
  margin-top: 1em;
}

.label {
  grid-column: 1;
}

.label.breakdown.header {
  grid-column: 1 / span 10;
}

.label.item {
  padding-left: 2em;
}

.value {
  font-family: Source Code Pro, monospace;
  font-size: 10pt;
}

@media print {
  .value {
    font-family: Source Code Pro, monospace;
    font-size: 1rem;
  }
  * {
    font-size: 1rem;
  }
  .sheet {
    grid-template-columns: 40% repeat(10, 20%);
  }
}

.total.value {
  margin-top: 1em;
}

.breakdown.total {
  margin-top: 0.2em;
  padding-top: 4px;
  border-top: 1px solid white;
}

.breakdown.total.value {
  border-top: 1px solid #808080;
}

.periodname {
  padding: 0.5em 1em 0.5em 1em;
  border-bottom: 0.2em solid black;
  font-weight: bold;
  justify-self: stretch;
  align-self: stretch;
  text-align: center;
}

.currency {
  justify-self: end;
  padding-right: 1em;
}

.period.value {
  text-align: right;
  padding-right: 2.2em;
}

.period.value.negative {
  color: #400000;
  padding-right: 1em;
}

.period.value.nil {
  color: #a0a0a0;
}

.hidden {
  display: none;
}

        """

        style.appendChild(doc.createTextNode(style_text))

    def to_html(self, out):

        impl = getDOMImplementation()

        self.periods = [
            Period.load(v)
            for v in self.metadata.get("report").get("periods")
        ]
        
        doc = impl.createDocument(None, "html", None)
        self.doc = doc

        html = self.doc.documentElement

        html.setAttribute("xmlns", XHTML_NAMESPACE)

        self.html = html

        head = doc.createElement("head")
        html.appendChild(head)

        self.add_style(head)

        body = doc.createElement("body")
        html.appendChild(body)

        elt = self.to_ixbrl_elt(self)

        def walk(elt):
            if elt.nodeType == elt.ELEMENT_NODE:

                # Remove ixbrl stuff, just turn tags into span tags.
                if elt.tagName[:3] == "ix:":
                    try:
                        elt.removeAttribute("contextRef")
                    except: pass
                    try:
                        elt.removeAttribute("name")
                    except: pass
                    try:
                        elt.removeAttribute("format")
                    except: pass
                    try:
                        elt.removeAttribute("unitRef")
                    except: pass
                    try:
                        elt.removeAttribute("decimals")
                    except: pass
                    elt.tagName = "span"
                if elt.childNodes:
                    for e in elt.childNodes:
                        walk(e)

        walk(elt)

        body.appendChild(elt)

#        out.write(doc.toprettyxml())
        out.write(doc.toxml())


    def to_ixbrl(self, out):

        impl = getDOMImplementation()

        self.periods = [
            Period.load(v)
            for v in self.metadata.get("report").get("periods")
        ]
        
        doc = impl.createDocument(None, "html", None)
        self.doc = doc

        html = self.doc.documentElement

        html.setAttribute("xmlns", XHTML_NAMESPACE)

        # FIXME: Hard-coded
        html.setAttribute("xmlns:ix", "http://www.xbrl.org/2013/inlineXBRL")
        html.setAttribute("xmlns:uk-bus",
                          "http://xbrl.frc.org.uk/cd/2021-01-01/business")
        html.setAttribute("xmlns:uk-geo",
                          "http://xbrl.frc.org.uk/cd/2021-01-01/countries")
        html.setAttribute("xmlns:uk-core", 
                          "http://xbrl.frc.org.uk/fr/2021-01-01/core")
        html.setAttribute("xmlns:uk-direp", "http://xbrl.frc.org.uk/reports/2021-01-01/direp")
        html.setAttribute("xmlns:link", "http://www.xbrl.org/2003/linkbase")
        html.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
        html.setAttribute("xmlns:xbrli", "http://www.xbrl.org/2003/instance")
        html.setAttribute("xmlns:xbrldi", "http://xbrl.org/2006/xbrldi")
        html.setAttribute("xmlns:ixt2",
                          "http://www.xbrl.org/inlineXBRL/transformation/2011-07-31")
        html.setAttribute("xmlns:iso4217", "http://www.xbrl.org/2003/iso4217")

        self.html = html

        head = doc.createElement("head")
        html.appendChild(head)

        def add_title(val):
            t = doc.createElement("title");
            t.appendChild(doc.createTextNode(val));
            head.appendChild(t)

        self.metadata.get("report").get("title").use(add_title)

        self.add_style(head)

        body = doc.createElement("body")
        html.appendChild(body)

        hiddev = doc.createElement("div")
        hiddev.setAttribute("class", "hidden")
        body.appendChild(hiddev)

        hdr = doc.createElement("ix:header")
        hiddev.appendChild(hdr)

        hidden = doc.createElement("ix:hidden")
        hdr.appendChild(hidden)
        self.hidden = hidden

        refs = doc.createElement("ix:references")
        hdr.appendChild(refs)
       
        resources = doc.createElement("ix:resources")
        hdr.appendChild(resources)
        self.resources = resources

        self.create_metadata()

        self.create_contexts()

        currency = self.metadata.get("report").get("currency")

        unit = doc.createElement("xbrli:unit")
        unit.setAttribute("id", currency)
        measure = doc.createElement("xbrli:measure")
        measure.appendChild(doc.createTextNode("iso4217:" + currency))
        unit.appendChild(measure)
        resources.appendChild(unit)

        unit = doc.createElement("xbrli:unit")
        unit.setAttribute("id", "pure")
        measure = doc.createElement("xbrli:measure")
        measure.appendChild(doc.createTextNode("xbrli:pure"))
        unit.appendChild(measure)
        resources.appendChild(unit)
       
        frc_schema = "https://xbrl.frc.org.uk/FRS-102/2021-01-01/FRS-102-2021-01-01.xsd"        
        schema = doc.createElement("link:schemaRef")
        schema.setAttribute("xlink:type", "simple")
        schema.setAttribute("xlink:href", frc_schema)
        schema.appendChild(doc.createTextNode(""))
        refs.appendChild(schema)

        elt = self.to_ixbrl_elt(self)
        body.appendChild(elt)

        out.write(doc.toprettyxml())
#        out.write(doc.toxml())

    def create_contexts(self):

        report = self.metadata.get("report")
        business = self.metadata.get("business")

#        report_date = report.get("date")

        company_number = business.get("company-number")

        for key in self.taxonomy.contexts:

            ctxt = self.taxonomy.contexts[key]
            cdef = ctxt.definition

            segs = [
                self.create_segment_member(k, cdef.segments[k])
                for k in cdef.segments
            ]

            crit = [
                self.create_entity(company_number, segs)
            ]

            if cdef.period:
                crit.append(self.create_period(cdef.period[0], cdef.period[1]))

            if cdef.instant:
                crit.append(self.create_instant_period(cdef.instant))

            ce = self.create_context(ctxt.id, crit)

            self.resources.appendChild(ce)

        return

        report = self.metadata.get("report")
        business = self.metadata.get("business")

        report_date = report.get("date")

        company_number = business.get("company-number")

        directors = business.get("directors")

        # report-date
        self.resources.appendChild(self.create_context("report-date", [
            self.create_entity(company_number),
            self.create_instant_period(report_date)
        ]))

        # period-<n> (report periods)
        for i in range(0, len(self.periods)):
            self.resources.appendChild(self.create_context("period-" + str(i), [
                self.create_entity(company_number),
                self.create_period(self.periods[i])
            ]))

        # entity-trading-<n> (report periods)
        for i in range(0, len(self.periods)):
            self.resources.appendChild(self.create_context("entity-trading-" + str(i), [
                self.create_entity(company_number),
                self.create_period(self.periods[i])
            ]))

        # director<n>
        for i in range(0, len(directors)):
            name = "officer-" + str(i + 1)
            self.resources.appendChild(self.create_context(name, [
                self.create_entity(company_number,
                                   [
                                       self.create_segment_member("uk-bus:EntityOfficersDimension",
                                                                  "uk-bus:Director" + str(i + 1))
                                   ]),
                self.create_period(self.periods[0])
            ]))

        # formation-form
        form = business.get("company-formation").get("form")
        if form:
            if form in formation_forms:
                self.resources.appendChild(
                    self.create_context("formation-form", [
                        self.create_entity(company_number, [
                            self.create_segment_member("uk-bus:LegalFormEntityDimension",
                                                       formation_form_name[form])
                        ]),
                        self.create_period(self.periods[0])
                ])
            )

        # formation-country-0
        country = business.get("company-formation").get("country")
        if country:
            if country in country_names:
                self.resources.appendChild(
                    self.create_context("formation-country", [
                        self.create_entity(company_number, [
                            self.create_segment_member("uk-geo:CountriesRegionsDimension",
                                                       country_names[country])
                        ]),
                        self.create_period(self.periods[0])
                ])
            )

        # formation-date
        date = business.get("company-formation").get("date")
        if date:
            self.resources.appendChild(
                self.create_context("formation-date", [
                    self.create_entity(company_number, []),
                    self.create_instant_period(date)
                ])
            )

        # standards-period
        stds = report.get("accounting-standards")
        if stds != None and stds in accounting_standards:
            self.resources.appendChild(
                self.create_context("standards-period", [
                    self.create_entity(company_number, [
                        self.create_segment_member("uk-bus:AccountingStandardsDimension",
                                                   accounting_standards[stds])
                    ]),
                    self.create_period(self.periods[0])
                ])
            )

        # accounts-type-period
        actype = report.get("accounts-type")
        if actype != None and actype in accounts_type:
            self.resources.appendChild(
                self.create_context("accounts-type-period", [
                    self.create_entity(company_number, [
                        self.create_segment_member("uk-bus:AccountsTypeDimension",
                                                   accounts_type[actype]),
                    ]),
                    self.create_period(self.periods[0])
                ])
            )
                                

        # accounts-status-period
        stat = report.get("accounts-status")
        if stat != None and stat in accounts_status:
            self.resources.appendChild(
                self.create_context("accounts-status-period", [
                    self.create_entity(company_number, [
                        self.create_segment_member("uk-bus:AccountsStatusDimension",
                                                   accounts_status[stat])
                        ]),
                    self.create_period(self.periods[0])
                ])
            )

        # period-end-<n>
        for i in range(0, len(self.periods)):
            self.resources.appendChild(
                self.create_context("period-end-" + str(i), [
                    self.create_entity(company_number),
                    self.create_instant_period(self.periods[i].end)
                ])
            )

        # within-year-<n>
        for i in range(0, len(self.periods)):
            self.resources.appendChild(
                self.create_context("within-year-" + str(i), [
                    self.create_entity(company_number, [
                        self.create_segment_member("uk-core:MaturitiesOrExpirationPeriodsDimension",
                                                   "uk-core:WithinOneYear")
                    ]),
                    self.create_instant_period(self.periods[i].end)
                ])
            )

        # after-year-<n>
        for i in range(0, len(self.periods)):
            self.resources.appendChild(
                self.create_context("after-year-" + str(i), [
                    self.create_entity(company_number, [
                        self.create_segment_member("uk-core:MaturitiesOrExpirationPeriodsDimension",
                                                   "uk-core:AfterOneYear")
                    ]),
                    self.create_instant_period(self.periods[i].end)
                ])
            )

        # sector-0
        sector = business.get("industry-sector")
        if sector:
            if sector in industry_sectors:
                self.resources.appendChild(self.create_context("sector-0", [
                    self.create_entity(company_number, [
                        self.create_segment_member("uk-bus:MainIndustrySectorDimension",
                                                   industry_sector_names[sector])
                    ]),
                    self.create_period(self.periods[0])
                ]))

        # country-0
        country = business.get("contact").get("country")
        if country:
            if country in country_names:

                self.resources.appendChild(
                    self.create_context("country-0", [
                        self.create_entity(company_number, [
                            self.create_segment_member("uk-geo:CountriesRegionsDimension",
                                                       country_names[country])
                        ]), 
                        self.create_period(self.periods[0])
                    ])
                )

        # web-0
        country = business.get("contact").get("country")
        if country:
            if country in country_names:

                self.resources.appendChild(
                    self.create_context("web-0", [
                        self.create_entity(company_number, [
                            self.create_segment_member("uk-geo:CountriesRegionsDimension",
                                                       country_names[country])
                        ]), 
                        self.create_period(self.periods[0])
                    ])
                )

        # phone-0
        # FIXME: Hard-coded
        self.resources.appendChild(self.create_context("phone-0", [
            self.create_entity(company_number, [
                self.create_segment_member("uk-bus:PhoneNumberTypeDimension",
                                           "uk-bus:Landline")
            ]),
            self.create_period(self.periods[0])
        ]))

    def add_nn(self, par, name, ctxt, val):
        par.appendChild(self.make_nn(name, ctxt, val))

    def make_nn(self, name, ctxt, val):
        elt = self.doc.createElement("ix:nonNumeric")
        elt.setAttribute("name", name)
        elt.setAttribute("contextRef", ctxt)
        elt.appendChild(self.doc.createTextNode(val))
        return elt

    def add_date(self, par, name, ctxt, val):
        par.appendChild(self.make_date(name, ctxt, val))

    def make_date(self, name, ctxt, val):
        elt = self.doc.createElement("ix:nonNumeric")
        elt.setAttribute("name", name)
        elt.setAttribute("contextRef", ctxt)
        elt.setAttribute("format", "ixt2:datedaymonthyearen")
        elt.appendChild(self.doc.createTextNode(val.strftime("%d %B %Y")))
        return elt

    def add_number(self, par, name, ctxt, val, unit="GBP"):
        par.appendChild(self.make_number(name, ctxt, val, unit))

    def make_number(self, name, ctxt, val, unit="GBP"):

        elt = self.doc.createElement("ix:nonFraction")
        elt.setAttribute("name", name)

        elt.setAttribute("contextRef", ctxt)
        elt.setAttribute("format", "ixt2:numdotdecimal")
        elt.setAttribute("unitRef", unit)
        elt.setAttribute("decimals", "2")

        elt.appendChild(self.doc.createTextNode(str(val)))

        return elt

    def make_div(self, par, elts):
        div = self.doc.createElement("div")
        self.add_elts(div, elts)
        par.appendChild(div)
        return div

    def add_elts(self, par, elts):
        for elt in elts:
            par.appendChild(elt)

    def make_text(self, t):
        return self.doc.createTextNode(t)

    def create_context(self, id, elts):
        ctxt = self.doc.createElement("xbrli:context")
        ctxt.setAttribute("id", id)
        for elt in elts:
            ctxt.appendChild(elt)
        return ctxt

    def create_entity(self, id, elts=None):

        if elts == None:
            elts = []

        companies_house_url="http://www.companieshouse.gov.uk/"

        ent = self.doc.createElement("xbrli:entity")
        cid = self.doc.createElement("xbrli:identifier")
        cid.setAttribute("scheme", companies_house_url)
        cid.appendChild(self.doc.createTextNode(id))
        ent.appendChild(cid)

        for elt in elts:
            ent.appendChild(elt)

        return ent

    def create_instant_period(self, date):

        cperiod = self.doc.createElement("xbrli:period")

        instant = self.doc.createElement("xbrli:instant")
        instant.appendChild(self.doc.createTextNode(str(date)))
        cperiod.appendChild(instant)

        return cperiod

    def create_period(self, s, e):

        cperiod = self.doc.createElement("xbrli:period")

        start = self.doc.createElement("xbrli:startDate")
        start.appendChild(self.doc.createTextNode(str(s)))
        cperiod.appendChild(start)

        end = self.doc.createElement("xbrli:endDate")
        end.appendChild(self.doc.createTextNode(str(e)))
        cperiod.appendChild(end)

        return cperiod

    def create_segment_member(self, dim, value):

        seg = self.doc.createElement("xbrli:segment")

        expmem = self.doc.createElement("xbrldi:explicitMember")
        expmem.setAttribute("dimension", dim)
        expmem.appendChild(self.doc.createTextNode(value))
        seg.appendChild(expmem)

        return seg

    def create_metadata(self):
        report = self.metadata.get("report")
        business = self.metadata.get("business")

        company_number = business.get("company-number")
        report_date = report.get_date("date")

        report_date_cdef = ContextDefinition()
        report_date_cdef.set_instant(report_date)
        report_date_context = self.taxonomy.get_context(report_date_cdef)

        report_period_cdef = ContextDefinition()
        report_period_cdef.set_period(
            report.get("periods")[0].get_date("start"),
            report.get("periods")[0].get_date("end")
        )
        report_period_context = self.taxonomy.get_context(report_period_cdef)
        
        report_title_fact = report_date_context.create_string_fact(
            "report-title",
            report.get("title")
        )

        report_title_fact.append(self.doc, self.hidden)

        report_date_context.create_date_fact("report-date", report_date).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        report.get("periods")[0].get_date("start").use(
            lambda val:
            report_date_context.create_date_fact("period-start", val)
        ).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        report.get("periods")[0].get_date("end").use(
            lambda val:
            report_date_context.create_date_fact("period-end", val)
        ).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        report_period_context.create_string_fact("software", software).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        report_period_context.create_string_fact("software-version",
                                                 software_version).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        business.get("company-name").use(
            lambda val: report_period_context.create_string_fact(
                "company-name", val
            )
        ).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        business.get("company-number").use(
            lambda val: report_period_context.create_string_fact(
                "company-number", val
            )
        ).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        business.get("vat-registration").use(
            lambda val: report_period_context.create_string_fact(
                "vat-registration", val
            )
        ).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        report.get_date("statement-date").use(
            lambda val: report_period_context.create_date_fact(
                "balance-sheet-date", val
            )
        ).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        return

        report.get_date("statement-date").use(
            lambda val:
            self.add_date(self.hidden, "uk-bus:BalanceSheetDate",
                          "report-date", val)
        )

        business.get("activities").use(
            lambda val: self.add_nn(self.hidden,
                               "uk-bus:DescriptionPrincipalActivities",
                               "period-0", val)
        )

        def add_sic_codes(val):
            for i in range(0, 3):
                if len(val) > (i):
                    nm = "uk-bus:SICCodeRecordedUKCompaniesHouse{0}".format(i+1)
                    self.add_nn(self.hidden, nm, "period-0", val[i])
                
        business.get("sic-codes").use(
            lambda val: add_sic_codes(val)
        )

        sector = business.get("industry-sector")
        if sector:
            if sector in industry_sectors:
                self.add_nn(self.hidden, "uk-bus:MainIndustrySector",
                            "sector-0", "")

        business.get("is-dormant").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:EntityDormantTruefalse",
                                    "period-0", json.dumps(val))
        )

        self.add_nn(self.hidden, "uk-bus:EntityTradingStatus",
                    "entity-trading-0", "")

        report.get("accounting-standards").use(
            lambda x:
            self.add_nn(self.hidden, "uk-bus:AccountingStandardsApplied",
                        "standards-period", "")
        )

        report.get("accounts-type").use(
            lambda x:
            self.add_nn(self.hidden, "uk-bus:AccountsTypeFullOrAbbreviated",
                        "accounts-type-period", "")
        )

        report.get("accounts-status").use(
            lambda x:
            self.add_nn(self.hidden, "uk-bus:AccountsStatusAuditedOrUnaudited",
                        "accounts-status-period", "")
        )

        form = business.get("company-formation.form")
        if form:
            if form in formation_forms:
                self.add_nn(self.hidden, "uk-bus:LegalFormEntity",
                            "formation-form", "")

        country = business.get("company-formation.country")
        if country:
            if country in country_names:
                self.add_nn(self.hidden,
                            "uk-bus:CountryFormationOrIncorporation",
                            "formation-country", "")

        date = business.get("company-formation.date")
        self.add_nn(self.hidden,
                    "uk-bus:DateFormationOrIncorporation",
                    "formation-date", date)

        def add_avg_employee_counts(val):
            for i in range(0, len(val)):

                elt = self.doc.createElement("ix:nonFraction")
                elt.setAttribute("name", "uk-core:AverageNumberEmployeesDuringPeriod")
                elt.setAttribute("contextRef", "period-" + str(i))
                elt.setAttribute("format", "ixt2:numdotdecimal")
                elt.setAttribute("decimals", "0")
                elt.setAttribute("unitRef", "pure")
                elt.appendChild(self.doc.createTextNode(str(val[i])))

                self.hidden.appendChild(elt)

        report.get("average-employees").use(add_avg_employee_counts)

        directors = business.get("directors")
        if directors:
            for i in range(0, len(directors)):
                nm = "uk-bus:NameEntityOfficer"
                self.add_nn(self.hidden, nm, "officer-{0}".format(i + 1),
                            directors[i])

        def signer(val):
            for i in range(0, len(directors)):
                if val == directors[i]:
                    self.add_nn(self.hidden,
                                "uk-core:DirectorSigningFinancialStatements",
                                "officer-" + str(i + 1), "")

        report.get("signing-director").use(signer)

        business.get("contact").get("name").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:NameContactDepartmentOrPerson",
                                    "country-0", val)
        )

        def add_address(val):
            for i in range(0, 2):
                if len(val) > (i):
                    nm = "uk-bus:AddressLine{0}".format(i+1)
                    self.add_nn(self.hidden, nm, "country-0", val[i])
                
        business.get("contact").get("address").use(
            lambda val: add_address(val)
        )

        business.get("contact").get("location").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:PrincipalLocation-CityOrTown",
                                    "country-0", val)
        )

        business.get("contact").get("county").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:CountyRegion",
                                    "country-0", val)
        )

        business.get("contact").get("postcode").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:PostalCodeZip",
                                    "country-0", val)
        )

        def add_phone(val):
            val.get("country").use(
                lambda val:
                self.add_nn(self.hidden, "uk-bus:CountryCode",
                            "phone-0", val)
            )

            val.get("area").use(
                lambda val:
                self.add_nn(self.hidden, "uk-bus:AreaCode",
                            "phone-0", val)
            )

            val.get("number").use(
                lambda val:
                self.add_nn(self.hidden, "uk-bus:LocalNumber",
                            "phone-0", val)
            )

        business.get("contact").get("phone").use(
            lambda val: add_phone(val)
        )

        business.get("website").get("url").use(
            lambda val: self.add_nn(self.hidden,
                               "uk-bus:WebsiteMainPageURL",
                               "web-0", val)
        )

        business.get("website").get("description").use(
            lambda val: self.add_nn(self.hidden,
                               "uk-bus:DescriptionOrOtherInformationOnWebsite",
                               "web-0", val)
        )

    @staticmethod
    def get_element(id, cfg, session, tx):

        elt_defs = cfg.get("elements")

        for elt_def in elt_defs:

            if elt_def.get("id") == id:
                return BasicElement.load(elt_def, cfg, session, tx)

        raise RuntimeError("Could not find element '%s'" % id)

