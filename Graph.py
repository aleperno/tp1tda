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

	def __init__(self, key):
		self.key = key

		#To ve used on DFS
		self.father = None
		self.visited = False

	def __eq__(self,other):
		return self.key == other.key

	def __str__(self):
		return self.key

	def isVisited(self):
		return self.visited

	def visit(self):
		print "Visitando %s" % self.key
		self.visited=True

class Graph:

	def __init__(self):
		#Standalone initialization
		self.vertices = {}
		self.adjacencies = {}


	def __str__(self):
		#Prints graph as 'vertex: [edges]'
		s=''
		for v in self.vertices.keys():
			#First character on the line is the vertex
			s += "%s: " % v
			for a in self.adjacencies[v]:
				s += "%s," % a
			s += "\n"
		return s

	def isVertex(self, vertex):
		return self.vertices.has_key(vertex.key)

	def addVertex(self, vertex):
		if not self.isVertex(vertex):
			self.vertices[vertex.key] = vertex
			self.adjacencies[vertex.key] = []
			return True
		else:
			print "Vertex already exists"
			return False

	def delVertex(self, vertex):
		if self.isVertex(vertex):
			self.vertices.pop(vertex.key)
			self.adjacencies.pop(vertex.key)

			#Now I must delete all adjacencies references to the vertex
			for lin in self.adjacencies.values():
				try:
					l.remove(vertex)
				except ValueError:
					#DoNothing
				 	continue

	def getAllVertex(self):
		#Returns all the keys
		return self.vertices.values()

	def getAllNeighbours(self,vertex):
		#Returns list containing all the neighbours of the vertex
		if self.isVertex(vertex):
			return self.adjacencies[vertex.key]
		else:
			print "vertex not in grahp"
			return False

	def addAdjacency(self, vertex, adj):
		#Checks if it isnt already a adjacency.
		a = self.vertices[adj.key]
		if a not in self.adjacencies[vertex.key]:
			self.adjacencies[vertex.key].append(a)
			return True
		else:
			return False

	def addEdge(self, vertex1, vertex2):
		#First checks if there is vertex exists
		if (self.isVertex(vertex1) and self.isVertex(vertex2)):
			#As the intended graph is undirected, A>B and B>A should be made.
			self.addAdjacency(vertex1,vertex2)
			self.addAdjacency(vertex2,vertex1)
			return True
		else:
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


	def idfs(self):
		count = 0
		heap = []
		l=[]
		sets=[]
		#Will start on the first vertex
		v=self.getAllVertex()[0]
		v.visit()
		l.append(a)
		for a in self.adjacencies[v.key]:
			heap.append(a)
		while not len(heap)==0:
			t = heap.pop()
			if not t.isVisited():
				t.visit()
				for a in self.adjacencies[t.key]:
					heap.append(a)

	def rdfs(self):
		
		for vert in self.getAllVertex():
			if not vert.isVisited():
				self.dfsvisit(vert)
				l.append(vert.key)

	def dfsvisit(self,vert):
		vert.visit()
		for vecino in self.adjacencies[vert.key]:
			if not vecino.isVisited():
				self.dfsvisit(vecino)