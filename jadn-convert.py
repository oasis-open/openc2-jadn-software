"""
Translate JSON Abstract Data Notation (JADN) files
"""

import os

from libs.codec.jadn import jadn_load, jadn_dump, jadn_check, jadn_analyze
from libs.convert.tr_jas import jas_load, jas_dump
from libs.convert.tr_tables import table_dump

if __name__ == "__main__":
    for fn in ("openc2",):
        ifname = os.path.join("schema", fn)
        ofname = os.path.join("schema_gen", fn)

        # Convert JADN Abstract Syntax (JAS) to JADN

        print(os.path.join(os.getcwd(), ifname + ":"))
        source = ifname + ".jas"
        dest = ofname + "_gens"
        schema = jas_load(source)
        jadn_check(schema)
        jadn_dump(schema, dest + ".jadn", source)
        jadn_analyze(schema)

        # Convert JADN to JAS, prettyprinted JADN, and property tables

        source = ifname + ".jadn"
        dest = ofname + "_genj"
        schema = jadn_load(source)
        jas_dump(schema, dest + ".jas", source)
        jadn_dump(schema, dest + ".jadn", source)
        table_dump(schema, dest + ".xlsx", source)
