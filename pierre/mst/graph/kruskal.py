#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-


import sys


class Edge:
  def __init__(self, p_g, p_v1, p_v2, p_weight):
    self.m_graph  = p_g
    self.m_v1     = p_v1
    self.m_v2     = p_v2
    self.m_weight = p_weight

  def __str__(self):
    return self.m_graph.m_names[self.m_v1] + "," + self.m_graph.m_names[self.m_v2] + ":" + str(self.m_weight)


class Vertex:
  def __init__(self, p_label):
    self.m_label = p_label

  def __str__(self):
    return self.m_label


class Kruskal:
  def __init__(self, p_adjList):
    self.m_edges    = []
    self.m_vertices = []
    self.m_names    = []

    l_verticesToIndex = {}
    for c_edge in p_adjList:
      if c_edge[0] in l_verticesToIndex:
        l_start = l_verticesToIndex[c_edge[0]]
      else:
        l_start = len(self.m_vertices)
        l_verticesToIndex[c_edge[0]] = l_start
        self.m_vertices.append(Vertex(c_edge[0]))
        self.m_names.append(c_edge[0])
      if c_edge[1] in l_verticesToIndex:
        l_end = l_verticesToIndex[c_edge[1]]
      else:
        l_end = len(self.m_vertices)
        l_verticesToIndex[c_edge[1]] = l_end
        self.m_vertices.append(Vertex(c_edge[1]))
        self.m_names.append(c_edge[1])
      self.m_edges.append(Edge(self, l_start, l_end, c_edge[2]))
    self.m_edges.sort(key=lambda x:x.m_weight)

  def __str__(self):
    res = ""
    for c_edge in self.m_edges:
      res += str(c_edge) + " "
    return res

  def run(self):
    l_kruskal = []
    l_components = [ [x] for x in range(len(self.m_vertices)) ]
    for c_edge in self.m_edges:
      l_v1 = c_edge.m_v1
      for c_comp1 in range(len(l_components)):
        if l_v1 in l_components[c_comp1]:
          break
      l_v2 = c_edge.m_v2
      if l_v2 in l_components[c_comp1]:
        continue
      for c_comp2 in range(len(l_components)):
        if l_v2 in l_components[c_comp2]:
          break
      l_merged = l_components[c_comp1] + l_components[c_comp2]
      if c_comp1 < c_comp2:
        l_components[c_comp1] = l_merged
        l_components.pop(c_comp2)
      else:
        l_components[c_comp2] = l_merged
        l_components.pop(c_comp1)
      l_kruskal.append(c_edge)
    return l_kruskal

