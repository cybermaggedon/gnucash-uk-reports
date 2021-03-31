
from . period import Period
from . computation import Result
from . worksheet_model import Worksheet, SimpleValue, Breakdown, NilValue, Total

class SinglePeriodWorksheet(Worksheet):

    def __init__(self, parts, period):
        self.parts = parts
        self.period = period

    @staticmethod
    def create(cfg, report, comps, session):
        mpr = SinglePeriodWorksheet.load(cfg, report, comps)
        mpr.process(session)
        return mpr

    @staticmethod
    def load(cfg, report, comps):

        ttr = SinglePeriodWorksheet(
            [],
            Period.load(cfg.get("metadata.report.periods")[0])
        )

        ttr.id = report.get("id")
        ttr.business = cfg.get("business")
        ttr.metadata = report.get("metadata")

        for part in report.get("items"):
            ttr.parts.append(comps[part])

        return ttr

    def process(self, session):
        result = Result()

        for part in self.parts:
            part.compute(session, self.period.start, self.period.end, result)

        work_items = []

        for part in self.parts:
            work_items.append(part.get_output(result))

        self.items = work_items

    def get_periods(self):
        return [(self.period, 0)]

    def get_sections(self):
        return [(self.parts[v], v) for v in range(0, len(self.parts))]

    def describe_section(self, section):

        period = self.period

        item = self.items[section]

        if isinstance(item, Breakdown):

            detail = {
                "header": item.description,
                "total": [
                    self.items[section].value
                ]
            }

            if item.tags != None:
                detail["tags"] = item.tags

            its = []
            for i in range(0, len(item.items)):
                it = {
                    "description": item.items[i].description,
                    "values": [
                        self.items[section].items[i].value
                    ]
                }
                if item.items[i].tags != None:
                    it["tags"] = item.items[i].tags
                its.append(it)
            detail["items"] = its

            return detail

        if isinstance(item, NilValue):
            detail = {
                "header": item.description,
                "items": None,
                "total": None
            }

            if item.tags != None:
                detail["tags"] = item.tags

            return detail

        if isinstance(item, Total):
            detail = {
                "header": item.description,
                "items": None,
                "total": [item.value]
            }

            if item.tags != None:
                detail["tags"] = item.tags

            return detail
