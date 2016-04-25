#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-

import sys
import random
import time
import itertools
from collections import defaultdict

class Edge:
  def __init__(self, p_v1, p_v2, p_weight, p_orig = None):
    self.m_v1     = p_v1 # index de noeud
    self.m_v2     = p_v2 # index de noeud
    self.m_weight = p_weight
    self.m_orig   = p_orig


class Vertex:
  def __init__(self, p_label, p_index, p_graph):
    self.m_label     = p_label
    self.m_edges     = []
    self.m_index     = p_index
    self.m_component = p_index
    self.m_graph     = p_graph # toString

  def __str__(self):
    return self.m_label + "[" + str(self.m_index) + "]"  + "[" + str(self.m_component) + "]"
  def toString(self):
    return self.m_label + "[" + str(self.m_index) + "]"  + "[" + self.m_graph.m_vertices[self.getComponent()].m_label + "]"

  def addEdge(self, p_e):
    self.m_edges.append(p_e)

  def getLowestEdge(self):
    l_min = 10000000
    l_res = None
    for c_edge in self.m_edges:
      if c_edge.m_weight < l_min:
        l_min = c_edge.m_weight
        l_res = c_edge
    return l_res

  def getComponent(self):
    if self.m_index != self.m_component:
      self.m_component = self.m_graph.m_vertices[self.m_component].getComponent()
    return self.m_component

  def isComponent(self):
    return self.m_index == self.getComponent()


class RandMst:
  def __init__(self, p_adjList):
    self.m_vertices = []
    self.m_names    = []  # TODO suppress
    self.m_mst      = set()
    self.m_edges    = []

    l_verticesToIndex = {}
    for c_edge in p_adjList:
      if c_edge[0] in l_verticesToIndex:
        l_start = l_verticesToIndex[c_edge[0]]
      else:
        l_start = len(self.m_vertices)
        l_verticesToIndex[c_edge[0]] = l_start
        self.m_vertices.append(Vertex(c_edge[0], l_start, self))
        self.m_names.append(c_edge[0])
      if c_edge[1] in l_verticesToIndex:
        l_end = l_verticesToIndex[c_edge[1]]
      else:
        l_end = len(self.m_vertices)
        l_verticesToIndex[c_edge[1]] = l_end
        self.m_vertices.append(Vertex(c_edge[1], l_end, self))
        self.m_names.append(c_edge[1])
      if len(c_edge) == 4:
        l_edge = Edge(l_start, l_end, c_edge[2], c_edge[3])
      else:
        l_edge = Edge(l_start, l_end, c_edge[2])
      self.m_edges.append(l_edge)
      self.m_vertices[l_start].addEdge(l_edge)
      self.m_vertices[l_end].addEdge(l_edge)

    self.m_vcount = len(self.m_vertices)

  def __str__(self):
    res = ""
    for c_edge in self.m_edges:
      res += str(c_edge) + " "
    return res

  def printComponents(self):
    l_res = [[] for _ in range(len(self.m_vertices))]
    for c_idx in range(len(self.m_vertices)):
      l_vertex = self.m_vertices[c_idx]
      if l_vertex:
        l_res[l_vertex.getComponent()].append(l_vertex.m_label)
    for c_arr in l_res:
      if 0 == len(c_arr):
        continue
  def printEdges(self, p_msg, p_edges):
    print(p_msg, " ".join([self.m_names[x.m_v1] + "," + self.m_names[x.m_v2] + ":" + str(x.m_weight) for x in p_edges]))


  def componentCount(self):
    return self.m_vcount

  def runFull(self, p_level):
    while 1 != self.componentCount():
      #print("FULL ---", self.componentCount(), p_level)
      if not self.boruvkaStep():
        break
    return self.m_mst

  def run(self, p_level = 0):
    #print("---", self.componentCount(), len(self.m_edges), p_level, time.time())
    #self.printEdges("  ", sorted(self.m_edges, key=lambda x:x.m_weight))
    if 1 >= self.componentCount():
      return set()

    self.boruvkaStep()
    #print("-b1", self.componentCount(), len(self.m_edges), p_level, time.time())
    #self.printEdges("s1", sorted(self.m_mst, key=lambda x:x.m_weight))
    self.boruvkaStep()
    #print("-b2", self.componentCount(), len(self.m_edges), p_level, time.time())
    #self.printEdges("s2", sorted(self.m_mst, key=lambda x:x.m_weight))

    l_g0 = self.g0()
    #print("g0", l_g0.componentCount(), p_level)
    #l_g0.printEdges("g0", l_g0.m_edges)
    l_mst2 = set()

    l_g1 = l_g0.g1(0.5)
    #l_g1.printEdges("g1 " + str(l_g1.componentCount()), sorted(l_g1.m_edges, key=lambda x:x.m_weight))
    l_mst1 = l_g1.run(p_level + 1) ## TODO
    #l_g1.printEdges("f1", sorted(l_mst1, key=lambda x:x.m_weight))

    l_g2 = l_g0.g2(l_g1)
    #l_g2.printEdges("g2", sorted(l_g2.m_edges, key=lambda x:x.m_weight))
    l_mst2 = l_g2.run(p_level + 1) ## TODO
    #l_g2.printEdges("f2", sorted(l_mst2, key=lambda x:x.m_weight))

    return self.m_mst | set([c_edge.m_orig for c_edge in l_mst2])

  def g0(self):
    l_adj = []
    l_edgeMap = {}
    for c_edge in self.m_edges:
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 == l_v2:
        continue
      if l_v2 > l_v1:
        l_v1, l_v2 = l_v2, l_v1
      l_edge = (l_v1, l_v2)
      if l_edge in l_edgeMap:
        if c_edge.m_weight < l_edgeMap[l_edge].m_weight:
          l_edgeMap[l_edge] = c_edge
      else:
        l_edgeMap[l_edge] = c_edge
    for c_key, c_value in l_edgeMap.items():
      l_adj.append((str(c_key[0]), str(c_key[1]), c_value.m_weight, c_value))
    return RandMst(l_adj)

  def g1(self, p_prob):
    l_res = RandMst([])
    l_res.m_vertices = [None for x in self.m_vertices]
    l_res.m_names    = self.m_names
    for c_edge in self.m_edges:
      if random.random() < p_prob:
        l_res.addEdge(c_edge)
    l_res.m_vcount   = len([x for x in l_res.m_vertices if x])
    return l_res

  def g1Tst(self, p_prob):
    l_res = RandMst([])
    l_res.m_vertices = [None for x in self.m_vertices]
    l_res.m_names    = self.m_names
    for c_edge in self.m_edges:
      if set([self.m_names[c_edge.m_v1], self.m_names[c_edge.m_v2]]) == set(["A", "D"]) or \
         set([self.m_names[c_edge.m_v1], self.m_names[c_edge.m_v2]]) == set(["D", "F"]) or \
         set([self.m_names[c_edge.m_v1], self.m_names[c_edge.m_v2]]) == set(["B", "D"]) or \
         set([self.m_names[c_edge.m_v1], self.m_names[c_edge.m_v2]]) == set(["B", "E"]) or \
         False:
        l_res.addEdge(c_edge)
    l_res.m_vcount   = len([x for x in l_res.m_vertices if x])
    return l_res

  def g2(self, p_g1):
    #p_g1.printComponents()

    # max weigth for all components
    l_weights = {}
    for c_edge in p_g1.m_edges:
      l_v1 = p_g1.m_vertices[c_edge.m_v1]
      l_v2 = p_g1.m_vertices[c_edge.m_v2]
      l_c1 = l_v1.getComponent()
      if l_c1 == l_v2.getComponent():
        if l_c1 in l_weights:
          if c_edge.m_weight < l_weights[l_c1]:
            continue
        l_weights[l_c1] = c_edge.m_weight

    # build graph
    l_res = RandMst([])
    l_res.m_vertices = [None for x in self.m_vertices]
    l_res.m_names    = self.m_names
    for c_edge in self.m_edges:
      #print("edge " + self.m_names[c_edge.m_v1] + "," + self.m_names[c_edge.m_v2] + ":" + str(c_edge.m_weight))

      l_v1g1 = p_g1.m_vertices[c_edge.m_v1]
      l_v2g1 = p_g1.m_vertices[c_edge.m_v2]
      if None == l_v1g1 or None == l_v2g1:
        #print("add None")
        l_res.addEdge(c_edge)
        continue
      l_c1 = l_v1g1.getComponent()
      if l_c1 == l_v2g1.getComponent():
        # check weight
        l_comp = l_v2g1.getComponent()
        l_weight = 0
        #print("check")
        if c_edge.m_weight <= l_weights[l_c1]:
          # add non F-heavy edge
          #print("add non F-heavy")
          l_res.addEdge(c_edge)
      else:
        # add edge connecting componenents
        #print("add connect")
        l_res.addEdge(c_edge)
    l_res.m_vcount = len([x for x in l_res.m_vertices if x])
    return l_res

  def addEdge(self, p_edge):
    if self.m_vertices[p_edge.m_v1]:
      l_v1 = self.m_vertices[p_edge.m_v1]
    else:
      l_v1 = Vertex(self.m_names[p_edge.m_v1], p_edge.m_v1, self)
      self.m_vertices[p_edge.m_v1] = l_v1
    if self.m_vertices[p_edge.m_v2]:
      l_v2 = self.m_vertices[p_edge.m_v2]
    else:
      l_v2 = Vertex(self.m_names[p_edge.m_v2], p_edge.m_v2, self)
      self.m_vertices[p_edge.m_v2] = l_v2
    l_v1.addEdge(p_edge)
    l_v2.addEdge(p_edge)
    self.m_edges.append(p_edge)

  def boruvkaStep(self):
    #self.printComponents()
    #print("---", self.componentCount())
    l_addedSet = set()
    for c_vertexIdx in range(len(self.m_vertices)):
      l_vertex = self.m_vertices[c_vertexIdx]
      if None == l_vertex or not l_vertex.isComponent():
        continue
      #print("on " + l_vertex.m_label)
      l_edge = l_vertex.getLowestEdge()
      if l_edge and l_edge not in l_addedSet:
        #print(" edge " + str(l_edge))
        l_addedSet.add(l_edge)
    #print("-bs", len(l_addedSet), time.time())
    if 0 == len(l_addedSet):
      return False      # graphe non connecte
    l_contractedVertices = set()
    # self.m_eq = 0
    # self.m_gt = 0
    for c_edge in l_addedSet:
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 != l_v2:
        #print("edge " + str(c_edge))
        l_contractedVertices.add(l_v1)
        l_contractedVertices.add(l_v2)
        self.contractVertices(self.m_vertices[l_v1], self.m_vertices[l_v2])
        #print(" all: " + " ".join(sorted([x.toString() for x in self.m_vertices])))
        self.m_mst.add(c_edge)
    self.contractEdges(l_contractedVertices)
    #print("-eg", self.m_eq, self.m_gt)
    return True

  # Contraction des noeuds
  def contractVertices(self, p_v1, p_v2):
    #print(" contract: " + str(p_v1) + " and " + str(p_v2))
    self.m_vcount -= 1
    p_v2.m_component = p_v1.m_index
  # Puis contraction des aretes une fois tous les noueds contractes
  def contractEdges(self, p_vertices):
    l_edgesOfComponents = defaultdict(list)
    for c_vidx in p_vertices:
      l_vertex = self.m_vertices[c_vidx]
      l_edgesOfComponents[l_vertex.getComponent()].append(l_vertex.m_edges)
      l_vertex.m_edges = []
    for c_comp, c_edgesList in l_edgesOfComponents.items():
      l_edgeMap = {}
      for c_edges in c_edgesList:
        for c_edge in c_edges:
          l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
          l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
          # ___OPTI___
          if l_v2 > l_v1:
            #self.m_gt += 1
            l_v1, l_v2 = l_v2, l_v1
          elif l_v1 == l_v2:
            #self.m_eq += 1
            continue

          l_edge = (l_v1, l_v2)
          if l_edge in l_edgeMap:
            if c_edge.m_weight < l_edgeMap[l_edge].m_weight:
              l_edgeMap[l_edge] = c_edge
          else:
            l_edgeMap[l_edge] = c_edge
      self.m_vertices[c_comp].m_edges = l_edgeMap.values()

    #print("-co", len(p_v1.m_edges) + len(p_v2.m_edges), len(l_edgeMap), time.time())

  ####### NON OPTIMISE ###############################
  # Step pour utiliser les contractions non optimisees
  def boruvkaStepNoOpt(self):
    #self.printComponents()
    #print("---", self.componentCount())
    l_addedSet = set()
    for c_vertexIdx in range(len(self.m_vertices)):
      l_vertex = self.m_vertices[c_vertexIdx]
      if None == l_vertex or not l_vertex.isComponent():
        continue
      #print("on " + l_vertex.m_label)
      l_edge = l_vertex.getLowestEdge()
      if l_edge and l_edge not in l_addedSet:
        #print(" edge " + str(l_edge))
        l_addedSet.add(l_edge)
    #print("-bs", len(l_addedSet), time.time())
    if 0 == len(l_addedSet):
      return False      # graphe non connecte
    l_contractedVertices = set()
    # self.m_eq = 0
    # self.m_gt = 0
    for c_edge in l_addedSet:
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 != l_v2:
        #print("edge " + str(c_edge))
        l_contractedVertices.add(l_v1)
        l_contractedVertices.add(l_v2)
        self.contractNaive(self.m_vertices[l_v1], self.m_vertices[l_v2])
        #self.contractAndRemoveEdges(self.m_vertices[l_v1], self.m_vertices[l_v2])
        #self.contractAndRemoveEdgesOptIf(self.m_vertices[l_v1], self.m_vertices[l_v2])
        #print(" all: " + " ".join(sorted([x.toString() for x in self.m_vertices])))
        self.m_mst.add(c_edge)
    #print("-eg", self.m_eq, self.m_gt)
    return True

  # Supprime uniquement les aretes internes : pas boruvka
  def contractNaive(self, p_v1, p_v2):
    #print(" contract: " + str(p_v1) + " and " + str(p_v2))
    self.m_vcount -= 1
    p_v2.m_component = p_v1.m_index
    l_edges = []
    for c_edge in itertools.chain(p_v1.m_edges, p_v2.m_edges):
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 == l_v2:
        continue
      l_edges.append(c_edge)
    if 0 == len(l_edges):
      self.m_vcount -= 1
    #print("-co", len(p_v1.m_edges) + len(p_v2.m_edges), len(l_edges), time.time())

    p_v1.m_edges = l_edges
    p_v2.m_edges = []

  # Supprime les aretes internes et les aretes de poids trop fort
  def contractAndRemoveEdges(self, p_v1, p_v2):
    #print(" contract: " + str(p_v1) + " and " + str(p_v2))
    self.m_vcount -= 1
    p_v2.m_component = p_v1.m_index
    l_edgeMap = {}
    for c_edge in itertools.chain(p_v1.m_edges, p_v2.m_edges):
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 == l_v2:
        continue
      if l_v2 > l_v1:
        l_v1, l_v2 = l_v2, l_v1
      l_edge = (l_v1, l_v2)
      if l_edge in l_edgeMap:
        if c_edge.m_weight < l_edgeMap[l_edge].m_weight:
          l_edgeMap[l_edge] = c_edge
      else:
        l_edgeMap[l_edge] = c_edge
    if 0 == len(l_edgeMap):
      self.m_vcount -= 1
    #print("-co", len(p_v1.m_edges) + len(p_v2.m_edges), len(l_edgeMap), time.time())

    p_v1.m_edges = l_edgeMap.values()
    p_v2.m_edges = []

  # Le cas == est beaucoup moins frequent que le cas > (sur les index), donc on fait le test > en premier
  def contractAndRemoveEdgesOptIf(self, p_v1, p_v2):
    #print(" contract: " + str(p_v1) + " and " + str(p_v2))
    self.m_vcount -= 1
    p_v2.m_component = p_v1.m_index
    l_edgeMap = {}
    for c_edge in itertools.chain(p_v1.m_edges, p_v2.m_edges):
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      # ___OPTI___
      if l_v2 > l_v1:
        l_v1, l_v2 = l_v2, l_v1
      elif l_v1 == l_v2:
        continue
      l_edge = (l_v1, l_v2)
      if l_edge in l_edgeMap:
        if c_edge.m_weight < l_edgeMap[l_edge].m_weight:
          l_edgeMap[l_edge] = c_edge
      else:
        l_edgeMap[l_edge] = c_edge
    if 0 == len(l_edgeMap):
      self.m_vcount -= 1
    #print("-co", len(p_v1.m_edges) + len(p_v2.m_edges), len(l_edgeMap), time.time())

    p_v1.m_edges = l_edgeMap.values()
    p_v2.m_edges = []
