
from . period import Period
from . computation import Result
from . worksheet_model import Worksheet, SimpleValue, Breakdown, NilValue, Total

class MultiPeriodWorksheet(Worksheet):

    def __init__(self, parts, periods):
        self.parts = parts
        self.periods = periods

    @staticmethod
    def create(cfg, report, comps, session):

        periods = []
        for pdef in cfg.get("metadata.report.periods"):
            periods.append(Period.load(pdef))

        mpr = MultiPeriodWorksheet.load(cfg, report, comps, periods)
        mpr.process(session)
        return mpr

    @staticmethod
    def load(cfg, report, comps, periods):

        mpr = MultiPeriodWorksheet([], periods)

        mpr.id = report.get("id")

        for part in report.get("items"):
            mpr.parts.append(comps[part])

        return mpr

    def process(self, session):

        all_items = []

        for period in self.periods:

            result = Result()

            for part in self.parts:
                part.compute(session, period.start, period.end, result)

            work_items = []

            for part in self.parts:
                work_items.append(part.get_output(result))

            all_items.append(work_items)

        self.items = all_items

    def get_periods(self):
        return [(self.periods[v], v) for v in range(0, len(self.periods))]

    def get_sections(self):
        return [(self.parts[v], v) for v in range(0, len(self.parts))]

    def describe_section(self, section):

        if len(self.periods) < 1:
            raise RuntimeError("Multi-period must have at least one period")

        # Need to get one occurence of the item to work out its kind.
        item = self.items[0][section]

        if isinstance(item, Breakdown):

            detail = {
                "header": item.description,
                "total": [
                    self.items[p][section].value
                    for p in range(0, len(self.periods))
                ]
            }

            if item.tags != None:
                detail["tags"] = item.tags

            its = []
            for i in range(0, len(item.items)):
                it = {
                    "description": item.items[i].description,
                    "values": [
                        self.items[p][section].items[i].value
                        for p in range(0, len(self.periods))
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
                "total": [
                    self.items[p][section].value
                    for p in range(0, len(self.periods))
                ]
            }
            if item.tags != None:
                detail["tags"] = item.tags
            return detail
