
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
        return

    def to_ixbrl_elt(self, par, taxonomy):

        doc = par.doc

        div = doc.createElement("div")
        div.setAttribute("class", "title page")

        def add_company_name(fact):
            div2 = doc.createElement("h1")
            div2.setAttribute("class", "heading")
            fact.append(doc, div2)
            div.appendChild(div2)

        taxonomy.get_metadata(self.data, "company-name").use(add_company_name)
        
        def add_report_title(fact):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            fact.append(doc, div2)
            div.appendChild(div2)

        taxonomy.get_metadata(self.data, "report-title").use(add_report_title)

        def add_company_number(fact):
            div2 = par.doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Registered number: "))
            fact.append(doc, div2)
            div.appendChild(div2)

        taxonomy.get_metadata(self.data, "company-number").use(
            add_company_number
        )

        div2 = doc.createElement("div")
        div.appendChild(div2)
        div2.setAttribute("class", "information")
        div2.appendChild(par.doc.createTextNode("For the period: "))
        taxonomy.get_metadata(self.data, "period-start").use(
            lambda fact: fact.append(doc, div2)
        )
        div2.appendChild(par.doc.createTextNode(" to "))
        taxonomy.get_metadata(self.data, "period-end").use(
            lambda fact: fact.append(doc, div2)
        )

        def add_report_date(fact):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Date: "))
            fact.append(doc, div2)
            div.appendChild(div2)

        taxonomy.get_metadata(self.data, "report-date").use(
            add_report_date
        )

        div2 = doc.createElement("div")
        div.appendChild(div2)
        div2.setAttribute("class", "information")
        div2.appendChild(par.doc.createTextNode("Directors: "))

        meta = taxonomy.get_all_metadata(self.data, "officer")

        for i in range(0, len(meta)):
            if i > 0:
                div2.appendChild(par.doc.createTextNode(", "))
            meta[i].append(doc, div2)

        div2.appendChild(par.doc.createTextNode("."))

        sig = par.doc.createElement("div")
        sig.setAttribute("class", "signature")
        div.appendChild(sig)

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Approved by the board of directors and authorised for publication on "))

        taxonomy.get_metadata(self.data, "authorised-date").use(
            lambda fact: fact.append(doc, p)
        )

        p.appendChild(par.doc.createTextNode("."))
        sig.appendChild(p)

        p = par.doc.createElement("p")

        p.appendChild(par.doc.createTextNode("Signed on behalf of the directors by "))

        taxonomy.get_metadata(self.data, "signing-officer").use(
            lambda fact: fact.append(doc, p)
        )

        p.appendChild(par.doc.createTextNode(
            self.data.get_config("metadata.report.signed-by")
        ))

        p.appendChild(par.doc.createTextNode("."))

        sig.appendChild(p)

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
