
from . basicelement import BasicElement
from . basicelement import software, software_version

from datetime import datetime

class NotesElement(BasicElement):
    def __init__(self, metadata, title, notes, tx):
        super().__init__(metadata, tx)
        self.title = title
        self.notes = notes

    @staticmethod
    def load(elt_def, cfg, tx):

        e = NotesElement(
            cfg.get("metadata"),
            elt_def.get("title"),
            elt_def.get("notes"),
            tx
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

            text = "For the accounting period ending {0} the company was entitled to exemption from audit under section 477 of the Companies Act 2006 relating to small companies.".format(year_end.strftime("%d %B %Y"))

            par.add_nn(elt, "uk-direp:StatementThatCompanyEntitledToExemptionFromAuditUnderSection477CompaniesAct2006RelatingToSmallCompanies",
                       "period-0", text)

            return elt

        if n == "no-audit-required":

            elt = par.doc.createElement("span")

            par.add_nn(elt,
                       "uk-direp:StatementThatMembersHaveNotRequiredCompanyToObtainAnAudit",
                       "period-0",
                       "The members have not required the company to obtain an audit of its financial statements for the accounting period in accordance with section 476.")

            return elt

        if n == "micro-entity-provisions":

            elt = par.doc.createElement("span")
            par.add_nn(elt, "uk-direp:StatementThatAccountsHaveBeenPreparedInAccordanceWithProvisionsSmallCompaniesRegime",
                       "period-0", "These financial statements have been prepared in accordance with the micro-entity provisions.")

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
