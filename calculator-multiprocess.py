#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, csv, queue
from multiprocessing import Process,Queue

class Argvs:
  def __init__(self):
    self.args = sys.argv[1:]
  def argvs_read(self):
    try:
      index_c = self.args.index('-c')
      configfile = self.args[index_c + 1]
      index_u = self.args.index('-d')
      userdatafile = self.args[index_u+1]
      index_o = self.args.index('-o')
      outputfile = self.args[index_o+1]
    except:
      raise
    return configfile,userdatafile,outputfile

class Config:
  def __init__(self, configfile):
    self._config = {}
    self.configfile = configfile
  def read_configfile(self):
    with open(self.configfile, 'r') as cfile:
      for line in cfile:
        clist_tmp = line.strip('\n').split('=')
        try:
          self._config[clist_tmp[0].strip()] = float(clist_tmp[1].strip())
        except:
          print('Type changing has wrong!')
    return self._config

class Userdata:
  def __init__(self, userdatafile):
    self.userdata = {}
    self.userdatafile = userdatafile
  def read_userdata(self):
    with open(self.userdatafile, 'r') as ufile:
      reader = csv.reader(ufile)
      for line in reader:
        try:
          self.userdata[int(line[0].strip())] = int(line[1].strip())
        except ValueError:
          print('Type changing has wrong!')
    return self.userdata

class Sspay:
  def __init__(self):
    self.sspay = 0
  def get_sspay(self, configdata, salary):
    try:
      percent = configdata['YangLao'] + configdata['YiLiao'] + configdata['ShiYe'] + configdata['GongShang'] + configdata['ShengYu'] + configdata['GongJiJin']
      if salary < 0:
        raise
      elif salary >= 0 and salary <= configdata['JiShuL']:
        self.sspay = configdata['JiShuL'] * percent
      elif salary >= configdata['JiShuH']:
        self.sspay = configdata['JiShuH'] * percent
      else:
        self.sspay = salary * percent
    except:
      print ('something wrong!')
    return float('%.2f'%self.sspay)

class Tax:
  def tax_calculator(self, salary, sspay):
    if salary < 0:
      return "Parameter Error"
    else:
      m = salary - sspay - 3500
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
    return float('%.2f'%tax)

def main():
  argv = Argvs()
  argvs = argv.argvs_read()
  config = Config(argvs[0])
  configdata = config.read_configfile()
  user = Userdata(argvs[1])
  userdata = user.read_userdata()
  tax_cal = Tax()
  socialsecurity = Sspay()
  result = []
  q1 = Queue()
  q2 = Queue()
  def f1(q1):
    for number,salary in userdata.items():
      q1.put((number, salary))
  def f2(q1, q2):
    while True:
      try:
        newdata = q1.get(timeout=1)
      except queue.Empty:
        return
      sspay = socialsecurity.get_sspay(configdata, newdata[1])
      tax = tax_cal.tax_calculator(newdata[1], sspay)
      net_pay = newdata[1] - sspay - tax
      q2.put((newdata[0],newdata[1],sspay,tax,float('%.2f'%net_pay)))
  def f3(q2):
    with open(argvs[2], 'w', newline='') as f:
      writer = csv.writer(f)
      while True:
        try:
          writer.writerow(q2.get(timeout=1))
        except queue.Empty:
          return
  p1 = Process(target=f1, args=(q1,))
  p2 = Process(target=f2, args=(q1,q2))
  p3 = Process(target=f3, args=(q2,))
  
  p1.start()
  p2.start()
  p3.start()
  p1.join()
  p2.join()
  p3.join()
  p1.terminate()
      
'''
  for number,salary in userdata.items():
    sspay = socialsecurity.get_sspay(configdata, salary)
    tax = tax_cal.tax_calculator(salary, sspay)
    net_pay = salary - sspay - tax
    result.append((number,salary,sspay,tax,float('%.2f'%net_pay)))
  with open(argvs[2], 'w', newline='') as f:
    writer = csv.writer(f)
    for row in result:
      writer.writerow(row)
'''

if __name__ == '__main__':
  main()
  
