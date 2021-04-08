
from . basicelement import BasicElement
from . fact import *

import base64

class Title(BasicElement):
    def __init__(self, img, type, data):
        super().__init__(data)
        self.title = data.get_config("metadata.report.title")
        self.date = data.get_config("metadata.report.date")
        self.img = img
        self.type = type

    @staticmethod
    def load(elt_def, data):

        e = Title(
            elt_def.get("signature-image"),
            elt_def.get("signature-type"),
            data
        )

        return e

    def to_text(self, out):

        ci = self.data.get_company_information()

        ci.get("company-name").use(
            lambda val: out.write("{0}\n".format(val))
        )

        ci.get("company-number").use(
            lambda val: out.write("Registered number: {0}\n".format(val))
        )

        ri = self.data.get_report_information()

        ri.get("report-title").use(
            lambda val: out.write("{0}\n".format(val))
        )

        start = ri.get("period-start")
        end = ri.get("period-start")
        if start and end:
            out.write("For the period: {0} - {1}\n".format(start, end))

        ri.get("report-date").use(
            lambda val: out.write("Approved for publication {0}\n".format(val))
        )

    def to_ixbrl_elt(self, par):

        doc = par.doc

        div = doc.createElement("div")
        div.setAttribute("class", "title page")

        report = self.data.get_config("metadata.report")
        business = self.data.get_config("metadata.business")
        date = report.get_date("date")

        report_date_cdef = ContextDefinition()
        report_date_cdef.set_instant(date)
        report_date_context = self.taxonomy.create_context(report_date_cdef)

        report_period_cdef = ContextDefinition()
        report_period_cdef.set_period(
            report.get("periods")[0].get_date("start"),
            report.get("periods")[0].get_date("end")
        )
        report_period_context = self.taxonomy.create_context(report_period_cdef)

        
        
        def company_name(val):
            div2 = doc.createElement("h1")
            div2.setAttribute("class", "heading")

            fact = report_period_context.create_string_fact("company-name", val)
            fact.append(doc, div2)
            div.appendChild(div2)

        def report_title(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            fact = report_period_context.create_string_fact("report-title", val)
            fact.append(doc, div2)
            div.appendChild(div2)

        def company_number(val):
            div2 = par.doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Registered number: "))
            fact = report_period_context.create_string_fact("company-number",
                                                            val)
            fact.append(doc, div2)
            div.appendChild(div2)

        def report_date(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Date: "))
            fact = report_date_context.create_date_fact("report-date", val)
            fact.append(doc, div2)
            div.appendChild(div2)

        def report_period(p):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("For the period: "))
            fact = report_date_context.create_date_fact("period-start",
                                                          p.get_date("start"))
            fact.append(doc, div2)
            div2.appendChild(par.doc.createTextNode(" to "))
            fact = report_date_context.create_date_fact("period-end",
                                                          p.get_date("end"))
            fact.append(doc, div2)
            div.appendChild(div2)

        self.data.get_config("metadata.business.company-name").use(company_name)
        self.data.get_config("metadata.report.title").use(report_title)
        self.data.get_config("metadata.business.company-number").use(company_number)
        self.data.get_config("metadata.report.periods")[0].use(report_period)
        self.data.get_config_date("metadata.report.date").use(report_date)

        # Directors
        div2 = doc.createElement("div")
        div.appendChild(div2)
        div2.setAttribute("class", "information")
        div2.appendChild(par.doc.createTextNode("Directors: "))

        directors = self.data.get_config("metadata.business.directors")

        for i in range(0, len(directors)):

            if i > 0:
                div2.appendChild(par.doc.createTextNode(", "))

            cdef = ContextDefinition()
            cdef.set_period(
                report.get("periods")[0].get_date("start"),
                report.get("periods")[0].get_date("end")
            )
            cdef.lookup_segment("director", "director" + str(i + 1),
                                self.taxonomy)
            context = self.taxonomy.create_context(cdef)
        
            fact = context.create_string_fact("director", directors[i])
            fact.append(par.doc, div2)

        sig = par.doc.createElement("div")
        sig.setAttribute("class", "signature")

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Approved by the board of directors and authorised for publication on "))

        def report_date(val):
            fact = report_date_context.create_date_fact("issue-date",
                                                        val)
            fact.append(par.doc, p)

        self.data.get_config_date("metadata.report.date").use(report_date)

        p.appendChild(par.doc.createTextNode("."))

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Signed on behalf of the directors by "))

        def signer(val):
            for i in range(0, len(directors)):
                if val == directors[i]:
                    fact = context.create_string_fact("signer", "")
                    fact.append(par.doc, p)
                    p.appendChild(par.doc.createTextNode(val))

        self.data.get_config("metadata.report.signing-director").use(signer)

        p.appendChild(par.doc.createTextNode("."))


        if self.img and self.type:
            img = par.doc.createElement("img")
            img.setAttribute("alt", "Director's signature")
            data = base64.b64encode(open(self.img, "rb").read()).decode("utf-8")
            img.setAttribute("src",
                             "data:{0};base64,{1}".format(self.type, data)
                             )
            sig.appendChild(img)

        div.appendChild(sig)
        
        return div
