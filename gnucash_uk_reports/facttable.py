
from . period import Period
from . basicelement import BasicElement
from . fact import *
from . worksheet import get_worksheet

from xml.dom.minidom import getDOMImplementation
from xml.dom import XHTML_NAMESPACE

from datetime import datetime, date
import json

class Box:
    def __init__(self, number, description, value, tag=None):
        self.number = number
        self.description = description
        self.value = value
        if tag == None:
            self.tag = {}
        else:
            self.tag = tag

business_type_name = {
    "company": "ct-comp:Company"
}

business_type = {
    "company": "Company"
}

class FactTable(BasicElement):

    def __init__(self, metadata, elts, session, cfg, tx):
        super().__init__(metadata, tx)
        self.elements = elts
        self.session = session
        self.cfg = cfg

    @staticmethod
    def load(elt_def, cfg, session, tx):

        c = FactTable(
            cfg.get("metadata"),
            elt_def.get("facts"),
            session,
            cfg,
            tx
        )
        return c

    def add_style(self, elt):

        doc = self.doc
        
        style = doc.createElement("style")
        style.setAttribute("type", "text/css")
        elt.appendChild(style)
            
        style_text = """

BODY {
  background-color: #d0f8f8;
}

.hidden {
  display: none;
}

.data {
  display: flex;
  flex-direction: row;
  margin: 4px;
}

.data DIV {
  padding: 0.5rem;
}

.data .number {
  width: 2em;
  text-align: center;
  color: white;
  background-color: #30a090;
  border: 2px solid #004030;
  font-weight: bold;
  padding-left: 1rem;
  padding-right: 1rem;
}

.data .description {
  width: 14em;
}

.data .value {
  border: 2px solid black;
  background-color: white;
}

.data .value.false {
  color: #a0a0a0;
}

        """

        style.appendChild(doc.createTextNode(style_text))

    def ASDto_ixbrl(self, out):

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

        def add_title(val):
            t = doc.createElement("title");
            t.appendChild(doc.createTextNode(val));
            head.appendChild(t)

        add_title("FIXME: Facts")

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

#        self.create_contexts()

        self.create_metadata()

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
       
        ct_schema = "http://www.hmrc.gov.uk/schemas/ct/comp/2020-04-01/ct-comp-2020.xsd"
        schema = doc.createElement("link:schemaRef")
        schema.setAttribute("xlink:type", "simple")
        schema.setAttribute("xlink:href", ct_schema)
        schema.appendChild(doc.createTextNode(""))
        refs.appendChild(schema)

        elt = self.to_ixbrl_elt(self)
        body.appendChild(elt)

        out.write(doc.toprettyxml())
#        out.write(doc.toxml())

    def get_context(self, id):

        period = Period.load(self.metadata.get("report.periods")[0])

        cdef = ContextDefinition()
        cdef.set_instant(period.end)
        cdef.add_segments(id, self.taxonomy)

        context = self.taxonomy.get_context(cdef)

        return context

    def to_ixbrl_elt(self, par):

        div = par.doc.createElement("div")
        div.setAttribute("class", "facts document")

        title = par.doc.createElement("h2")
        title.appendChild(par.doc.createTextNode("FACTS FIXME"))
        div.appendChild(title)

        period = Period.load(self.metadata.get("report.periods")[0])

        for v in self.elements:

            if v.get("kind") == "config":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_string_fact(
                    id, self.metadata.get(v.get("key"))
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "config-date":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_date_fact(
                    id, self.metadata.get_date(v.get("key"))
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "bool":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_bool_fact(
                    id, v.get_bool("value")
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "worksheet-value":

                worksheet_id = v.get("worksheet")

                wsht = get_worksheet(worksheet_id, self.cfg, self.session,
                                     self.taxonomy)

                value_id = v.get("value")

                ds = wsht.get_dataset()

                # FIXME: Assumed first period.
                found = False
                for section in ds.sections:
                    if section.id == value_id:
                        if section.total == None:
                            raise RuntimeError("BUNCHES")
                        fact = section.total.values[0]
                        found = True

                if found == False:
                    raise RuntimeError("Couldn't find value '%s'" % value_id)

                elt = self.make_data(par, str(v.get("field")),
                                     v.get("description"),
                                     fact)
                div.appendChild(elt)

        return div

#        for d in report_data:

    def make_data(self, par, field, desc, fact):

        row = par.doc.createElement("div")
        row.setAttribute("class", "data")

        num = par.doc.createElement("div")
        num.setAttribute("class", "number")
        row.appendChild(num)
        num.appendChild(par.doc.createTextNode(field))

        descelt = par.doc.createElement("div")
        descelt.setAttribute("class", "description")
        row.appendChild(descelt)
        descelt.appendChild(par.doc.createTextNode(desc + ": "))

        valelt = par.doc.createElement("div")
        valelt.setAttribute("class", "value")
        row.appendChild(valelt)
        fact.append(par.doc, valelt)

        return row

    def create_metadata(self):

        report = self.metadata.get("report")
        business = self.metadata.get("business")

# report_data = [

#     Box(1, "Company Name",
#         lambda x: x.metadata.get("business.company-name"),
#         tag={
#             "tag": "ct-comp:CompanyName"
#         }
#     ),

#     Box(2, "Company Number",
#         lambda x: x.metadata.get("business.company-number")),
    
#     Box(3, "Tax reference",
#         lambda x: x.metadata.get("tax.utr"), {
#             "tag": "ct-comp:TaxReference"
#         }),

#     Box(4, "Type of company", FactTable.get_company_type),

#     Box(5, "NI trading activity",
#         lambda x: x.metadata.get_bool("tax.ni.trading"),
#         tag={
#             "tag": "ct-comp:NITradingActivity"
#         }),

#     Box(6, "NI SME", lambda x: x.metadata.get_bool("tax.ni.sme"),
#         {
#             "tag": "ct-comp:NISmallOrMediumEnterprise"
#         }),

#     Box(7, "NI Employer", lambda x: x.metadata.get_bool("tax.ni.employer"),
#         {
#             "tag": "ct-comp:NIEmployer"
#         }),

#     Box(8, "NI employer and SME with non-SME partnership profits",
#         lambda x: x.metadata.get_bool("tax.ni.employer-and-sme-with-non-sme-partnership-profits", False),
#         {
#             "tag": "ct-comp:NIEmployerAndSMEWithNon-SMEPartnershipProfits"
#         }),

#     Box(8, "NI SME and not an NI employer with SME partnership profits",
#         lambda x: x.metadata.get_bool("tax.ni.sme-and-not-an-ni-employer-with-sme-partnership-profits", False),
#         {
#             "tag": "ct-comp:NISMEAndNotAnNIEmployerWithSMEPartnershipProfits"
#         }),

#     Box(8, "SME and NI employer with excluded trade with back office election",
#         lambda x: x.metadata.get_bool("tax.ni.sme-and-ni-employer-with-excluded-trade-with-back-office-election", False),
#         {
#             "tag": "ct-comp:SMEAndNIEmployerWithExcludedTradeWithBackOfficeElection"
#         }),

#     Box(8, "NI pre commencement intangibles",
#         lambda x: x.metadata.get_bool("tax.ni.pre-commencement-intangibles", False),
#         {
#             "tag": "ct-comp:NIPreCommencementIntangibles"
#         }),

#     Box(8, "SME NI large company rules election",
#         lambda x: x.metadata.get_bool("tax.ni.sme-large-company-rules-election", False),
#         {
#             "tag": "ct-comp:SMENILargeCompanyRulesElection"
#         }),

#     Box(8, "Northern Ireland profits included",
#         lambda x: x.metadata.get_bool("tax.ni.profits-included", False),
#         {
#             "tag": "ct-comp:NorthernIrelandProfitsIncluded"
#         }),

#     Box(8, "Northern Ireland corporation tax included",
#         lambda x: x.metadata.get_bool("tax.ni.corporation-tax-included", False),
#         {
#             "tag": "ct-comp:NorthernIrelandCorporationTaxIncluded"
#         }),

#     Box(8, "Northern Ireland corporation tax included",
#         lambda x: x.metadata.get_bool("tax.ni.corporation-tax-included", False),
#         {
#             "tag": "ct-comp:NorthernIrelandCorporationTaxIncluded"
#         }),

#     Box(8, "NI trading losses used against rest of UK/mainstream profits",
#         lambda x: x.metadata.get_bool("tax.ni.group-relief-ni-trading-losses-used-against-rest-of-uk-mainstream-profits", False),
#         {
#             "tag": "ct-comp:GroupReliefNITradingLossesUsedAgainstRestOfUKMainstreamProfits"
#         }),

#     Box(8, "NI trading losses used against NI trading profits",
#         lambda x: x.metadata.get_bool("tax.ni.group-relief-trading-losses-used-against-ni-trading-profits", False),
#         {
#             "tag": "ct-comp:GroupReliefNITradingLossesUsedAgainstRestOfUKMainstreamProfits"
#         }),

#     Box(8, "Rest of UK/mainstream losses used against NI trading profits",
#         lambda x: x.metadata.get_bool("tax.ni.group-relief-rest-of-uk-mainstream-losses-used-against-ni-trading-profits", False),
#         {
#             "tag": "ct-comp:GroupReliefRestOfUKMainstreamLossesUsedAgainstNITradingProfits"
#         }),


# #    Box(7, "NI employer", "get_ni_employer"),
# #    Box(8, "Special circumstances", "get_special_circumstances"),
#     Box(30, "Period from", FactTable.get_period_from, tag={"tag": "ct-comp:StartOfPeriodCoveredByReturn"}),
#     Box(31, "Period to", "get_period_to", tag={"tag": "ct-comp:EndOfPeriodCoveredByReturn"}),
#     Box("-", "Start of period covered by return", "get_period_from",
#         tag={"tag": "ct-comp:StartOfPeriodCoveredByReturn"}),
#     Box("-", "End of period covered by return", "get_period_to",
#         tag={"tag": "ct-comp:EndOfPeriodCoveredByReturn"}),
#     Box("-", "Company is a partner in a firm", "get_partner_in_a_firm",
#         tag={"tag": "ct-comp:CompanyIsAPartnerInAFirm"}),
#     Box("-", "Software", "get_software",
#         tag={"tag": "ct-comp:ct-comp:NameOfProductionSoftware"}),
#     Box("-", "Version", "get_software_version",
#         tag={"tag": "ct-comp:ct-comp:VersionOfProductionSoftware"}),
# ]

