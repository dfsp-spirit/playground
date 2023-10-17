#!/usr/bin/env python

from jsonschema import validate
import json

schema = json.load(open('protein.schema.json',))

validate(instance={"proteinId" : "X13hfgasf4124", "tags" : [ "membrane", "multi-chain" ], "dimensions" : { "length" : 31.5, "width": 14.5, "height" : 32.7  }}, schema=schema)

validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)


