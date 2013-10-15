"""Graph.py
Description: simple & undirected graph implementation for course 75.29 Teoria de
Algoritmos @ University of Buenos Aires

Authors:
Medrano, Lautaro
Pernin, Alejandro
"""


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

		#To be used on DFS
		self.father = None
		self.visited = False

	def __eq__(self,other):
		return self.key == other.key

	def __str__(self):
		return self.key

	def isVisited(self):
		return self.visited

	def visit(self,father):
		if not father:
			f=''
		else:
			f= father.key
		#print "Visitando %s desde %s" % (self.key, f)
		self.visited=True
		self.father=father

class Graph:

	def __init__(self):
		#Standalone initialization
		self.vertices = {}
		self.adjacencies = {}

		self.comp = []

	def __str__(self):
		#Prints graph as 'vertex: [edges]'
		s = ''
		for v in self.vertices.keys():
			#First character on the line is the vertex
			s += "%s: " % v
			for a in self.adjacencies[v]:
				s += "%s," % a
			s += "\n"
		return s

		#O(1)
	def countVertices(self):
		return len(self.getAllVertex())

		#O(1)
	def isVertex(self, vertex):
		return self.vertices.has_key(vertex.key)

		#O(1)
	def addVertex(self, vertex):
		if not self.isVertex(vertex): #O(1)
			self.vertices[vertex.key] = vertex #O(1)
			self.adjacencies[vertex.key] = []  #O(1)
			return True
		else:
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

		#O(1)
	def getAllVertex(self):
		#Returns all the keys
		return self.vertices.values()

		#O(1)
	def getAllNeighbours(self, vertex):
		#Returns list containing all the neighbours of the vertex
		if self.isVertex(vertex): #O(1)
			return self.adjacencies[vertex.key] #O(1)
		else:
			print "vertex not in grahp"
			return False

		#O(1)
	def addAdjacency(self, vertex, adj):
		#Checks if it isnt already a adjacency.
		a = self.vertices[adj.key] #O(1)
		if a not in self.adjacencies[vertex.key]: #O(1)
			self.adjacencies[vertex.key].append(a) #O(1)
			return True
		else:
			return False

		#O(1)
	def isEdge(self,vertex1,vertex2):
		print "Chequeando adyacencia entre %s y %s" % (vertex1,vertex2)
		if vertex1 in self.getAllNeighbours(vertex2):
			return True
		else:
			return False

		#O(1)
	def addEdge(self, vertex1, vertex2):
		#First checks if there is vertex exists
		if (self.isVertex(vertex1) and self.isVertex(vertex2)): #O(1) 
			#As the intended graph is undirected, A>B and B>A should be made.
			self.addAdjacency(vertex1,vertex2) #O(1)
			self.addAdjacency(vertex2,vertex1) #O(1)
			return True
		else:
			return False

		#O(1)
	def delEdge(self, vertex1, vertex2):
		#As it is undirected, both references must be deleted
		try:
			self.graph[vertex2.value].pop(vertex1.value) #O(1)
			self.graph[vertex1.value].pop(vertex2.value) #O(1) 
			return True
		except KeyError:
			#Either vertex not in graph or no edge
			print "Error while deleting edge"
			return False

	"""
	The common DFS running time is O(V+E) V:Vertices, E:Edges. ('Introduction to Algorithms' Second Edition -
	Thomas Cormen page 543).
	As I add a cycle over the list 'l', hence I only add a element when a vertex is being visited,
	every call to the cycle will empty the list	and the operations inside the cycle are O(1) at the
	whole DFS this cycle will add O(V).
	Summing
	O(V+E) + O(V) = O(V+V+E) = O(2V+E) = O(2V) + O(E) = 2O(V) + O(E) = O(V) + O(E) = O(V+E)
	[O(kg)=O(g) if k is constant and nonzero]
	"""
	def rdfs(self):
		l=[]	
		for vert in self.getAllVertex(): #O(V)
			if not vert.isVisited():
				self.dfsvisit(None,vert,l)

	def dfsvisit(self,father,vert,l):
		vert.visit(father) #O(1)
		l.append(vert) #O(1)

		"""At most I will go through every edge"""
		for vecino in self.adjacencies[vert.key]: #O(E)
			if not vecino.isVisited():
				self.dfsvisit(vert,vecino,l)
			elif (vert.father != None) and (vert.father != vecino): #O(1)
				"""If the vertex's neighbour im trying to visit is already visited
				and it is not the vertex's father, It means there I have reached a loop.
				So I proceed to save the loop 
				"""
				aux = []

				"""As the only time a element is included in the list is when visited,
				at most the list will include all the vertices"""
				while len(l)>0: #O(V)
					v = l.pop() #O(1)
					aux.append(v) #O(1)
					if v.key == vecino.key: #O(1)
						break
				if aux:
					self.comp.append(aux) #O(1)

	def edgesInSets(self,set1,set2):
		count=0
		for i in set1:
			for j in set2:
				if self.isEdge(i,j):
					count +=1
		return count

	def calcStrenght(self):
		cant = len(self.comp)
		res = 0
		aux = {}
		
		for li in self.comp:
			cont = 0
			for lj in self.comp:
				if li==lj:
					continue
				else:
					cont += self.edgesInSets(li,lj)
			if not res or cont < res:
				res = cont
		return res

