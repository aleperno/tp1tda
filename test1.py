#!/usr/bin/python
import sys
from Graph import *

def main():
	v1 = Vertex('A')
	v2 = Vertex('B')
	v3 = Vertex('C')
	e1 = Edge(v1,v3)
	e = Edge(v1,v2)
	print e
	g = Graph()
	g.addVertex(v1)
	g.addVertex(v2)
	g.addVertex(v3)
	print g.addEdge(e)
	print g.addEdge(e1)
	print g
	print "Will try to delete edge"
	print g.delEdge(v1,v2)
	print g
	v4 = Vertex('A')
	g.delVertex(v4)
	print g

if __name__ == '__main__':
	main()