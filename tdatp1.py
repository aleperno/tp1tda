#!/usr/bin/python
"""Prueba cargar un grafo desde un archivo y lo imprime"""

import sys
from Graph import *

def usage():
	print "Usage: python test.py #strenght <filename>"
	print "Usage: ./test.py #strenght <filename>"

def checkConditions(graph,strenght):
	"""As the graph should be simple and connected, at the most
	the graph will have #V*(#V-1)/2 edges (complete graph case)
	"""
	v=graph.countVertices()
	print "El grafo tiene %s vertices" % v
	maximo = (v*(v-1)/2)
	if(int(strenght)>maximo):
		print "No es posible la robustez pedida"
		return False
	return True

def loadGraph():
	graph = Graph()
	try:
		aux = open(sys.argv[2])
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
		print "Verify parameters, input file does not exist"
	return False

def main():
	g = loadGraph()
	if not g:
		return
	print g
	robustez = sys.argv[1]
	print "Se requiere robustez %s" % robustez
	if checkConditions(g,robustez):
		print "probando dfs\n"
		g.rdfs()
		
		for i in g.comp:
			s = '['
			for j in i:
				s += "'%s'," % j.key
			s += "]\n"
			print s
	else:
		return

	print g.setStrenght(int(robustez))
	print "ahora a imprimir el resultado"
	g.printResult()

if __name__ == '__main__':
	main()