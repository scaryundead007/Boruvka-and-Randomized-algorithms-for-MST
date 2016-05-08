#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-

import sys
from collections import defaultdict

class Edge:
  def __init__(self, p_v1, p_v2, p_weight):
    self.m_v1     = p_v1   # index
    self.m_v2     = p_v2   # index
    self.m_weight = p_weight


class Vertex:
  def __init__(self, p_label, p_index, p_graph):
    self.m_label      = p_label
    self.m_edges      = []
    self.m_index      = p_index
    self.m_component  = p_index
    self.m_compVerts  = [p_index]
    self.m_compWeight = -1
    self.m_maxPath    = defaultdict(dict)
    self.m_graph      = p_graph # toString

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
    if self.m_index == self.m_component:
      return self.m_component
    return self.m_graph.m_vertices[self.m_component].getComponent()

  def isComponent(self):
    return self.m_index == self.getComponent()


class PathMax:
  def __init__(self, p_edgeList):
    self.m_edges       = []
    self.m_vertices    = []
    self.m_compWeights = defaultdict(lambda: defaultdict(lambda: -1))

    l_vertices = {}
    for c_edge in p_edgeList:
      self.m_edges.append(c_edge)
      l_start = c_edge.m_v1
      if l_start not in l_vertices:
        l_vertices[l_start] = Vertex(l_start, l_start, self)
      l_end = c_edge.m_v2
      if l_end not in l_vertices:
        l_vertices[l_end] = Vertex(l_end, l_end, self)
      l_vertices[l_start].addEdge(c_edge)
      l_vertices[l_end].addEdge(c_edge)

    self.m_vertices = []
    for c_key, c_vertex in l_vertices.items():
      while len(self.m_vertices) <= c_key:
        self.m_vertices.append(None)
      self.m_vertices[c_key] = c_vertex

  def __str__(self):
    res = ""
    for c_edge in self.m_edges:
      res += str(c_edge) + " "
    return res

  def getMax(self, p_u, p_v):
    #print("---", p_u, p_v)
    return self.m_compWeights[p_u][p_v]

  def printComponents(self):
    l_res = [[] for _ in range(len(self.m_vertices))]
    for c_idx in range(len(self.m_vertices)):
      l_vertex = self.m_vertices[c_idx]
      if l_vertex:
        l_res[l_vertex.getComponent()].append(l_vertex.m_label)
    for c_arr in l_res:
      if 0 == len(c_arr):
        continue
      print(sorted(c_arr))

  def compWeights(self):
    l_res = ""
    for c_src in self.m_compWeights:
      for c_dst in self.m_compWeights[c_src]:
        l_res += str(c_src) + "," + str(c_dst) + "," + str(self.m_compWeights[c_src][c_dst]) + " "
    return l_res

  def run(self):
    #print("---", self.compWeights())
    for c_edge in sorted(self.m_edges, key=lambda x:x.m_weight):
      #print("------------------------------", self.componentCount())
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 != l_v2:
        #print("edge " + str(c_edge))
        #print("-", c_edge.m_v1, c_edge.m_v2, c_edge.m_weight)
        self.contractVertices(self.m_vertices[l_v1], self.m_vertices[l_v2], c_edge.m_weight)
        #print(" all: " + " ".join(sorted([x.toString() for x in self.m_vertices])))
        #print("--", self.compWeights())

  # Contraction des noeuds
  def contractVertices(self, p_v1, p_v2, p_weight):
    #print("-", p_v1.m_index, p_v2.m_index, p_v1.m_compVerts, p_v2.m_compVerts)
    #print(" contract: " + str(p_v1) + " and " + str(p_v2))
    p_v2.m_component = p_v1.m_index

    for c_u in p_v1.m_compVerts:
      for c_v in p_v2.m_compVerts:
        l_maxW = max(self.m_compWeights[c_u][p_v1.m_index],
                     self.m_compWeights[c_v][p_v2.m_index],
                     p_weight)
        self.m_compWeights[c_u][c_v] = l_maxW
        self.m_compWeights[c_v][c_u] = l_maxW

    p_v1.m_compVerts.extend(p_v2.m_compVerts)
    p_v1.m_compWeight = max(p_v1.m_compWeight, p_v2.m_compWeight, p_weight)
