
from . format import NegativeParenFormatter
from xml.dom.minidom import getDOMImplementation
from xml.dom import XHTML_NAMESPACE
from datetime import datetime, date

class IxbrlReporter:

    def __init__(self, par=None):
        self.par = par

    def get_elt(self, worksheet):

        fmt = NegativeParenFormatter()

        def format_number(n):
            return fmt.format("{0:,.2f}", n)

        doc = self.par.doc

        def add_header(grid, periods):

            # Blank header cell
            blank = doc.createElement("div")
            blank.setAttribute("class", "label")
            grid.appendChild(blank)
            blank.appendChild(doc.createTextNode(" "))

            # Header cells for period names
            for period in periods:

                elt = doc.createElement("div")
                grid.appendChild(elt)
                elt.setAttribute("class", "period periodname")
                elt.appendChild(doc.createTextNode(period[0].name))

            # Blank header cell
            blank = doc.createElement("div")
            blank.setAttribute("class", "label")
            grid.appendChild(blank)
            blank.appendChild(doc.createTextNode(" "))

            # Header cells for period names
            for period in periods:

                elt = doc.createElement("div")
                grid.appendChild(elt)
                elt.setAttribute("class", "period currency")
                elt.appendChild(doc.createTextNode("£"))

        def maybe_tag(value, detail, pid):

            tag = detail.get("tags").get("tag")

            if tag:

                elt = doc.createElement("ix:nonFraction")
                elt.setAttribute("name", tag)

                if "context" in detail["tags"]:
                    ctxt = detail["tags"]["context"].format(pid)
                else:
                    ctxt = "period-end-{0}".format(pid)
                elt.setAttribute("contextRef", ctxt)
                elt.setAttribute("format", "ixt2:numdotdecimal")
                elt.setAttribute("unitRef", "GBP")
                elt.setAttribute("decimals", "2")

                if abs(value) < 0.001:
                    sign = False
                else:
                    if value < 0:
                        sign = True
                    else:
                        sign = False

                    if "sign" in detail["tags"]:
                        if detail["tags"]["sign"] == "reversed":
                            sign = not sign

                if sign:
                    elt.setAttribute("sign", "-")

                # Sign and negativity of value is not the same.

                if value < 0:

                    txt = doc.createTextNode("{0:,.2f}".format(-value))
                    elt.appendChild(txt)

                    span = doc.createElement("span")
                    span.appendChild(doc.createTextNode("( "))
                    span.appendChild(elt)
                    span.appendChild(doc.createTextNode(" )"))
                    return span

                txt = doc.createTextNode("{0:,.2f}".format(value))
                elt.appendChild(txt)

                return elt

            # Sign and negativity of value is not the same.
            if value < 0:

                txt = doc.createTextNode("{0:,.2f}".format(-value))

                span = doc.createElement("span")
                span.appendChild(doc.createTextNode("( "))
                span.appendChild(txt)
                span.appendChild(doc.createTextNode(" )"))
                return span

            txt = doc.createTextNode("{0:,.2f}".format(value))
            return txt

        def add_nil_section(grid, detail, periods):

            div = doc.createElement("div")
            div.setAttribute("class", "label header")
            div.appendChild(doc.createTextNode(detail["header"]))
            grid.appendChild(div)

            for i in range(0, len(periods)):
                div = doc.createElement("div")
                div.setAttribute("class", "period total value nil")
                grid.appendChild(div)
                content = maybe_tag(0, detail, i)
                div.appendChild(content)

        def add_total_section(grid, detail, periods):

            div = doc.createElement("div")
            div.setAttribute("class", "label header total")
            div.appendChild(doc.createTextNode(detail["header"]))
            grid.appendChild(div)

            for i in range(0, len(periods)):
                div = doc.createElement("div")
                grid.appendChild(div)
                value = detail["total"][i]
                if abs(value) < 0.001:
                    div.setAttribute("class", "period total value nil")
                elif value < 0:
                    div.setAttribute("class", "period total value negative")
                else:
                    div.setAttribute("class", "period total value")
                content = maybe_tag(value, detail, i)
                div.appendChild(content)

        def add_breakdown_section(grid, detail, periods):

            div = doc.createElement("div")
            div.setAttribute("class", "label breakdown header")
            div.appendChild(doc.createTextNode(detail["header"]))
            grid.appendChild(div)

            for item in detail["items"]:

                div = doc.createElement("div")
                div.setAttribute("class", "label breakdown item")
                div.appendChild(doc.createTextNode(item["description"]))
                grid.appendChild(div)

                for i in range(0, len(periods)):

                    value = item["values"][i]

                    div = doc.createElement("div")
                    if abs(value) < 0.001:
                        div.setAttribute("class", "period value nil")
                    elif value < 0:
                        div.setAttribute("class", "period value negative")
                    else:
                        div.setAttribute("class", "period value")

                    content = maybe_tag(value, item, i)

                    div.appendChild(content)
                    grid.appendChild(div)

            div = doc.createElement("div")
            div.setAttribute("class", "label breakdown total")
            grid.appendChild(div)
            div.appendChild(doc.createTextNode("Total"))

            for i in range(0, len(periods)):

                div = doc.createElement("div")

                grid.appendChild(div)

                value = detail["total"][i]

                if abs(value) < 0.001:
                    div.setAttribute("class",
                                     "period value nil breakdown total")
                elif value < 0:
                    div.setAttribute("class",
                                     "period value negative breakdown total")
                else:
                    div.setAttribute("class", "period value breakdown total")

                content = maybe_tag(value, detail, i)
                div.appendChild(content)

        def add_section(tbody, detail, periods):

            if detail["total"] == None and detail["items"] == None:

                add_nil_section(tbody, detail, periods)

            elif detail["items"] == None:

                add_total_section(tbody, detail, periods)

            else:

                add_breakdown_section(tbody, detail, periods)

        def create_report(worksheet):

            periods = worksheet.get_periods()
            sections = worksheet.get_sections()

            grid = doc.createElement("div")
            grid.setAttribute("id", worksheet.id)
            grid.setAttribute("class", "sheet")

            add_header(grid, periods)

            for section, id in sections:

                detail = worksheet.describe_section(id)

                add_section(grid, detail, periods)

            return grid

        return create_report(worksheet)


