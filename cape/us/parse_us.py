#!/usr/bin/python

import argparse

HEADER = '\t'.join([
  'Date',
  'P',  # S&P Comp.
  'D',  # Dividend
  'E',  # Earnings
  'CPI',  # Consumer Price Index
  'Fraction',  # Date Fraction
  'Rate GS10',  # Long Interest Rate GS10
  'Price',  # Real Price
  'Dividend',  # Real Dividend
  'Earnings',  # Real Earnings
  'CAPE',
])

def sanitize_date(date, prev_date):
  yyyy, mm = date.split('.')
  if mm == '1':  # a bug in shiller's spreadsheet
    mm = '10'
  assert len(yyyy) == 4
  assert len(mm) == 2
  if prev_date == None:
    return '%s.%s' % (yyyy, mm)
  y, m = int(yyyy), int(mm)
  py, pm = prev_date.split('.')
  py, pm = int(py), int(pm)
  assert m >= 1
  assert m <= 12
  if pm < 12:
    assert y == py
    assert m == pm + 1
  else:
    assert y == py + 1
    assert m == 1
  return '%s.%s' % (yyyy, mm)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--raw_file', required=True)
  parser.add_argument('--parsed_file', required=True)
  args = parser.parse_args()

  with open(args.raw_file, 'r') as fp:
    lines = fp.read().splitlines()

  fp = open(args.parsed_file, 'w')
  start = False
  end = False
  prev_date = None
  for line in lines:
    if not start:
      if line == HEADER:
        start = True
      continue
    assert not end
    date, p, d, e, cpi, f, r, rp, rd, re, cape = line.split('\t')
    if date == '':
      end = True
      continue
    prev_date = sanitize_date(date, prev_date)
    print >> fp, '\t'.join([
        prev_date, p, d, e, cpi, f, r, rp, rd, re, cape])
  fp.close()

if __name__ == '__main__':
  main()

