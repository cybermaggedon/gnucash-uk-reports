
from . worksheet import get_worksheet
from . basicelement import BasicElement
from . report import TextReporter
from . ixbrl import IxbrlReporter

class WorksheetElement(BasicElement):
    def __init__(self, metadata, title, worksheet):
        super().__init__(metadata)
        self.title = title
        self.worksheet = worksheet
    @staticmethod
    def load(elt_def, cfg, session, tx):

        e = WorksheetElement(
            cfg.get("metadata"),
            elt_def.get("title"),
            get_worksheet(elt_def.get("worksheet"), cfg, session, tx)
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
