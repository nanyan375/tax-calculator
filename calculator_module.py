#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, csv
import getopt, configparser
import datetime

class Prefix:
  def __init__(self):
    self.args = sys.argv[1:]
  def usage(self):
    print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
  def deal_with_args(self):
    argss = {}
    try:
      shortargs = 'hC:c:d:o:'
      longargs = ['help']
      opts, args = getopt.getopt(self.args, shortargs, longargs)
      for opt,arg in opts:
        argss[opt] = arg 
      if '-h' in argss.keys():
        self.usage()
      if '--help' in argss.keys():
        self.usage()
      return argss
    except getopt.GetoptError:
      print("Error")
      self.usage()
      sys.exit(1)
  def configparse(self):
    configdata = {}
    args = self.deal_with_args()
    config = configparser.ConfigParser()
    try:
      config.read(args['-c'])
    except ValueError:
      print('The arguments did not include the configfile')
    if '-C' in args.keys():
      con_list = config.items(args['-C'].upper())
    else:
      con_list = config.items('DEFAULT')
    for key,value in con_list:
      configdata[key] = float(value)
    return configdata  

"""
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
"""

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
      percent = configdata['yanglao'] + configdata['yiliao'] + configdata['shiye'] + configdata['gongshang'] + configdata['shengyu'] + configdata['gongjijin']
      if salary < 0:
        raise
      elif salary >= 0 and salary <= configdata['jishul']:
        self.sspay = configdata['jishul'] * percent
      elif salary >= configdata['jishuh']:
        self.sspay = configdata['jishuh'] * percent
      else:
        self.sspay = salary * percent
    except:
      print ('something wrong!')
    return float(self.sspay)

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
    return float(tax)

def main():
  prefix = Prefix()
  args = prefix.deal_with_args()
  configdata = prefix.configparse()
  user = Userdata(args['-d'])
  userdata = user.read_userdata()
  tax_cal = Tax()
  socialsecurity = Sspay()
  result = []
  for number,salary in userdata.items():
    sspay = socialsecurity.get_sspay(configdata, salary)
    tax = tax_cal.tax_calculator(salary, sspay)
    net_pay = salary - sspay - tax
    result.append((number,salary,'%.2f'%sspay,'%.2f'%tax,'%.2f'%net_pay, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
  with open(args['-o'], 'w', newline='') as f:
    writer = csv.writer(f)
    for row in result:
      writer.writerow(row)

if __name__ == '__main__':
  main()
  
