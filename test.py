#!/usr/bin/python
import sys
from Graph import *

def usage():
	print "Usage: python test.py <filename>"
	print "Usage: ./test.py <filename>"

def loadGraph():
	graph = Graph()
	try:
		aux = open(sys.argv[1])
		for line in aux:
			line = line.replace(':',',').replace('\n','').split(',')
			print line
			print line[0]
			v1 = Vertex(line[0])
			graph.addVertex(v1)
			for n in range(1,len(line)):
				v2 = Vertex(line[n])
				print line[n]
				if (not graph.isVertex(v2)):
					graph.addVertex(v2)
				e = Edge(v1,v2)
				graph.addEdge(e)
		return graph

	except KeyError:
		print "An error has occurred"
	except IndexError:
		usage()
	except IOError:
		print "Verify parameters"
	exit
	print "wachooo"


def main():
	g = loadGraph()
	print g
"""
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
"""
if __name__ == '__main__':
	main()