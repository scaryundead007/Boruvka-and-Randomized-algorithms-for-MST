#! /usr/bin/env python3.4
#-*- coding: utf-8 -*-

# taken from https://jeremykun.com/2013/08/22/the-erdos-renyi-random-graph/
# and https://breakingcode.wordpress.com/2013/04/08/finding-connected-components-in-a-graph/

import random

class Node(object):
  def __init__(self, index):
    self.index = index
    self.neighbors = set()

  def __repr__(self):
    return repr(self.index)

class RandomGraph(object):
  def __init__(self, n, p):
    self.m_vertices = [Node(i) for i in range(n)]
    edges = [(i,j) for i in range(n) for j in range(i) if random.random() < p]

    for (i,j) in edges:
      self.m_vertices[i].neighbors.add(self.m_vertices[j])
      self.m_vertices[j].neighbors.add(self.m_vertices[i])

  def connectedComponents(self):
    l_components = []
    l_vertices = set(self.m_vertices)

    while l_vertices:
      l_vertex = l_vertices.pop()
      l_queue = [ l_vertex ]
      l_component = set()
      l_component.add(l_vertex)

      while l_queue:
        l_vertex = l_queue.pop(0)
        l_neighbors = l_vertex.neighbors - l_component
        l_component |= l_neighbors
        l_queue.extend(l_neighbors)
        l_vertices -= l_neighbors
      l_components.append(l_component)
    return l_components

  def largestComponent(self):
    l_max  = 0
    l_maxC = None
    for c in self.connectedComponents():
      if len(c) > l_max:
        l_max = len(c)
        l_maxC = c
    return l_maxC

  def largestComponentEdges(self):
    l_lc = self.largestComponent()
    l_res = set()
    for c_vertex in l_lc:
      for c_neighbors in c_vertex.neighbors:
        if c_vertex.index > c_neighbors.index:
          l_res.add((c_vertex.index, c_neighbors.index))
    return l_res
