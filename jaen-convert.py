"""
Translate JSON Abstract Encoding Notation (JAEN) files
"""

import os

from jaen.codec.jaen import jaen_load, jaen_dump, jaen_check
from jaen.convert.tr_jas import jas_load, jas_dump
from jaen.convert.tr_tables import table_dump

if __name__ == "__main__":
    for fn in ("openc2", "cybox", "observables"):
        ifname = os.path.join("data", fn)
        ofname = os.path.join("data_gen", fn)

        # Convert JAEN Abstract Syntax (JAS) to JAEN

        source = ifname + ".jas"
        dest = ofname + "_gens"
        jaen = jas_load(source)
        jaen_check(jaen)
        jaen_dump(jaen, dest + ".jaen", source)

        # Convert JAEN to JAS, prettyprinted JAEN, and property tables

        source = ifname + ".jaen"
        dest = ofname + "_genj"
        jaen = jaen_load(source)
        jas_dump(jaen, dest + ".jas", source)
        jaen_dump(jaen, dest + ".jaen", source)
        table_dump(jaen, dest + ".xlsx", source)
