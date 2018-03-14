#! /usr/bin/env python3


import sys

def tax_calculator(salary):
  try:
    salary=int(salary)
  except ValueError:
    return 'ParameterError'
  if salary < 0:
    return "Parameter Error"
  elif salary <= 3500:
    tax = 0
  else:
    m = salary - 3500
    if m <= 1500:
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
  return format(tax, '.2f')

if __name__ == '__main__':
  print(tax_calculator(sys.argv[1]))
