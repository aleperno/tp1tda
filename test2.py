#!/usr/bin/python
"""Prueba cargar un grafo desde un archivo y lo imprime"""

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
			v1 = Vertex(line[0])
			graph.addVertex(v1)
			for n in range(1,len(line)):
				v2 = Vertex(line[n])
				if (not graph.isVertex(v2)):
					graph.addVertex(v2)
				graph.addEdge(v1,v2)
		return graph

	except KeyError:
		print "An error has occurred"
	except IndexError:
		usage()
	except IOError:
		print "Verify parameters"
	return False

def main():
	g = loadGraph()
	if not g:
		return
	print g
	print "probando dfs\n"
	g.rdfs()
	print g.comp

if __name__ == '__main__':
	main()