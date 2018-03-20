#!/usr/bin/env python3

import sys,csv,getopt,configparser,time

from calculator import Prefix

prefix = Prefix()
result = prefix.deal_with_args()
print(result)
#print(prefix.configparse())

