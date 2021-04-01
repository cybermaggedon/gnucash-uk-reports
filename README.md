
# `gnucash-uk-reports`

## Introduction

This is a utility which allows gnucash accounts to be presented as UK-format
accounts.  Output formats are plain text, HTML and UK-taxonomy iXBRL format
are all supported outputs.  

iXBRL is XHTML with embedded XBRL tags so that the document can be viewed in
an HTML browser, but embedded tags all the underlying data to be extracted
by automated tools.  This allows the same accounts to be usable by a human, and
also by automated data extraction tools.

The iXBRL is the part of this which is UK-specific, the plain text
output is presumably usable in any accounting regime.

This can be used to automate production of account information so that you
can get an up-to-date balance sheet out of gnucash.  

In theory the iXBRL format accounts can be submitted to HRMC and
Companies House for annual filings.  This is not something I have
tried (yet).


## Status

Balance sheet and Income statement are known to be working and can be
seen in the example accounts.  Other account presentations may be possible
by modifying the configuration file.

While gnucash is used for account information, you still need to put a
considerable amount of static information in a JSON configuration file
e.g. your company details and periods on which to report.  You also
may need to tweak the account settings if your gnucash chart of
accounts deviates significantly from the UK-VAT standard template.

This is prototype code.  It works for me, it may not work for you.  Also,
I am not an accountant, so while it may work for you, there is no guarantee
that the output won't land you in a heap of trouble.

This git repo contains a set of example accounts and an example configuration
file so that you can check the code works 'out of the box'.

## Installing

There is a dependency on the `gnucash` Python module, which cannot be installed
from PyPI.  See <https://wiki.gnucash.org/wiki/Python_Bindings> for
installation.  On Linux (Debian, Ubuntu, Fedora), the Python modules are
available on package repositories.  MacOS and Windows builds of GnuCash are
reportedly not shipping with Python APIs at the moment.

```
pip3 install git+https://github.com/cybermaggedon/gnucash-uk-reports
```

## Usage

```
gnucash-uk-reports <config> <report> <format>
```

Where:
- `config` specifies a configuration file.  See
  [Configuration File](docs/config.md).
- `report` specifies a report tag.
- `format` specifies output format.  `text` outputs plain text, `ixbrl`
  outputs iXBRL (XHTML tagged with XBRL tags) and `html` outputs HTML, which
  is iXBRL with the XBRL tags removed.

To output from the sample accounts, try outputting text:

```
gnucash-uk-reports reports.json report text
```

And iXBRL:

```
gnucash-uk-reports reports.json report ixbrl > out.html
```

You should be able to view that page in a browser.

## Screenshots of output

[Screenshots](docs/screenshots.md)

## Other things to try

Having created iXBRL, you can try loading into
[Arelle](https://arelle.org/arelle/) which is an iXBRL development tool.
In Arelle, you can invoke a validation and check the output matches the
schema.

Once Arelle is installed, you can install the Workiva
[ixbrl-viewer](https://github.com/Workiva/ixbrl-viewer).  When an iXBRL
document is loaded into Arelle, the document is automatically loaded into
a browser with markup so that you can navigate the tags and discover tagged
information.  With the iXBRL viewer when you hover over tagged information,
it is highlighted, clicking opens up the metadata viewer.

