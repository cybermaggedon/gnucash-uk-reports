
from . basicelement import BasicElement
from . basicelement import software, software_version
from . fact import *

from datetime import datetime

class NotesElement(BasicElement):
    def __init__(self, title, notes, data):
        super().__init__(data)
        self.title = title
        self.notes = notes

    @staticmethod
    def load(elt_def, data):

        e = NotesElement(
            elt_def.get("title"),
            elt_def.get("notes"),
            data
        )

        return e

    def to_text(self, out):

        # Not putting out notes
        pass

    def get_note_elts(self, n, par, taxonomy):

        period = self.data.get_report_period()
        year_end = period.end
        rpc = self.data.business_context.with_period(period)
        
        if n == "small-company-audit-exempt":

            elt = par.doc.createElement("span")

            text = "For the accounting period ending {0} the company was entitled to exemption from audit under section 477 of the Companies Act 2006 relating to small companies.".format(year_end.strftime("%d %B %Y"))

            datum = StringDatum("small-company-exempt-from-audit", text, rpc)
            fact = taxonomy.create_fact(datum)
            fact.append(par.doc, elt)

            return elt

        if n == "no-audit-required":

            elt = par.doc.createElement("span")

            text = "The members have not required the company to obtain an audit of its financial statements for the accounting period in accordance with section 476."

            datum = StringDatum("members-not-required-audit", text, rpc)
            fact = taxonomy.create_fact(datum)
            fact.append(par.doc, elt)

            return elt

        if n == "micro-entity-provisions":

            elt = par.doc.createElement("span")
            text = "These financial statements have been prepared in accordance with the micro-entity provisions."
            
            datum = StringDatum("accounts-prepared-small-company-regime", text,
                                rpc)
            fact = taxonomy.create_fact(datum)
            fact.append(par.doc, elt)

            return elt

        if n == "company":

            elt = par.doc.createElement("span")

            elt.appendChild(par.doc.createTextNode("The company is a private company limited by shares and is registered in England and Wales number "))

            taxonomy.get_metadata(self.data, "company-number").use(
                lambda fact: fact.append(par.doc, elt)
            )

            elt.appendChild(par.doc.createTextNode(". The registered address is: "))

            taxonomy.get_metadata(self.data, "contact-address1").use(
                lambda fact: fact.append(par.doc, elt)
            )

            taxonomy.get_metadata(self.data, "contact-address2").use(
                lambda fact: (
                    elt.appendChild(par.doc.createTextNode(", ")),
                    fact.append(par.doc, elt)
                )
            )

            taxonomy.get_metadata(self.data, "contact-address3").use(
                lambda fact: (
                    elt.appendChild(par.doc.createTextNode(", ")),
                    fact.append(par.doc, elt)
                )
            )

            taxonomy.get_metadata(self.data, "contact-location").use(
                lambda fact: (
                    elt.appendChild(par.doc.createTextNode(", ")),
                    fact.append(par.doc, elt)
                )
            )

            taxonomy.get_metadata(self.data, "contact-county").use(
                lambda fact: (
                    elt.appendChild(par.doc.createTextNode(", ")),
                    fact.append(par.doc, elt)
                )
            )

            taxonomy.get_metadata(self.data, "contact-postcode").use(
                lambda fact: (
                    elt.appendChild(par.doc.createTextNode(" ")),
                    fact.append(par.doc, elt)
                )
            )

            elt.appendChild(par.doc.createTextNode(".")),

            return elt

        if n == "directors-acknowledge":

            elt = par.doc.createElement("span")

            text = "The directors acknowledge their responsibilities for complying with the requirements of the Act withrespect to accounting records and the preparation of financial statements."

            datum = StringDatum("directors-duty", text, rpc)
            fact = taxonomy.create_fact(datum)
            fact.append(par.doc, elt)

            return elt
            
        if n == "software-version":

            elt = par.doc.createElement("span")

            elt.appendChild(par.doc.createTextNode("These accounts were generated using "))

            taxonomy.get_metadata(self.data, "software").use(
                lambda fact: fact.append(par.doc, elt)
            )

            elt.appendChild(par.doc.createTextNode(" version "))

            taxonomy.get_metadata(self.data, "software-version").use(
                lambda fact: fact.append(par.doc, elt)
            )

            elt.appendChild(par.doc.createTextNode("."))

            return elt

        if n.startswith("note:"):
             text = n[5:]
             return par.doc.createTextNode(text)
        
        raise RuntimeError("Note '%s' not known." % n)

    def to_ixbrl_elt(self, par, taxonomy):

        div = par.doc.createElement("div")
        div.setAttribute("class", "notes page")

        title = par.doc.createElement("h2")
        if self.title:
            title.appendChild(par.doc.createTextNode(self.title))
        else:
            title.appendChild(par.doc.createTextNode("Notes"))
        div.appendChild(title)

        ol = par.doc.createElement("ol")
        div.appendChild(ol)

        for note in self.notes:

            li = par.doc.createElement("li")
            ol.appendChild(li)

            p = par.doc.createElement("p")
            li.appendChild(p)

            p.appendChild(self.get_note_elts(note, par, taxonomy))

        return div
