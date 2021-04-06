
from . multi_period import MultiPeriodWorksheet
from . computation import Computable
from . fact import FRS101

def get_worksheet(id, cfg, session, taxonomy=FRS101()):

    comp_defs = cfg.get("computations")

    comps = {}
    for comp_def in comp_defs:
        comp =  Computable.load(comp_def, comps, taxonomy)
        comps[comp.id] = comp

    for ws_def in cfg.get("worksheets"):

        if ws_def.get("id") == id:

            kind = ws_def.get("kind")

            if kind == "multi-period":
                return MultiPeriodWorksheet.create(cfg, ws_def, comps, session)

            raise RuntimeError("Don't know worksheet type '%s'" % kind)

    raise RuntimeError("Could not find worksheet '%s'" % id)

