
from . basicelement import BasicElement

class Composite(BasicElement):
    def __init__(self, metadata, elts):
        super().__init__(metadata)
        self.elements = elts

    @staticmethod
    def load(elt_def, cfg, session, tx):

        c = Composite(
            cfg.get("metadata"),
            [
                BasicElement.get_element(v, cfg, session, tx)
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
