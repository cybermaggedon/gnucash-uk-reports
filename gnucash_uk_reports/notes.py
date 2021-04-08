
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

    def get_note_elts(self, n, par):

        report = self.cfg.get("metadata.report")

        report_date_context = par.get_report_date_context()
        report_period_context = par.get_report_period_context()
        
        if n == "small-company-audit-exempt":

            val = self.cfg.get("metadata.report.periods")[0].get("end")
            year_end = datetime.fromisoformat(val).date()

            elt = par.doc.createElement("span")

            text = "For the accounting period ending {0} the company was entitled to exemption from audit under section 477 of the Companies Act 2006 relating to small companies.".format(year_end.strftime("%d %B %Y"))

            fact = report_period_context.create_string_fact("small-company-exempt-from-audit", text)
            fact.append(par.doc, elt)

            return elt

        if n == "no-audit-required":

            elt = par.doc.createElement("span")

            text = "The members have not required the company to obtain an audit of its financial statements for the accounting period in accordance with section 476."

            fact = report_period_context.create_string_fact("members-not-required-audit", text)
            fact.append(par.doc, elt)

            return elt

        if n == "micro-entity-provisions":

            elt = par.doc.createElement("span")
            text = "These financial statements have been prepared in accordance with the micro-entity provisions."
            
            fact = report_period_context.create_string_fact("accounts-prepared-small-company-regime", text)
            fact.append(par.doc, elt)

            return elt

        if n == "company":

            company_number = self.cfg.get("metadata.business.company-number")
            addr = self.cfg.get("metadata.business.contact.address")

            elt = par.doc.createElement("span")
            elt.appendChild(par.doc.createTextNode("The company is a private company limited by shares and is registered in England and Wales number "))

            fact = report_period_context.create_string_fact("company-number", company_number)
            fact.append(par.doc, elt)

            elt.appendChild(par.doc.createTextNode(". The registered address is: "))

            contact_context = par.get_contact_context()
            for i in range(0, 3):
                if len(addr) > (i):
                    if i > 0:
                        elt.appendChild(par.doc.createTextNode(", "))
                    nm = "contact-address{0}".format(i+1)
                    fact = contact_context.create_string_fact(nm, addr[i])
                    fact.append(par.doc, elt)

            def location(val):
                elt.appendChild(par.doc.createTextNode(", "))
                fact = contact_context.create_string_fact(
                    "contact-location", val
                )
                fact.append(par.doc, elt)

            loc = self.cfg.get("metadata.business.contact.location").use(location)

            def county(val):
                elt.appendChild(par.doc.createTextNode(", "))
                fact = contact_context.create_string_fact(
                    "contact-county", val
                )
                fact.append(par.doc, elt)

            loc = self.cfg.get("metadata.business.contact.county").use(county)

            def postcode(val):
                elt.appendChild(par.doc.createTextNode(" "))
                fact = contact_context.create_string_fact(
                    "contact-postcode", val
                )
                fact.append(par.doc, elt)

            loc = self.cfg.get("metadata.business.contact.postcode").use(postcode)

            elt.appendChild(par.doc.createTextNode("."))

            return elt

        if n == "directors-acknowledge":

            elt = par.doc.createElement("span")

            text = "The directors acknowledge their responsibilities for complying with the requirements of the Act withrespect to accounting records and the preparation of financial statements."

            fact = report_period_context.create_string_fact("directors-duty", text)
            fact.append(par.doc, elt)

            return elt
            
        if n == "software-version":

            elt = par.doc.createElement("span")

            elt.appendChild(par.doc.createTextNode("These accounts were generated using "))


            fact = report_period_context.create_string_fact(
                "software", software
            )
            fact.append(par.doc, elt)

            elt.appendChild(par.doc.createTextNode(" version "))

            fact = report_period_context.create_string_fact(
                "software-version", software_version
            )
            fact.append(par.doc, elt)

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

            p.appendChild(self.get_note_elts(note, par))

        return div
