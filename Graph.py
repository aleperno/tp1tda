"""Graph.py
Description: simple & undirected graph implementation for course 75.29 Teoria de
Algoritmos @ University of Buenos Aires

Authors:
Medrano, Lautaro
Pernin, Alejandro
"""

#NotUsed
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

		self.res = []

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

	def printResult(self):
		count = 1
		for line in self.res:
			print "Arista%s: %s" % (count,line)
			count += 1
		if count == 1:
			#There were no results
			print "Ya se cumple la robustez requerida"

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
			self.adjacencies[vertex.key] = {} #O(1)
			return True
		else:
			return False

	#NotUsed
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
		#Returns all the vertices
		return self.vertices.values()

	#O(1)
	def getAllNeighbours(self, vertex):
		#Returns list containing all the neighbours keys of the vertex
		if self.isVertex(vertex): #O(1)
			return self.adjacencies[vertex.key].keys() #O(1)
		else:
			print "vertex not in grahp"
			return False

	#O(1)
	def addAdjacency(self, vertex, adj):
		#Checks if it isnt already a adjacency.
		a = self.vertices[adj.key] #O(1)
		if not self.adjacencies[vertex.key].has_key(a.key): #O(1)
			self.adjacencies[vertex.key][a.key]=None #O(1)
			return True
		else:
			return False

	#O(1)
	def isEdge(self,vertex1,vertex2):
		#print "Chequeando adyacencia entre %s y %s" % (vertex1,vertex2)
		if self.adjacencies[vertex2.key].has_key(vertex1.key): #O(1)
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

	#O(1) NOT USED
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
		for key_vecino in self.getAllNeighbours(vert): #O(E)
			vecino = self.vertices[key_vecino]
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
	#O(cant)
	def addEdgesSets(self,laux,cant):
		for i in range(cant):
			try:
				v1 = laux[i][0]
				v2 = laux[i][1]
				self.addEdge(v1,v2)
				s = "%s , %s" % (v1.key , v2.key)
				self.res.append(s)
			except IndexError:
				#There are no more available edges to add
				return

	#O(cant)
	def addEdgesVertex(self,vertex,cant):
		for i in self.getAllVertex():
			if not cant:
				#No edges to add
				return
			if i == vertex :
				continue
			elif not self.isEdge(vertex,i):
				self.addEdge(vertex,i)
				s = "%s , %s" % (vertex.key , i.key)
				self.res.append(s)
				cant -= 1

	#O(|set1|*|set2|)
	def edgesInSets(self,set1,set2,laux):
		count=0
		for i in set1:
			for j in set2:
				if self.isEdge(i,j):
					count +=1
				else:
					#Saves the no-edges to be used if more edges are required
					laux.append((i,j)) #O(1)
		return count

	"""O(V^2)+O(V^2) = O(V^2) """
	def setStrenght(self,svalue):
		cant = len(self.comp)
		res = 0
		aux = {}
		#First analyze the strength from the set point of view (see report)
		"""
		The worst case in terms of sets quantities is the best case in terms of sets size and
		vice versa. The annlysis of each case resulted that each wors case has a O(V^2) running time.
		quant * {quant * (size * size) + (size * (V-size))}
		-Worst case in terms of quant, is when having the most ammount of loops, each loop has a 
		minimum size of 3 vertices so, at most i'll have V/3 loops of size 3.
		V/3 * {V/3 * (3 * 3) + (3 * V-3)} 
		Applying O() properties, the running time is O(V^2)
		-Worst case in terms of size, is when having two loops, each with half of the vertices.
		2 * {2  (V/2 * V/2) + (V/2 * V/2)}
		Applying O() properties, the running time is O(V^2)
		"""
		for li in self.comp: #Depends on sets quantity, O(|self.comp|)
			cont = 0
			laux = []
			for lj in self.comp: # Depends on sets quantity, O(|self.comp|)
				#See how many edges to other sets there are
				if li==lj:
					continue
				else:
					cont += self.edgesInSets(li,lj,laux)#Depends on sets size,O(|li|*|lj|)
			if cont < svalue:
				#The set has less edges to other sets than the required strength
				cant = svalue - cont #The required ammount of edges to be added to comply the requirements
				self.addEdgesSets(laux,cant) #Worst case O(|li|*V-|li|), for each vertex, add edge to all other vertex

		"""Upper bound O(V^2)"""
		#Now analize the strenght from the vertex point of view:
		for vertex in self.getAllVertex(): #O(V)
			ncount = len(self.getAllNeighbours(vertex)) #O(1)
			if (ncount < svalue):
				#The vertex has less neighbours than the required strength
				cant = svalue - ncount #Ammount of edges to be added
				self.addEdgesVertex(vertex,cant) #Worst case O(V-1) if i have to complete the graph 