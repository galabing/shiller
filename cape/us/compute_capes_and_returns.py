#!/usr/bin/python

import argparse

X = [1, 3, 6, 12, 24, 60, 120]  # for calculating cape
Y = [1, 3, 6, 12, 24, 60, 120]  # for calculating returns

def tofloat(s):
  if s == '' or s == 'NA':
    return None
  return float(s)

def tostr(f):
  if f is None:
    return 'NA'
  return '%.2f' % f

def compute_cape(rps, res, i, x):
  if i < x:
    return None
  rp = rps[i]
  re = res[i-x:i]
  if any([e is None for e in re]):
    return None
  return rp/(sum(re)/x)

def compute_return(ps, i, y):
  n = len(ps)
  if i+y >= n:
    return None
  return (ps[i+y] - ps[i]) / ps[i]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--parsed_file', required=True)
  parser.add_argument('--output_file', required=True)
  args = parser.parse_args()

  with open(args.parsed_file, 'r') as fp:
    lines = fp.read().splitlines()
  dates = []
  ps, ds, es = [], [], []  # price, dividend, earnings
  cpis = []
  rs = []  # long interest rate GS10
  rps, rds, res = [], [], []  # real price, real dividend, real earnings
  cape10s = []
  for line in lines:
    date, p, d, e, cpi, f, r, rp, rd, re, cape10 = line.split('\t')
    dates.append(date)
    ps.append(tofloat(p))
    ds.append(tofloat(d))
    es.append(tofloat(e))
    cpis.append(tofloat(cpi))
    rs.append(tofloat(r))
    rps.append(tofloat(rp))
    rds.append(tofloat(rd))
    res.append(tofloat(re))
    cape10s.append(tofloat(cape10))

  capes = []
  rets = []
  rrets = []
  n = len(dates)
  for x in X:
    cape = []
    for i in range(n):
      cape.append(compute_cape(rps, res, i, x))
    capes.append(cape)
  for y in Y:
    ret = []
    rret = []
    for i in range(n):
      ret.append(compute_return(ps, i, y))
      rret.append(compute_return(rps, i, y))
    rets.append(ret)
    rrets.append(rret)

  headers = ['date']
  for x in X:
    headers.append('cape-%d' % x)
  headers.append('shiller-cape')
  for y in Y:
    headers.append('ret-%d' % y)
  for y in Y:
    headers.append('rret-%d' % y)
  with open(args.output_file, 'w') as fp:
    print >> fp, '\t'.join(headers)
    for i in range(n):
      line = [dates[i]]
      for j in range(len(capes)):
        line.append(tostr(capes[j][i]))
      line.append(tostr(cape10s[i]))
      for j in range(len(rets)):
        line.append(tostr(rets[j][i]))
      for j in range(len(rrets)):
        line.append(tostr(rrets[j][i]))
      print >> fp, '\t'.join(line)

if __name__ == '__main__':
  main()

