"""
Translate JSON Abstract Data Notation (JADN) files
"""

import os
import sys
import traceback

from libs.codec.jadn import jadn_load, jadn_dump, jadn_check, jadn_analyze
from libs.convert.tr_jas import jas_load, jas_dump
from libs.convert.tr_tables import table_dump

if __name__ == "__main__":
    for fn in ("openc2",):
        ifname = os.path.join("schema", fn)
        ofname = os.path.join("schema_gen", fn)

        # Convert JADN Abstract Syntax (JAS) to JADN

        print(os.path.join(os.getcwd(), ifname + ":"))
        source_s = ifname + ".jas"
        dest = ofname + "_gens"
        schema_s = jas_load(source_s)
        jadn_check(schema_s)
        jadn_dump(schema_s, dest + ".jadn", source_s)
        jadn_analyze(schema_s)

        # Convert JADN to JAS, prettyprinted JADN, and property tables

        source = ifname + ".jadn"
        dest = ofname + "_genj"
        schema = jadn_load(source)
        jas_dump(schema, dest + ".jas", source)
        jadn_dump(schema, dest + ".jadn", source)
        table_dump(schema, dest + ".xlsx", source)

        # Check that they match
        try:
            assert schema == schema_s
        except AssertionError:
            print('Warning:', source_s, '!=', source)
            t1 = {t[0]:t for t in schema_s['types']}
            t2 = {t[0]:t for t in schema['types']}
            for t in set(t1) & set(t2):
                if t1[t] != t2[t]:
                    print('  x', t)
