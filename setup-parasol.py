#!/usr/bin/env python
import brightway2 as bw
import lca_algebraic as agb
from dotenv import load_dotenv
from os import environ as env
from bw2io.ecoinvent import import_ecoinvent_release
import bw2io

load_dotenv()

bw.projects.set_current("parasol-project")

MYDB = "parasol"
agb.resetDb(MYDB)
agb.resetParams(MYDB)
agb.setForeground(MYDB)

# Need to be imported set current project
import parasol_lca

ECOINVENT_VERSION="3.9"
BIOSPHERE_NAME=f"ecoinvent-{ECOINVENT_VERSION}-biosphere"
TECHNOSPHERE_NAME=f"ecoinvent-{ECOINVENT_VERSION}-cutoff"

if TECHNOSPHERE_NAME in bw2io.databases:
    print("Ecoinvent already imported")
else:
    import_ecoinvent_release(
        ECOINVENT_VERSION, "cutoff",
        env["ECOINVENT_LOGIN"],
        env["ECOINVENT_PASSWORD"])

parasol_lca.create({
    "target_database": MYDB,
    "version": ECOINVENT_VERSION,
    "biosphere": BIOSPHERE_NAME,
    "technosphere": TECHNOSPHERE_NAME
})

# Select impact/activity
activity = agb.findActivity('[parasol] PV impact per kWh', db_name=MYDB, single=True)
