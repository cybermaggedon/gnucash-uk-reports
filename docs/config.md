
# Configuration

The configuration file is a JSON file, and consists of the following parts:

## `accounts`

This is where you specify the gnucash accounts filename:

```
{
    ...
    "accounts": {
	"file": "example.gnucash"
    }
    ...
}
```

## `metadata.business`

This is where you describe your business e.g.

```
{
    ...
    "metadata": {
	"business": {
	    "company-name": "Example Biz Ltd.",
	    "company-number": "012345678",
	    "vat-registration": "GB012345678",
	    "activities": "Computer security consultancy and development services",
	    "industry-sector": "m",
	    "is-dormant": false,
	    "company-formation": {
		"form": "private-limited-company",
		"country": "england-and-wales",
		"date": "2019-03-01"
	    },
	    "sic-codes": [
		"62020", "62021"
	    ],
	    "directors": [
		"A Bloggs",
		"B Smith",
		"C Jones"
	    ],
	    "contact": {
		"name": "Corporate Enquiries",
		"address": [
		    "123 Leadbarton Street",
		    "Dumpston Trading Estate"
		],
		"location": "Threapminchington",
		"county": "Minchingshire",
		"postcode": "QQ99 9ZZ",
		"email": "corporate@example.org",
		"phone": {
		    "country": "+44",
		    "area": "7900",
		    "number": "0123456"
		},
		"country": "UK"
	    },
	    "website": {
		"url": "https://example.org/corporate",
		"description": "Corporate website"
	    }
	}
	...
    }
    ...
}
```

The settings here apply to micro-entity accounts.  If you're using this 
software for a larger entity, then... Well, that's brave of you.

## `metadata.report`

This is where you add metadata regarding your report.  The report
structure itself is defined later.  Of particular note is the
`statement-date`, `date` and `periods` fields which define the timeline
aspects of the report.

```
{
    ...
    "metadata": {
        ...
	"report": {
	    "title": "Unaudited Micro-Entity Accounts",
	    "accounts-status": "audit-exempt-no-accountants-report",
	    "accounts-type": "abridged-accounts",
	    "accounting-standards": "micro-entities",
	    "statement-date": "2021-08-31",
	    "date": "2021-06-13",
	    "currency": "GBP",
	    "signing-director": "B Smith",
	    "periods": [
		{
		    "name": "2020",
		    "start": "2020-03-01",
		    "end": "2021-02-28"
		},
		{
		    "name": "2019",
		    "start": "2019-03-01",
		    "end": "2020-02-29"
		}
	    ]
	}
    }
    ...
}
```

## `computations`

This sections describes a set of report computations.  These can be
types: `group` which fetches information from gnucash accounts.
`computation` which sums information from other `group` and `computation`
elements.

### `group` type

Here's an example.  The group is called `fixed-assets`, with an appropriate
description.  A group consists of zero or more lines, each line has a list
of Gnucash accounts to access.  When the group is displayed each line is
shown with its total, and then there's a total for all the lines.

```
{
    "computations": [
        ...
	{
	    "id": "fixed-assets",
	    "kind": "group",
	    "description": "Fixed Assets",
            "hide-breakdown": false,
	    "lines": [
		{
		    "id": "tangible-assets",
		    "kind": "line",
		    "description": "Tangible Assets",
		    "tags": {
			"tag": "uk-core:PropertyPlantEquipmentIncludingRight-of-useAssets"
		    },
		    "in-year": false,
		    "accounts": [
			"Assets:Capital Equipment"
		    ]
		}
	    ],
	    "tags": {
		"tag": "uk-core:FixedAssets",
		"sign": "reversed"
	    }
	}
	...
    ]
    ...
}
```

The output might look like this:

```
Fixed Assets:
  Tangible Assets                       :    512.00
Total                                   :    512.00
```

Each line can have an iXBRL name in the `tags` element, as well as tag
information for the whole group.

In gnucash, things that cause money to go away (e.g. liabilities) are negative.
In iXBRL they are normally positive, so you can set the `sign` field to
`reversed` to turn something which is normally a Gnucash negative into an
iXBRL positive.

When examining Gnucash accounts the `group` usually looks at transactions
which are within the current period (usually an accounting year).  This is
correct for income/expense information where you are only accounting
within a period, but incorrect for balance sheet where you are accumulating
information from the origins of a company.  This is controlled with the
`in-year` attribute.  Set to `false` to examine transactions from the beginning
from time immemorial.

If the `line` list is empty i.e. there are no line items, the group
will evaluate to zero.

If you are using iXBRL output, and have line items or group item which have
no tags, no iXBRL tagging will take place for these items.  This is the
correct thing to do for data for which no iXBRL tags exist.

The `hide-breakdown` attribute causes a group to be shown as a total
without individual lines shown.

### `computation` type
The computation type sums information from other groups or computations.
e.g. we can compute net current assets by summing current assets etc.:
```
{
    "computations": [
        ...
	{
	    "id": "net-current-assets",
	    "kind": "computation",
	    "description": "Net Current Assets",
	    "tags": {
		"tag": "uk-core:NetCurrentAssetsLiabilities"
	    },
	    "inputs": [
		"current-assets",
		"prepayments-and-accrued-income",
		"creditors-within-1-year"
	    ]
	}
	...
    ]
    ...
}
```

The output is a single line e.g.

```
Net Current Assets                      :   8080.00
```

## `worksheets`

Computations don't cause any output per se.  To turn computations into
anything you need to combine them in a worksheet.  e.g. Here's a balance
sheet, which lists a set of computations in order.

The worksheet only defines what goes into the output, it doesn't describe
what is shown, or how the data is linked.  It's the `computation` elements
which describe the information flows.

Here's a balance sheet exmaple:

```
{
    "worksheets": [
        ...
	{
	    "id": "balance-sheet",
	    "kind": "multi-period",

	    "items": [
		"fixed-assets",
		"current-assets",
		"prepayments-and-accrued-income",
		"creditors-within-1-year",
		"net-current-assets",
		"total-assets-less-liabilities",
		"creditors-after-1-year",
		"provisions-for-liabilities",
		"accruals-and-deferred-income",
		"net-assets",
		"capital-and-reserves",
		"total-capital-and-reserves"
	    ]

	}
	...
    ]
    ...
}
```


## `elements`

You use elements to assemble worksheets into a report.  This is the report
included in the example `reports.json`.  If you deviate considerably from this
structure, the report may not be valid.  This produces a balance sheet
and an income statement along with some notes.

```
{
   ...
    "elements": [
	{
	    "id": "report",
	    "kind": "composite",
	    "elements": [
		"title",
		"balance-sheet",
		"profit-and-loss",
		"notes",
		"signature"
	    ]
	},

	{
	    "id": "title",
	    "kind": "title"
	},
	{
	    "id": "balance-sheet",
	    "kind": "worksheet",
	    "title": "Balance Sheet",
	    "worksheet": "balance-sheet"
	},
	{
	    "id": "profit-and-loss",
	    "kind": "worksheet",
	    "title": "Income Statement",
	    "worksheet": "profit-and-loss"
	},
	{
	    "id": "notes",
	    "kind": "notes",
	    "notes": [
		"micro-entity-provisions",
		"small-company-audit-exempt",
		"no-audit-required",
		"company",
		"directors-acknowledge",
		"software-version",
		"note:These are fictional accounts, references to real-world entities or persons is unintentional."
	    ]
	},
	{
	    "id": "signature",
	    "kind": "signature"
	}
    ]
    ...
}
```

The `notes` section auto-generates report notes with appropriate company
data and iXBRL tags. e.g. `micro-entity-provisions` outputs a note which
says: "These financial statements have been prepared in accordance with the
micro-entity provisions."  `company` outputs something like "The company is
a private company limited by shares and is registered in England and Wales
number 012345678. The registered address is: 123 Leadbarton Street, Dumpston
Trading Estate, Threapminchington, Minchingshire QQ99 9ZZ."

Custom notes can be added with the `note:` prefix followed by any text you
want in the report.


