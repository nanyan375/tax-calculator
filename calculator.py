#! /usr/bin/env python3

import sys

class Config:
  def __init__(self, confile):
    self._config = {}
    self.confile = confile

  def get_confile(self):
    with open(str(self.confile), 'r') as cfile:
      for line in cfile:
        clist_tmp = line.split('=')
        self._config[clist_tmp[0].strip()] = clist_tmp[1].strip()
    return self._config
  #计算五险一金的总参数
  def social_security(self):
    self.cdata = self.get_confile()
    self.result = 0
    for value in self.cdata.values():
      self.result += value
    return result

class Userdata:
  def __init__(self, userdatafile):
    self.userdata = {}
    self.userdatafile = userdatafile
  def get_userdata(self):
    with open(str(self.userdatafile), 'r') as ufile:
      for line in ufile:
        ulist_tmp = line.split(',')
        self.userdata[str(ulist_tmp[0])] = ulist_tmp[1]
    return self.userdata

  def tax_calculator(self):
    self.udata = self.get_userdata()
    for key,value in self.udata.items():
      try:
        salary=int(value)
      except ValueError:
        return 'ParameterError'
      if salary < 0:
        return "Parameter Error"
      else:
        m = salary*(1-0.165) - 3500
    if m <= 0:
      tax = 0
    elif m <= 1500:
      tax = m*0.03
    elif m > 1500 and m <= 4500:
      tax = m*0.1-105
    elif m > 4500 and m <= 9000:
      tax = m*0.2-555
    elif m > 9000 and m <= 35000:
      tax = m*0.25-1005
    elif m > 35000 and m <= 55000:
      tax = m*0.30-2755
    elif m > 55000 and m <= 80000:
      tax = m*0.35-5505
    else:
      tax = m*0.45-13505
  return format((salary*(1-0.165)-tax), '.2f')
if __name__ == '__main__':
  for arg in sys.argv[1:]:
    arg_list = arg.split(':')
    print(arg_list[0]+':'+str(tax_calculator(int(arg_list[1]))))
