
from . period import Period
from . computation import Result
from . worksheet_model import Worksheet, SimpleValue, Breakdown, NilValue, Total
from . fact import *

class MultiPeriodWorksheet(Worksheet):

    def __init__(self, inputs, periods):
        self.inputs = inputs
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

        for input in report.get("items"):
            mpr.inputs.append(comps[input])

        return mpr

    def process(self, session):

        self.outputs = {}

        for period in self.periods:

            result = Result()

            for input in self.inputs:
                input.compute(session, period.start, period.end, result)

            period_output = {}

            for input in self.inputs:
                period_output[input] = input.get_output(result)

            self.outputs[period] = period_output

    def get_dataset(self):

        ds = Dataset()
        ds.periods = [v for v in self.periods]
        ds.sections = []
        
        for input in self.inputs:

            output0 = self.outputs[self.periods[0]][input]

            if isinstance(output0, Breakdown):

                sec = Section()
                sec.id = input.id
                sec.header = input.description
                sec.total = Series("Total", [
                    self.outputs[period][input].value
                    for period in self.periods
                ])

                sec.items = [
                    Series(
                        output0.items[i].description,
                        [
                            self.outputs[period][input].items[i].value
                            for period in self.periods
                        ]
                    )
                    for i in range(0, len(output0.items))
                ]

                ds.sections.append(sec)

            elif isinstance(output0, NilValue):

                sec = Section()
                sec.id = input.id
                sec.header = input.description
                sec.items = None
                sec.total = Series("Total", [
                    self.outputs[period][input].value
                    for period in self.periods
                ])
                ds.sections.append(sec)

            elif isinstance(output0, Total):

                sec = Section()
                sec.id = input.id
                sec.header = input.description
                sec.items = None
                sec.total = Series("Total", [
                    self.outputs[period][input].value
                    for period in self.periods
                ])
                ds.sections.append(sec)

        return ds
