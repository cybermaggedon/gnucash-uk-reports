
from . basicelement import BasicElement

import base64

class Title(BasicElement):
    def __init__(self, metadata, img, type, tx):
        super().__init__(metadata, tx)
        self.title = metadata.get("report").get("title")
        self.date = metadata.get("report").get("date")
        self.img = img
        self.type = type
    @staticmethod
    def load(elt_def, cfg, tx):

        e = Title(
            cfg.get("metadata"),
            elt_def.get("signature-image"),
            elt_def.get("signature-type"),
            tx
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

        def report_title(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            par.add_nn(div2,
                       "uk-bus:ReportTitle",
                       "period-0", val)
            div.appendChild(div2)

        def company_number(val):
            div2 = par.doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Registered number: "))
            par.add_nn(div2,
                       "uk-bus:UKCompaniesHouseRegisteredNumber",
                       "period-0", val)
            div.appendChild(div2)

        def report_date(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Date: "))
            par.add_date(div2,
                       "uk-bus:BusinessReportPublicationDate",
                       "report-date", val)
            div.appendChild(div2)

        def report_period(p):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "information")
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
        self.metadata.get("report").get("title").use(report_title)
        self.metadata.get("business").get("company-number").use(company_number)
        self.metadata.get("report").get("periods")[0].use(report_period)
        self.metadata.get("report").get_date("date").use(report_date)

        directors = self.metadata.get("business.directors")
        company_name = self.metadata.get("business").get("company-name")

        div2 = doc.createElement("div")
        div.appendChild(div2)
        div2.setAttribute("class", "information")
        div2.appendChild(par.doc.createTextNode("Directors: "))
        for i in range(0, len(directors)):
            if i > 0:
                div2.appendChild(par.doc.createTextNode(", "))
            par.add_nn(div2, "uk-bus:NameEntityOfficer",
                       "officer-{0}".format(i + 1),
                       directors[i])

        sig = par.doc.createElement("div")
        sig.setAttribute("class", "signature")

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Approved by the board of directors and authorised for publication on "))


        def report_date(val):
            par.add_date(p, "uk-core:DateAuthorisationFinancialStatementsForIssue",
                        "report-date", val)

        self.metadata.get("report").get_date("date").use(report_date)

        p.appendChild(par.doc.createTextNode("."))

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Signed on behalf of the directors by "))

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
            img.setAttribute("alt", "Director's signature")
            data = base64.b64encode(open(self.img, "rb").read()).decode("utf-8")
            img.setAttribute("src",
                             "data:{0};base64,{1}".format(self.type, data)
                             )
            sig.appendChild(img)

        div.appendChild(sig)
        
        return div
