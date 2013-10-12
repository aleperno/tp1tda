"""Graph.py
Description: simple & undirected graph implementation for course 75.29 Teoria de
Algoritmos @ University of Buenos Aires

Authors:
Medrano, Lautaro
Pernin, Alejandro
"""

import re
import heapq

class Edge:

	def __init__(self, vertex1, vertex2):
		self.vertex1 = vertex1
		self.vertex2 = vertex2
		self.label = ''
	
	def __str__(self):
		s = "%s <-> %s " % (self.vertex1, self.vertex2)
		return s

class Vertex:

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value


class Graph:

	def __init__(self):
		#Standalone initialization
		self.graph = {}

	def __str__(self):
		#Prints graph as 'vertex: [edges]'
		s = ''
		for i in self.graph.keys():
			s += "%s: " % i
			for j in self.graph[i].keys():
				s += "%s," % j
			s += "\n"
		return s

	def addVertex(self, vertex):
		self.graph[vertex.value] = {}

	def delVertex(self, vertex):
		try:
			self.graph.pop(vertex.value)
			return True
		except KeyError:
			#Vertex not in graph
			return False

	def isVertex(self, vertex):
		return self.graph.has_key(vertex.value)

	def getAllVertex(self):
		#Returns all the keys
		return self.graph.keys()

	def getAllNeighbours(self,vertex):
		#Returns dictionary containing all the neighbours of the vertex
		try:
			return self.graph[vertex]
		except KeyError:
			#Vertex not found in graph
			return False

	def addEdge(self, edge):
		#First checks if there is vertex exists
		try:
			""" Could have asked isVertex but this is fastest (one less step), 
				if the keys	does not exists it fails, otherwise it adds the edge
			"""
			self.graph[edge.vertex1.value][edge.vertex2.value] = edge.label
			self.graph[edge.vertex2.value][edge.vertex1.value] = edge.label
			#Crossing values so the graph stays undirected
			return True
		except KeyError:
			#Either vertex not in graph
			print "Error while adding edge"
			return False

	def delEdge(self, vertex1, vertex2):
		#As it is undirected, both references must be deleted
		try:
			self.graph[vertex2.value].pop(vertex1.value)
			self.graph[vertex1.value].pop(vertex2.value)
			return True
		except KeyError:
			#Either vertex not in graph or no edge
			print "Error while deleting edge"
			return False