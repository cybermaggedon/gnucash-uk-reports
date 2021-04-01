
from . report import TextReporter
from . ixbrl import IxbrlReporter
from . worksheet import get_worksheet
from . period import Period

from datetime import datetime
from xml.dom.minidom import getDOMImplementation
from xml.dom import XHTML_NAMESPACE
import base64
import json

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

class Element:

    def __init__(self, metadata):
        self.metadata = metadata

    @staticmethod
    def load(elt_def, cfg, session):

        kind = elt_def.get("kind")

        if kind == "composite":
            return Composite.load(elt_def, cfg, session)

        if kind == "title":
            return Title.load(elt_def, cfg)

        if kind == "worksheet":
            return WorksheetElement.load(elt_def, cfg, session)

        if kind == "notes":
            return NotesElement.load(elt_def, cfg)

        raise RuntimeError("Don't know element kind '%s'" % kind)

    def add_style(self, elt):

        doc = self.doc
        
        style = doc.createElement("style")
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
    padding-top: 4rem;
    padding-left: 4rem;
  }

  DIV.title.page DIV.subheading {
    padding-left: 4rem;
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

        self.create_contexts()

        self.create_metadata()

        currency = self.metadata.get("report").get("currency")
        unit = doc.createElement("xbrli:unit")
        unit.setAttribute("id", currency)
        measure = doc.createElement("xbrli:measure")
        measure.appendChild(doc.createTextNode("iso4217:" + currency))
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

#        out.write(doc.toprettyxml())
        out.write(doc.toxml())

    def create_contexts(self):

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

        # report periods, period<n>
        for i in range(0, len(self.periods)):
            self.resources.appendChild(self.create_context("period-" + str(i), [
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

    def create_metadata(self):

        report = self.metadata.get("report")
        business = self.metadata.get("business")

        report.get("title").use(
            lambda val:
            self.add_nn(self.hidden, "uk-bus:ReportTitle", "period-0", val)
        )

        report.get_date("date").use(
            lambda val:
            self.add_date(self.hidden, "uk-bus:BusinessReportPublicationDate",
                          "report-date", val))

        report.get("periods")[0].get_date("start").use(
            lambda val:
            self.add_date(self.hidden,
                          "uk-bus:StartDateForPeriodCoveredByReport",
                          "report-date", val))

        report.get("periods")[0].get_date("end").use(
            lambda val:
            self.add_date(self.hidden,
                          "uk-bus:EndDateForPeriodCoveredByReport",
                          "report-date", val))

        self.add_nn(self.hidden, "uk-bus:NameProductionSoftware", "period-0",
               software)
        self.add_nn(self.hidden, "uk-bus:VersionProductionSoftware", "period-0",
               software_version)

        business.get("company-name").use(
            lambda val: self.add_nn(self.hidden, 
                                    "uk-bus:EntityCurrentLegalOrRegisteredName",
                                    "period-0", val)
        )

        business.get("company-number").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:UKCompaniesHouseRegisteredNumber",
                                    "period-0", val)
        )

        business.get("vat-registration").use(
            lambda val: self.add_nn(self.hidden,
                                    "uk-bus:VATRegistrationNumber",
                                    "period-0", val)
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

    def create_period(self, p):

        cperiod = self.doc.createElement("xbrli:period")

        start = self.doc.createElement("xbrli:startDate")
        start.appendChild(self.doc.createTextNode(str(p.start)))
        cperiod.appendChild(start)

        end = self.doc.createElement("xbrli:endDate")
        end.appendChild(self.doc.createTextNode(str(p.end)))
        cperiod.appendChild(end)

        return cperiod

    def create_segment_member(self, dim, value):

        seg = self.doc.createElement("xbrli:segment")

        expmem = self.doc.createElement("xbrldi:explicitMember")
        expmem.setAttribute("dimension", dim)
        expmem.appendChild(self.doc.createTextNode(value))
        seg.appendChild(expmem)

        return seg

class Composite(Element):
    def __init__(self, metadata, elts):
        super().__init__(metadata)
        self.elements = elts

    @staticmethod
    def load(elt_def, cfg, session):

        c = Composite(
            cfg.get("metadata"),
            [
                get_element(v, cfg, session)
                for v in elt_def.get("elements")
            ]
        )
        return c

    def to_text(self, out):
        out.write("\n")
        for v in self.elements:
            v.to_text(out)
            out.write("\n")

    def to_ixbrl_elt(self, par):

        elt = par.doc.createElement("div")
        elt.setAttribute("class", "composite")

        for v in self.elements:

            sub = v.to_ixbrl_elt(par)
            elt.appendChild(sub)
        
        return elt

class Title(Element):
    def __init__(self, metadata, img, type):
        super().__init__(metadata)
        self.title = metadata.get("report").get("title")
        self.date = metadata.get("report").get("date")
        self.img = img
        self.type = type
    @staticmethod
    def load(elt_def, cfg):

        e = Title(
            cfg.get("metadata"),
            elt_def.get("signature-image"),
            elt_def.get("signature-type")
        )

        return e

    def to_text(self, out):

        
        self.metadata.get("business").get("company-name").use(
            lambda val:
            out.write("{0}\n".format(val))
        )

        self.metadata.get("business").get("company-number").use(
            lambda val:
            out.write("Registered number: {0}\n".format(val))
        )

        self.metadata.get("report").get("title").use(
            lambda val:
            out.write("{0}\n".format(val))
        )

        self.metadata.get("report").get("periods")[0].use(
            lambda val:
            out.write("For the period: {0} - {1}\n".format(
                val.get("start"), val.get("end")
            ))
        )

        self.metadata.get("report").get("date").use(
            lambda val:
            out.write("Approved for publication {0}\n".format(val))
        )

    def to_ixbrl_elt(self, par):

        doc = par.doc

        div = doc.createElement("div")
        div.setAttribute("class", "title page")

        def company_name(val):
            div2 = doc.createElement("h1")
            div2.setAttribute("class", "heading")
            par.add_nn(div2,
                       "uk-bus:EntityCurrentLegalOrRegisteredName",
                       "period-0", val)
            div.appendChild(div2)

        def company_number(val):
            div2 = par.doc.createElement("div")
            div2.setAttribute("class", "subheading")
            div2.appendChild(par.doc.createTextNode("Registered number: "))
            par.add_nn(div2,
                       "uk-bus:UKCompaniesHouseRegisteredNumber",
                       "period-0", val)
            div.appendChild(div2)

        def report_title(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            par.add_nn(div2,
                       "uk-bus:ReportTitle",
                       "period-0", val)
            div.appendChild(div2)

        def report_date(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            div2.appendChild(par.doc.createTextNode("Approved for publication "))
            par.add_date(div2,
                       "uk-bus:BusinessReportPublicationDate",
                       "report-date", val)
            div.appendChild(div2)

        def report_period(p):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            div2.appendChild(par.doc.createTextNode("For the period: "))
            par.add_date(div2,
                       "uk-bus:StartDateForPeriodCoveredByReport",
                       "report-date", p.get_date("start"))
            div2.appendChild(par.doc.createTextNode(" to "))
            par.add_date(div2,
                       "uk-bus:EndDateForPeriodCoveredByReport",
                       "report-date", p.get_date("end"))
            div.appendChild(div2)

        self.metadata.get("business").get("company-name").use(company_name)
        self.metadata.get("business").get("company-number").use(company_number)
        self.metadata.get("report").get("title").use(report_title)
        self.metadata.get("report").get("periods")[0].use(report_period)
        self.metadata.get("report").get_date("date").use(report_date)




        company_name = self.metadata.get("business").get("company-name")

        sig = par.doc.createElement("div")
        sig.setAttribute("class", "signature")

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Approved by the board of directors and authorised for publication on "))

        directors = self.metadata.get("business.directors")

        def report_date(val):
            par.add_date(p, "uk-bus:BusinessReportPublicationDate",
                       "report-date", val)

        self.metadata.get("report").get_date("date").use(report_date)

        p.appendChild(par.doc.createTextNode("."))

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Signed by "))

        def signer(val):
            for i in range(0, len(directors)):
                if val == directors[i]:
                    par.add_nn(p, "uk-core:DirectorSigningFinancialStatements",
                               "officer-" + str(i + 1), "")
                    p.appendChild(par.doc.createTextNode(val))


        self.metadata.get("report").get("signing-director").use(signer)

        p.appendChild(par.doc.createTextNode("."))


        if self.img and self.type:
            img = par.doc.createElement("img")
            data = base64.b64encode(open(self.img, "rb").read()).decode("utf-8")
            img.setAttribute("src",
                             "data:{0};base64,{1}".format(self.type, data)
                             )
            sig.appendChild(img)

        div.appendChild(sig)
        
        return div

class WorksheetElement(Element):
    def __init__(self, metadata, title, worksheet):
        super().__init__(metadata)
        self.title = title
        self.worksheet = worksheet
    @staticmethod
    def load(elt_def, cfg, session):

        e = WorksheetElement(
            cfg.get("metadata"),
            elt_def.get("title"),
            get_worksheet(elt_def.get("worksheet"), cfg, session)
        )

        return e

    def to_text(self, out):

        title = "*** {0} ***\n".format(self.title)
        out.write(title)
        
        rep = TextReporter()
        rep.output(self.worksheet, out)

        out.write("\n")

    def to_ixbrl_elt(self, par):

        rep = IxbrlReporter(par)

        elt = rep.get_elt(self.worksheet)

        div = par.doc.createElement("div")
        div.setAttribute("class", "worksheet page")

        title = par.doc.createElement("h2")
        title.appendChild(par.doc.createTextNode(self.title))
        div.appendChild(title)

        div.appendChild(elt)
        
        return div

class NotesElement(Element):
    def __init__(self, metadata, notes):
        super().__init__(metadata)
        self.notes = notes

    @staticmethod
    def load(elt_def, cfg):

        e = NotesElement(
            cfg.get("metadata"),
            elt_def.get("notes")
        )

        return e

    def to_text(self, out):

        # Not putting out notes
        pass

    def get_note_elts(self, n, par):

        if n == "small-company-audit-exempt":

            val = self.metadata.get("report").get("periods")[0].get("end")
            year_end = datetime.fromisoformat(val).date()

            elt = par.doc.createElement("span")

            par.add_nn(elt, "uk-direp:StatementThatCompanyEntitledToExemptionFromAuditUnderSection477CompaniesAct2006RelatingToSmallCompanies",
                       "period-0", "")
            
            elt.appendChild(par.doc.createTextNode("For the accounting period ending "))

            par.add_date(elt, "uk-bus:EndDateForPeriodCoveredByReport",
                         "report-date", year_end)

            elt.appendChild(par.doc.createTextNode(" the company was entitled to exemption from audit under section 477 of the Companies Act 2006 relating to small companies."))

            return elt

        if n == "no-audit-required":

            elt = par.doc.createElement("span")

            par.add_nn(elt, "uk-direp:StatementThatMembersHaveNotRequiredCompanyToObtainAnAudit",
                       "period-0", "")
            

            text = "The members have not required the company to obtain an audit of its financial statements for the accounting period in accordance with section 476."
            elt.appendChild(par.doc.createTextNode(text))
            return elt

        if n == "micro-entity-provisions":

            elt = par.doc.createElement("span")
            par.add_nn(elt, "uk-direp:StatementThatAccountsHaveBeenPreparedInAccordanceWithProvisionsSmallCompaniesRegime",
                       "period-0", "")

            text = "These financial statements have been prepared in accordance with the micro-entity provisions."
            elt.appendChild(par.doc.createTextNode(text))
            return elt

        if n == "company":

            cnum = self.metadata.get("business.company-number")
            addr = self.metadata.get("business.contact.address")

            elt = par.doc.createElement("span")
            elt.appendChild(par.doc.createTextNode("The company is a private company limited by shares and is registered in England and Wales number "))
            
            par.add_nn(elt, "uk-bus:UKCompaniesHouseRegisteredNumber",
                       "period-0", cnum)

            elt.appendChild(par.doc.createTextNode(". The registered address is: "))

            for i in range(0, 3):
                if i < len(addr):
                    if i > 0:
                        elt.appendChild(par.doc.createTextNode(", "))
                    par.add_nn(elt, "uk-bus:AddressLine" + str(i+1),
                               "country-0", addr[i])

            loc = self.metadata.get("business.contact.location").use(
                lambda val: (
                    elt.appendChild(par.doc.createTextNode(", ")),
                    par.add_nn(elt, "uk-bus:PrincipalLocation-CityOrTown",
                           "country-0", val)
                )
            )

            loc = self.metadata.get("business.contact.county").use(
                lambda val: (
                    elt.appendChild(par.doc.createTextNode(", ")),
                    par.add_nn(elt, "uk-bus:CountyRegion",
                               "country-0", val)
                )
            )

            loc = self.metadata.get("business.contact.postcode").use(
                lambda val: (
                    elt.appendChild(par.doc.createTextNode(" ")),
                    par.add_nn(elt, "uk-bus:PostalCodeZip",
                               "country-0", val)
                )
            )

            elt.appendChild(par.doc.createTextNode("."))

            return elt

        if n == "directors-acknowledge":

            elt = par.doc.createElement("span")

            text = "The directors acknowledge their responsibilities for complying with the requirements of the Act withrespect to accounting records and the preparation of financial statements."

            par.add_nn(elt, "uk-direp:StatementThatDirectorsAcknowledgeTheirResponsibilitiesUnderCompaniesAct",
                       "period-0", text)

            return elt
            
        if n == "software-version":

            elt = par.doc.createElement("span")

            elt.appendChild(par.doc.createTextNode("These accounts were generated using "))
            par.add_nn(elt, "uk-bus:NameProductionSoftware",
                         "period-0", software)
            elt.appendChild(par.doc.createTextNode(" version "))
            par.add_nn(elt, "uk-bus:VersionProductionSoftware",
                         "period-0", software_version)
            elt.appendChild(par.doc.createTextNode("."))

            return elt

        if n.startswith("note:"):
            text = n[5:]
            return par.doc.createTextNode(text)
        
        raise RuntimeError("Note '%s' not known." % n)

    def to_ixbrl_elt(self, par):

        div = par.doc.createElement("div")
        div.setAttribute("class", "notes page")

        title = par.doc.createElement("h2")
        title.appendChild(par.doc.createTextNode("Notes"))
        div.appendChild(title)

        ol = par.doc.createElement("ol")
        div.appendChild(ol)

        for note in self.notes:

            li = par.doc.createElement("li")
            ol.appendChild(li)

            p = par.doc.createElement("p")
            li.appendChild(p)

            p.appendChild(self.get_note_elts(note, par))

        return div

def get_element(id, cfg, session):

    elt_defs = cfg.get("elements")

    for elt_def in elt_defs:

        if elt_def.get("id") == id:
            return Element.load(elt_def, cfg, session)

    raise RuntimeError("Could not find element '%s'" % id)

