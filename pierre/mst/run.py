#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-

import sys
from pprint import pprint
import math
from datetime import datetime

from graph import kruskal
from graph import boruvka
from graph import randmst
from graph import random

RandomGraph = random.RandomGraph
Kruskal = kruskal.Kruskal
Boruvka = boruvka.Boruvka
RandMst = randmst.RandMst

# Verifie que l algo random et Kurskal donne le meme resultat
def compare(p_adj):
  l_g1 = Kruskal(p_adj)
  l_r1 = l_g1.run()
  l_r1 = sorted(l_r1, key=lambda x:x.m_weight)
  #print(sum([x.m_weight for x in l_r1]), " ".join([str(x) for x in l_r1]))

  l_g2 = RandMst(p_adj)
  l_r2 = l_g2.run()
  l_r2 = sorted(l_r2, key=lambda x:x.m_weight)

  if len(l_r1) != len(l_r2):
    return False
  for c_idx in range(len(l_r1)):
    l_e1 = l_r1[c_idx]
    l_e2 = l_r2[c_idx]
    if l_e1.m_v1 != l_e2.m_v1:
      return False
    if l_e1.m_v2 != l_e2.m_v2:
      return False
    if l_e1.m_weight != l_e2.m_weight:
      return False
  return True

# Mesure le temps d execution
def bench(p_adj):
  #print("------------------------------")
  l_g2 = RandMst(p_adj)
  l_g2v = l_g2.componentCount()
  l_g2e = len(l_g2.m_edges)
  l_start = datetime.now()
  l_r2 = l_g2.run()
  l_end = datetime.now()
  l_r2 = sorted(l_r2, key=lambda x:x.m_weight)
  print("r", sum([x.m_weight for x in l_r2]), "v:", l_g2v, "e:", l_g2e, "s:", (l_end - l_start).total_seconds())

  #l_g1 = Kruskal(p_adj)
  #l_start = datetime.now()
  #l_r1 = sorted(l_g1.run(), key=lambda x:x.m_weight)
  #l_end = datetime.now()
  #print("k", sum([x.m_weight for x in l_r1]), "v:", l_g2v, "e:", l_g2e, "s:", (l_end - l_start).total_seconds())

  #l_g1 = Boruvka(p_adj)
  #l_start = datetime.now()
  #l_r1 = sorted(l_g1.run(), key=lambda x:x.m_weight)
  #l_end = datetime.now()
  #print("b", sum([x.m_weight for x in l_r1]), "v:", l_g2v, "e:", l_g2e, "s:", (l_end - l_start).total_seconds())

  sys.stdout.flush()


# Convertit le graphe random en lettres et ajout du poids unique
def toString(p_val):
  l_res = ""
  while True:
    l_res += str(chr(65 + (p_val % 26)))
    p_val //= 26
    if p_val == 0:
      break
  return l_res
def generate(p_vc, p_prob):
  l_start = datetime.now()
  #print(p_vc, p_ec)
  l_graph = RandomGraph(p_vc, p_prob)
  l_weight = 1
  l_edges = []
  for c_edge in l_graph.largestComponentEdges():
    l_edges.append((toString(c_edge[0]), toString(c_edge[1]), l_weight))
    l_weight += 1
  l_end = datetime.now()

  return l_edges


######## MAIN
for c_adj in [
    [ ("A", "B", 1), ("B", "C", 3), ("A", "D", 9), ("A", "E", 7), ("B", "E", 13), ("B", "I", 8), ("B", "F", 10), ("C", "F", 5), ("E", "G", 4), ("E", "H", 11), ("G", "H", 2), ("H", "I", 6) ],
    [ ("A", "B", 7), ("A", "D", 4), ("B", "C", 11), ("B", "D", 9), ("B", "E", 10), ("C", "E", 5), ("D", "E", 15), ("D", "F", 6), ("E", "F", 12), ("E", "G", 8), ("F", "G", 13) ],
    [ ('A', 'E', 0), ('A', 'M', 1), ('B', 'F', 2), ('B', 'N', 3), ('C', 'D', 4), ('C', 'P', 5), ('D', 'L', 6), ('E', 'O', 7), ('F', 'I', 8), ('G', 'I', 9), ('H', 'O', 10),
      ('I', 'O', 11), ('J', 'L', 12), ('K', 'N', 13), ('M', 'P', 14)],
    [ ('A', 'M', 0), ('A', 'V', 1), ('B', 'DA', 2), ('C', 'H', 3), ('C', 'J', 4), ('C', 'CA', 5), ('C', 'FA', 6), ('D', 'V', 7), ('D', 'EA', 8), ('E', 'I', 9), ('E', 'R', 10),
      ('F', 'G', 11), ('F', 'N', 12), ('G', 'W', 13), ('I', 'X', 14), ('J', 'U', 15), ('K', 'M', 16), ('L', '@A', 17), ('M', 'X', 18), ('M', 'AA', 19), ('M', 'BA', 20), ('N', 'Y', 21),
      ('O', 'T', 22), ('P', 'W', 23), ('P', 'X', 24), ('Q', 'T', 25), ('Q', 'BA', 26), ('S', 'FA', 27), ('V', 'FA', 28), ('@A', 'BA', 29), ('@A', 'DA', 30)],
    [ ('L', 'O', 0), ('S', 'D', 1), ('G', 'D', 2), ('A', 'S', 3), ('H', 'B', 4), ('E', 'I', 5), ('F', 'L', 6), ('D', 'A', 7), ('I', 'R', 8), ('P', 'G', 9), ('L', 'J', 10),
      ('I', 'H', 11), ('S', 'O', 12), ('A', 'F', 13), ('N', 'F', 14), ('G', 'T', 15), ('K', 'S', 16), ('J', 'R', 17), ('M', 'D', 19), ('R', 'G', 20)],
    [ ('L', 'O', 0), ('S', 'D', 1), ('G', 'D', 2), ('A', 'S', 3), ('H', 'B', 4), ('E', 'I', 5), ('F', 'L', 6), ('D', 'A', 7), ('I', 'R', 8), ('P', 'G', 9), ('L', 'J', 10),
      ('I', 'H', 11), ('S', 'O', 12), ('A', 'F', 13), ('N', 'F', 14), ('G', 'T', 15), ('K', 'S', 16), ('J', 'R', 17), ('Q', 'C', 18), ('M', 'D', 19), ('R', 'G', 20), ('O', 'T', 21),
      ('I', 'J', 22), ('H', 'P', 23), ('O', 'E', 24), ('I', 'K', 25), ('H', 'C', 26), ('I', 'P', 27), ('N', 'S', 28), ('C', 'A', 29), ('T', 'P', 30), ('E', 'D', 31), ('M', 'L', 32),
      ('A', 'I', 33), ('G', 'O', 34), ('H', 'F', 35), ('L', 'N', 36), ('N', 'I', 37), ('H', 'Q', 38), ('O', 'F', 39), ('K', 'Q', 40)],
    [ ('A', 'JA', 0), ('B', 'IA', 1), ('C', 'M', 2), ('C', 'EB', 3), ('C', 'KB', 4), ('D', 'S', 5), ('D', '@A', 6), ('D', 'EA', 7), ('E', 'HA', 8), ('F', 'K', 9), ('G', 'S', 10),
      ('G', 'MA', 11), ('H', 'PA', 12), ('H', '@B', 13), ('I', 'GB', 14), ('J', 'FB', 15), ('K', 'UA', 16), ('L', 'HA', 17), ('L', 'RA', 18), ('M', 'BB', 19), ('N', 'Q', 20), ('N', 'HA', 21),
      ('N', 'IA', 22), ('O', 'U', 23), ('O', 'AA', 24), ('O', 'BB', 25), ('P', 'S', 26), ('R', 'LA', 27), ('T', 'X', 28), ('T', 'DB', 29), ('U', 'JA', 30), ('V', 'Y', 31), ('W', 'JA', 32),
      ('W', 'PA', 33), ('Y', 'CA', 34), ('Y', 'IB', 35), ('@A', 'FA', 36), ('BA', 'JA', 37), ('CA', 'DA', 38), ('CA', 'GB', 39), ('DA', 'QA', 40), ('FA', 'OA', 41), ('FA', 'TA', 42),
      ('GA', 'CB', 43), ('GA', 'GB', 44), ('GA', 'JB', 45), ('HA', 'KA', 46), ('IA', 'AB', 47), ('IA', 'FB', 48), ('KA', 'DB', 49), ('LA', 'VA', 50), ('MA', 'WA', 51), ('NA', 'PA', 52),
      ('OA', 'LB', 53), ('QA', 'XA', 54), ('SA', 'JB', 55), ('UA', 'CB', 56), ('VA', 'FB', 57), ('WA', 'YA', 58), ('@B', 'HB', 59), ('AB', 'HB', 60), ('BB', 'LB', 61), ('IB', 'LB', 62)],
    [ ('A', 'HA', 0), ('A', 'BB', 1), ('A', 'QB', 2), ('B', 'PC', 3), ('C', 'KB', 4), ('D', 'GC', 5), ('E', 'J', 6), ('E', 'SA', 7), ('E', '@C', 8), ('F', 'VA', 9), ('G', 'QD', 10),
      ('H', 'WC', 11), ('I', 'T', 12), ('I', 'OA', 13), ('K', 'X', 14), ('K', 'EC', 15), ('K', 'XD', 16), ('L', 'DB', 17), ('L', 'XB', 18), ('M', 'FC', 19), ('M', 'IC', 20), ('N', 'DD', 21),
      ('O', 'Q', 22), ('O', 'AA', 23), ('O', 'AC', 24), ('P', '@B', 25), ('P', 'WB', 26), ('R', 'AC', 27), ('R', 'ID', 28), ('S', 'UA', 29), ('T', 'HC', 30), ('T', 'GD', 31), ('U', 'XC', 32),
      ('V', 'UA', 33), ('V', 'AB', 34), ('W', 'UB', 35), ('W', 'HC', 36), ('X', 'CB', 37), ('X', 'RB', 38), ('Y', 'GC', 39), ('@A', 'HA', 40), ('AA', 'PB', 41), ('AA', 'UC', 42), ('AA', 'MD', 43),
      ('BA', 'OB', 44), ('BA', 'JD', 45), ('BA', 'SD', 46), ('CA', 'SA', 47), ('DA', 'ED', 48), ('EA', 'PD', 49), ('FA', '@B', 50), ('GA', 'OC', 51), ('GA', 'XC', 52), ('HA', 'PC', 53), ('IA', 'XA', 54),
      ('IA', 'RC', 55), ('JA', 'UC', 56), ('KA', 'XB', 57), ('KA', 'PC', 58), ('LA', 'ID', 59), ('MA', 'AB', 60), ('MA', 'VB', 61), ('MA', 'WC', 62), ('NA', 'NC', 63), ('OA', 'QC', 64), ('OA', 'RC', 65),
      ('PA', 'RA', 66), ('QA', 'EC', 67), ('RA', 'GB', 68), ('RA', 'SB', 69), ('RA', 'CD', 70), ('SA', 'MC', 71), ('SA', '@D', 72), ('TA', 'TD', 73), ('VA', 'LD', 74), ('WA', 'LB', 75), ('WA', 'BC', 76),
      ('WA', 'XC', 77), ('YA', 'SC', 78), ('@B', 'ND', 79), ('AB', 'MC', 80), ('BB', 'SC', 81), ('BB', 'OD', 82), ('CB', 'CC', 83), ('DB', 'RD', 84), ('EB', 'PD', 85), ('FB', 'CC', 86), ('HB', 'HD', 87),
      ('IB', 'MB', 88), ('IB', 'LD', 89), ('JB', 'RB', 90), ('JB', 'LC', 91), ('KB', 'SB', 92), ('LB', 'BD', 93), ('MB', 'JC', 94), ('MB', 'FD', 95), ('MB', 'MD', 96), ('MB', 'PD', 97), ('NB', 'UD', 98),
      ('NB', 'WD', 99), ('OB', 'DD', 100), ('PB', 'MC', 101), ('SB', 'NC', 102), ('TB', 'JC', 103), ('TB', 'UD', 104), ('WB', 'QD', 105), ('XB', 'HD', 106), ('YB', 'CC', 107), ('@C', 'RC', 108),
      ('BC', 'NC', 109), ('DC', 'IC', 110), ('EC', 'UC', 111), ('FC', 'ED', 112), ('FC', 'VD', 113), ('GC', 'FD', 114), ('JC', 'ED', 115), ('KC', 'XC', 116), ('OC', 'SD', 117), ('PC', 'VC', 118),
      ('PC', 'KD', 119), ('PC', 'XD', 120), ('QC', 'AD', 121), ('TC', 'BD', 122), ('TC', 'ID', 123), ('TC', 'QD', 124), ('YC', 'CD', 125), ('DD', 'TD', 126)]
]:
  # comparasion sur des graphes en dur
  if 2 > len(sys.argv):
    if compare(c_adj):
      #print("ok")
      pass
    else:
      print("### Error")
      sys.exit(1)

# comparasion sur des graphes randomw
if 2 > len(sys.argv):
  for c_vc in [100, 200, 400, 800, 1600, 3200]:
    print()
    print(c_vc, end="")
    l_edgeCounts = [ x for x in range(2, int((c_vc - 1) // 2), int((c_vc - 1) // 20)) ]
    l_edgeCounts.append(int(1 + math.log(c_vc)))
    l_edgeCounts.append(1)
    for c_edgeCount in sorted(l_edgeCounts):
      l_adj = generate(c_vc, int(c_vc * min(c_edgeCount, (c_vc - 1) // 2)))
      print(".", end="")
      sys.stdout.flush()
      if not compare(l_adj):
        print("### Error")
        sys.exit(1)

# mesure de temps sur des graphes random
if 2 <= len(sys.argv):
  for x in sys.argv[1:]:
    l_nodeCount = int(x)
    l_probas = [ x / 10.0 for x in range(1, 11) ]

    for c_proba in sorted(l_probas):
      l_adj = generate(l_nodeCount, c_proba)
      for i in range(10):
        bench(l_adj)


