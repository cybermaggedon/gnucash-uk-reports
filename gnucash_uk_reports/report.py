
from . format import NegativeParenFormatter
from . period import Period
from . ixbrl import IxbrlReporter
import io

class TextReporter:

    def output(self, worksheet, out):

        fmt = NegativeParenFormatter()

        def format_number(n):
            if abs(n) < 0.001:
                return "- "
            return fmt.format("{0:.2f}", n)

        periods = worksheet.get_periods()
        sections = worksheet.get_sections()

        out.write(fmt.format("{0:40}  ", ""))
        for period in periods:
            out.write(fmt.format("{0:>10} ", period[0].name + " "))

        out.write("\n")

        for section, id in sections:
            out.write("\n")

            detail = worksheet.describe_section(id)

            if detail["total"] == None and detail["items"] == None:

                out.write(fmt.format("{0:40}: ", detail["header"]))

                for period in periods:
                    out.write(fmt.format("{0:>10} ", " - "))

                out.write("\n")
                

            elif detail["items"] == None:

                out.write(fmt.format("{0:40}: ", detail["header"]))

                for i in range(0, len(periods)):

                    s = format_number(detail["total"][i])
                    out.write("{0:>10} ".format(s))

                out.write("\n")

            else:

                out.write(fmt.format("{0}:\n", detail["header"]))

                for item in detail["items"]:
                    
                    out.write(fmt.format("  {0:38}: ", item["description"]))

                    for i in range(0, len(periods)):

                        s = format_number(item["values"][i])
                        out.write(fmt.format("{0:>10} ", s))

                    out.write("\n")

                out.write(fmt.format("{0:40}: ", "Total"))

                for i in range(0, len(periods)):

                    s = format_number(detail["total"][i])
                    out.write(fmt.format("{0:>10} ", s))

                out.write("\n")


