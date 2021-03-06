
import json
import uuid
import os
import getpass
import socket
import sys
from datetime import datetime, date

# Configuration object, loads configuration from a JSON file, and then
# supports path navigate with config.get("part1.part2.part3")
class Config(dict):
    def __init__(self, value=None):
        if value == None:
            value = {}
        super().__init__(value)
    @staticmethod
    def load(file="config.json"):
        val = json.loads(open(file).read())
        c = Config(val)
        c.file = file
        return c
    @staticmethod
    def makevalue(val):
        if val == None:
            return NoneValue()
        if isinstance(val, str):
            return StringValue(val)
        if isinstance(val, list):
            return ListValue([Config.makevalue(v) for v in val])
        if isinstance(val, bool):
            return BoolValue(val)
        if isinstance(val, int):
            return IntValue(val)
        if isinstance(val, dict):
            return Config(val)
        raise RuntimeError("Can't help with type {0}".format(type(val)))
    def get(self, key, deflt=None):
        if "." not in key:
            if key in self:
                nav = self[key]
            else:
                nav = deflt
        else:
            keys = key.split(".")
            nav = self
            for key in keys:
                if key in nav:
                    nav = nav[key]
                else:
                    return Config.makevalue(deflt)
        return Config.makevalue(nav)
    def get_date(self, key, dflt=None):
        val = self.get(key, dflt)
        return DateValue.fromisoformat(val)
    def use(self, fn):
        return fn(self)

    def set(self, key, value):
        cfg = self.config
        keys = key.split(".")
        for v in keys[:-1]:
            cfg = cfg[v]
        cfg[keys[-1]] = value
    # Write back to file
    def write(self):
        with open(self.file, "w") as config_file:
            config_file.write(json.dumps(self.config, indent=4))

class StringValue(str):
    def __new__(cls, value):
        return str.__new__(cls, value)
    def use(self, fn):
        return fn(self)

class DateValue(date):
    def __new__(cls, y, m, d):
        return date.__new__(cls, y, m, d)
    @staticmethod
    def fromisoformat(s):
        d = date.fromisoformat(s)
        return DateValue(d.year, d.month, d.day)
    def use(self, fn):
        return fn(self)

class IntValue(int):
    def __new__(cls, value):
        return int.__new__(cls, value)
    def use(self, fn):
        return fn(self)

class BoolValue(int):
    def __new__(cls, value):
        return int.__new__(cls, value)
    def use(self, fn):
        return fn(bool(self))
    def __str__(self):
        return str(bool(self))
    def __bool__(self):
        return self != 0

class ListValue(list):
    def __new__(cls, value):
        return list.__new__(cls, value)
    def use(self, fn):
        return fn(self)

class NoneValue:
    def __init__(self):
        pass
    def use(self, fn):
        return NoneValue()
    def get(self, key, deflt=None):
        return Config.makevalue(deflt)
    def __bool__(self):
        return False

# Initialise configuration file with some (mainly) static values.  Also,
# collate personal information for the Fraud API.
def initialise_config(config_file):

    # This gets hold of the MAC address, which the uuid module knows.
    # FIXME: Hacky.
    try:
        mac = uuid.getnode()
        mac = [
            '{:02x}'.format((mac >> ele) & 0xff)
            for ele in range(0,8*6,8)
        ][::-1]
        mac = ':'.join(mac)
    except:
        # Fallback.
        mac = '00:00:00:00:00:00'

    config = {
        "accounts": {
	    "file": "accounts.gnucash"
        }
    }

    with open(config_file, "w") as cfg_file:
        cfg_file.write(json.dumps(config, indent=4))

    sys.stderr.write("Wrote %s.\n" % config_file)

