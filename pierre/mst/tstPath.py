#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-

import sys

from graph import boruvkaMax
from graph import pathmax

BoruvkaMax = boruvkaMax.Boruvka
Edge = boruvkaMax.Edge
PathMax = pathmax.PathMax

def compare(p_adj):
  l_edgeList = [ Edge(x[0],x[1],x[2]) for x in p_adj ]
  l_pm = PathMax(l_edgeList)
  l_bm = BoruvkaMax(l_edgeList)
  l_bm.run()

  for c_u in l_pm.m_msf:
    for c_v in l_pm.m_msf:
      if c_u < c_v:
        continue
      l_uvp = l_pm.getMax(c_u, c_v)
      l_vup = l_pm.getMax(c_v, c_u)
      if l_uvp != l_vup:
        print("ERROR Path", c_u, c_v, l_uvp, l_vup)
        sys.exit(1)
      l_uvb = l_bm.getMax(c_u, c_v)
      l_vub = l_bm.getMax(c_v, c_u)
      if l_uvb != l_vub:
        print("ERROR Boru", c_u, c_v, l_uvb, l_vub)
        sys.exit(1)
      if l_uvp != l_uvb:
        print("ERROR BP", c_u, c_v, l_uvb, l_uvp)
        sys.exit(1)
      print(c_u, c_v, l_uvp)


######################################################################
if __name__ == "__main__":
  l_adjs = [
    [
      (5, 6, 76),
      (3, 4, 97),
      (2, 0, 67),
      (2, 1, 78),
      (4, 6, 86),
      (3, 1, 103),
    ],
    [
      (1, 2, 1),
      (3, 2, 2),
      (3, 4, 3),
      (5, 4, 4),
      (5, 6, 5),
    ],
    [
      (1, 2, 1),
      (3, 2, 2),
      (2, 4, 3),
    ],
    [
      (5, 6, 76),
      (3, 4, 97),
      (2, 0, 67),
      (2, 1, 78),
      (4, 6, 86),
      (3, 1, 103),
    ],
    [
      (6, 5, 61),
      (2, 3, 59),
      (0, 3, 97),
      (3, 6, 64),
      (2, 1, 78),
    ]
  ]
  for c_adj in l_adjs:
    compare(c_adj)
    print("----")

