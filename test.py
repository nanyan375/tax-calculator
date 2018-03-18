#!/usr/bin/env python3

from calculator import Argvs
from calculator import Config
from calculator import Userdata
from calculator import Sspay, Tax

argvs = Argvs()
argv = argvs.argvs_read()
print (argv)

config = Config(argv[0])
configdata = config.read_configfile()
print(configdata)

user = Userdata(argv[1])
userdata = user.read_userdata()
print(userdata)

socialsecurity = Sspay()
tax_calcu = Tax()
for number,salary in userdata.items():
  sspay = socialsecurity.get_sspay(configdata, salary)
  tax = tax_calcu.tax_calculator(salary,sspay)
  print(number,sspay,tax)
