__author__ = 'ragib'

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from RandomDataGenerator import RandomDataGenerator

DEMO_DATA_FILE = "../data/demodata.txt"
DEMO_PARAM_FILE = "../data/demopara.txt"


# RDG = RandomDataGenerator()
RDG = RandomDataGenerator(300, 200, (0.005, 0.3), (0.005, 0.1))

data = RDG.genData()
T = data["T"]
MS = data["MS"]
SDC = data["SDC"]


with open(DEMO_DATA_FILE, "w") as df:
    for t in T:
        df.write("<")
        for its in t:
            df.write( "{" + ", ".join([str(it) for it in its]) + "}" )
        df.write(">\n")

with open(DEMO_PARAM_FILE, "w") as pf:
    for p in MS.keys():
        pf.write("MIS(" + str(p) + ") = " + str(MS[p]) + "\n")
    pf.write("SDC = " + str(SDC) + "\n")