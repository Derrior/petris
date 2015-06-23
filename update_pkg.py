#!/usr/bin/python3

import os

f = open("output.txt", "r")
for s in f.readlines():
    os.system("rm " + s.split()[1])


