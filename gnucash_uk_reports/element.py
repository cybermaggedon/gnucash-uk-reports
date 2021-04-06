
from . worksheet import get_worksheet
from . worksheetelement import WorksheetElement
from . period import Period
from . composite import Composite

class Element:

    @staticmethod
    def load(elt_def, cfg, session, tx):

        kind = elt_def.get("kind")

        if kind == "composite":
            return Composite.load(elt_def, cfg, session, tx)

        if kind == "title":
            return Title.load(elt_def, cfg)

        if kind == "worksheet":
            return WorksheetElement.load(elt_def, cfg, session, tx)

        if kind == "notes":
            return NotesElement.load(elt_def, cfg, tx)

        if kind == "ct600":
            from . ct600 import CT600
            return CT600.load(elt_def, cfg, session, tx)

        raise RuntimeError("Don't know element kind '%s'" % kind)
        
def get_element(id, cfg, session, tx):

    elt_defs = cfg.get("elements")

    for elt_def in elt_defs:

        if elt_def.get("id") == id:
            return Element.load(elt_def, cfg, session, tx)

    raise RuntimeError("Could not find element '%s'" % id)

