
from . period import Period
from . basicelement import BasicElement
from . fact import *
from . worksheet import get_worksheet

from xml.dom.minidom import getDOMImplementation
from xml.dom import XHTML_NAMESPACE

from datetime import datetime, date
import json

software = "gnucash-uk-reports"
software_version = "0.0.1"

class Box:
    def __init__(self, number, description, value, tag=None):
        self.number = number
        self.description = description
        self.value = value
        if tag == None:
            self.tag = {}
        else:
            self.tag = tag

business_type_name = {
    "company": "ct-comp:Company"
}

business_type = {
    "company": "Company"
}

class FactTable(BasicElement):

    def __init__(self, metadata, elts, session, cfg, tx):
        super().__init__(metadata, tx)
        self.elements = elts
        self.session = session
        self.cfg = cfg

    @staticmethod
    def load(elt_def, cfg, session, tx):

        c = FactTable(
            cfg.get("metadata"),
            elt_def.get("facts"),
            session,
            cfg,
            tx
        )
        return c

    def add_style(self, elt):

        doc = self.doc
        
        style = doc.createElement("style")
        style.setAttribute("type", "text/css")
        elt.appendChild(style)
            
        style_text = """

BODY {
  background-color: #d0f8f8;
}

.hidden {
  display: none;
}

.data {
  display: flex;
  flex-direction: row;
  margin: 4px;
}

.data DIV {
  padding: 0.5rem;
}

.data .number {
  width: 2em;
  text-align: center;
  color: white;
  background-color: #30a090;
  border: 2px solid #004030;
  font-weight: bold;
  padding-left: 1rem;
  padding-right: 1rem;
}

.data .description {
  width: 25em;
}

.data .value {
  border: 2px solid black;
  background-color: white;
}

.data .value.false {
  color: #a0a0a0;
}

        """

        style.appendChild(doc.createTextNode(style_text))

    def get_context(self, id):

        period = Period.load(self.metadata.get("report.periods")[0])

        cdef = ContextDefinition()

        td = self.taxonomy.get_time_dimension(id)

        if td == "instant":
            cdef.set_instant(period.end)
        else:
            cdef.set_period(period.start, period.end)
#        cdef.add_segments(id, self.taxonomy)
        cdef.add_segment("ct-comp:BusinessTypeDimension",
                         "ct-comp:Company")

        context = self.taxonomy.create_context(cdef)

        return context

    def to_ixbrl_elt(self, par):

        div = par.doc.createElement("div")
        div.setAttribute("class", "facts document")

        title = par.doc.createElement("h2")
        title.appendChild(par.doc.createTextNode("FACTS FIXME"))
        div.appendChild(title)

        period = Period.load(self.metadata.get("report.periods")[0])

        for v in self.elements:

            if v.get("kind") == "config":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_string_fact(
                    id, self.metadata.get(v.get("key"))
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "config-date":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_date_fact(
                    id, self.metadata.get_date(v.get("key"))
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "bool":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_bool_fact(
                    id, v.get_bool("value")
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "string":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_string_fact(
                    id, v.get("value")
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "money":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_money_fact(
                    id, v.get("value")
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "number":

                id = v.get("id")
                context = self.get_context(id)
                fact = context.create_number_fact(
                    id, v.get("value")
                )

                elt = self.make_data(par, v.get("field"),
                                     v.get("description"), fact)
                div.appendChild(elt)

            if v.get("kind") == "worksheet-value":

                id = v.get("id")

                worksheet_id = v.get("worksheet")

                wsht = get_worksheet(worksheet_id, self.cfg, self.session,
                                     self.taxonomy)

                value_id = v.get("value")

                ds = wsht.get_dataset()

                # FIXME: Assumed first period.
                found = False
                for section in ds.sections:
                    if section.id == value_id:
                        fact = section.total.values[0]
                        found = True
                    if section.items:
                        for item in section.items:
                            if item.id == value_id:
                                fact = item.values[0]
                                found = True

                if found == False:
                    raise RuntimeError("Couldn't find value '%s'" % value_id)

                # New context
                context = self.get_context(id)

                fact = fact.copy()
                fact.rename(id, context, self.taxonomy)

                elt = self.make_data(par, str(v.get("field")),
                                     v.get("description"),
                                     fact)
                div.appendChild(elt)

        return div

    def make_data(self, par, field, desc, fact):

        row = par.doc.createElement("div")
        row.setAttribute("class", "data")

        num = par.doc.createElement("div")
        num.setAttribute("class", "number")
        row.appendChild(num)
        num.appendChild(par.doc.createTextNode(field))

        descelt = par.doc.createElement("div")
        descelt.setAttribute("class", "description")
        row.appendChild(descelt)
        descelt.appendChild(par.doc.createTextNode(desc + ": "))

        valelt = par.doc.createElement("div")
        valelt.setAttribute("class", "value")
        row.appendChild(valelt)
        fact.append(par.doc, valelt)

        return row

    def get_report_date_context(self):

        report_date = self.metadata.get("report.date")

        cdef = ContextDefinition()
        cdef.set_instant(report_date)
        cdef.add_segment("ct-comp:BusinessTypeDimension",
                         "ct-comp:Company")
        context = self.taxonomy.create_context(cdef)

        return context

    def create_metadata(self):

        context = self.get_report_date_context()

        context.create_string_fact("software", software).use(
            lambda x: x.append(self.doc, self.hidden)
        )

        context.create_string_fact("software-version", software_version).use(
            lambda x: x.append(self.doc, self.hidden)
        )

