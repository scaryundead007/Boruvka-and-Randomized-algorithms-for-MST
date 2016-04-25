#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-

import sys

class Edge:
  def __init__(self, p_v1, p_v2, p_weight):
    self.m_v1     = p_v1   # index
    self.m_v2     = p_v2   # index
    self.m_weight = p_weight


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
    if self.m_index == self.m_component:
      return self.m_component
    return self.m_graph.m_vertices[self.m_component].getComponent()

  def isComponent(self):
    return self.m_index == self.getComponent()


class Boruvka:
  def __init__(self, p_adjList):
    self.m_vertices = []
    self.m_names    = []  # TODO suppress
    self.m_mst      = []

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
      l_edge = Edge(l_start, l_end, c_edge[2])
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
      l_res[l_vertex.getComponent()].append(l_vertex.m_label)
    for c_arr in l_res:
      if 0 == len(c_arr):
        continue
      print(sorted(c_arr))

  def componentCount(self):
    return self.m_vcount

  def run(self):
    while 1 != self.componentCount():
      #self.printComponents()
      #print("------------------------------", self.componentCount())
      l_addedSet = set()
      for c_vertexIdx in range(len(self.m_vertices)):
        l_vertex = self.m_vertices[c_vertexIdx]
        if not l_vertex.isComponent():
          continue
        #print("on " + l_vertex.m_label)
        l_edge = l_vertex.getLowestEdge()
        if l_edge not in l_addedSet:
          #print(" edge " + str(l_edge))
          l_addedSet.add(l_edge)
      for c_edge in l_addedSet:
        l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
        l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
        if l_v1 != l_v2:
          #print("edge " + str(c_edge))
          self.contract(self.m_vertices[l_v1], self.m_vertices[l_v2])
          #print(" all: " + " ".join(sorted([x.toString() for x in self.m_vertices])))
          self.m_mst.append(c_edge)
    return self.m_mst

  def contract(self, p_v1, p_v2):
    #print(" contract: " + str(p_v1) + " and " + str(p_v2))
    self.m_vcount -= 1
    p_v2.m_component = p_v1.m_index
    l_edges = []
    for c_edge in p_v1.m_edges: # pour toutes les aretes reliees au sommet v1
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 != l_v2:
        l_edges.append(c_edge)
    for c_edge in p_v2.m_edges:
      l_v1 = self.m_vertices[c_edge.m_v1].getComponent()
      l_v2 = self.m_vertices[c_edge.m_v2].getComponent()
      if l_v1 != l_v2:
        l_edges.append(c_edge)
    p_v1.m_edges = l_edges
    p_v2.m_edges = []
