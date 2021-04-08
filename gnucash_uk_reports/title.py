
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
            lambda val: out.write("{0}\n".format(val.value))
        )

        ci.get("company-number").use(
            lambda val: out.write("Registered number: {0}\n".format(val.value))
        )

        ri = self.data.get_report_information()

        ri.get("report-title").use(
            lambda val: out.write("{0}\n".format(val.value))
        )

        start = ri.get("period-start")
        end = ri.get("period-start")
        if start and end:
            out.write("For the period: {0} - {1}\n".format(
                start.value, end.value
            ))

        ri.get("report-date").use(
            lambda val:
            out.write("Approved for publication {0}\n".format(val.value))
        )

    def to_ixbrl_elt(self, par, taxonomy):

        doc = par.doc

        div = doc.createElement("div")
        div.setAttribute("class", "title page")

        ci = self.data.get_company_information()
        ri = self.data.get_report_information()

        def add_company_name(val):
            div2 = doc.createElement("h1")
            div2.setAttribute("class", "heading")
            fact = taxonomy.create_fact(val)
            fact.append(doc, div2)
            div.appendChild(div2)

        ci.get("company-name").use(add_company_name)
        
        def add_report_title(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "subheading")
            fact = taxonomy.create_fact(val)
            fact.append(doc, div2)
            div.appendChild(div2)

        ri.get("report-title").use(add_report_title)

        def add_company_number(val):
            div2 = par.doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Registered number: "))
            fact = taxonomy.create_fact(val)
            fact.append(doc, div2)
            div.appendChild(div2)

        ci.get("company-number").use(add_company_number)

        div2 = doc.createElement("div")
        div.appendChild(div2)
        div2.setAttribute("class", "information")
        div2.appendChild(par.doc.createTextNode("For the period: "))
        ri.get("period-start").use(
            lambda val: taxonomy.create_fact(val).append(doc, div2)
        )
        div2.appendChild(par.doc.createTextNode(" to "))
        ri.get("period-end").use(
            lambda val: taxonomy.create_fact(val).append(doc, div2)
        )

        def add_report_date(val):
            div2 = doc.createElement("div")
            div2.setAttribute("class", "information")
            div2.appendChild(par.doc.createTextNode("Date: "))
            taxonomy.create_fact(val).append(doc, div2)
            div.appendChild(div2)

        ri.get("report-date").use(add_report_date)

        div2 = doc.createElement("div")
        div.appendChild(div2)
        div2.setAttribute("class", "information")
        div2.appendChild(par.doc.createTextNode("Directors: "))

        def add_director(n):
            def fn(val):
                if n > 0:
                    div2.appendChild(par.doc.createTextNode(", "))
                taxonomy.create_fact(val).append(doc, div2)
            return fn
            
        for i in range(0, 20):

            ci.get("director" + str(i + 1)).use(add_director(i))

        div2.appendChild(par.doc.createTextNode("."))

        sig = par.doc.createElement("div")
        sig.setAttribute("class", "signature")
        div.appendChild(sig)

        p = par.doc.createElement("p")
        sig.appendChild(p)

        p.appendChild(par.doc.createTextNode("Approved by the board of directors and authorised for publication on "))

        ri.get("report-date").use(
            lambda val: taxonomy.create_fact(val).append(doc, p)
        )

        p.appendChild(par.doc.createTextNode("."))
        sig.appendChild(p)

        p = par.doc.createElement("p")

        p.appendChild(par.doc.createTextNode("Signed on behalf of the directors by "))

        def signer(val):
            fact = taxonomy.create_fact(val)
            fact.append(doc, p)

        ci.get("signed-by").use(signer)

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
