# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

from operator import itemgetter

class Node(object):
	def __init__(self, action, name, parent, distance, outdoor):
		self.action = action
		self.name = name
		self.parent = parent
		if self.parent == None:
			self.distance = 0
			self.outdoor = 0
		else:
			self.distance = parent.distance + distance
			self.outdoor = parent.outdoor + outdoor
	def path(self):
		if self.parent == None:
			return[(self.action, self.name)]
		else:
			return self.parent.path() + [(self.action, self.name)]		
	def inPath(self, s):
		if s == self.name:
			return True
		elif self.parent == None:
			return False
		else:
			return self.parent.inPath(s)
	def getName(self):
		return self.name
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name
	# def __eq__(self, other):
		# return self.name == other.name
	# def __ne__(self, other):
		# return not self.__eq__(other)

class Edge(object):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
	def getSource(self):
		return self.src
	def getDestination(self):
		return self.dest
	def __str__(self):
		return str(self.src) + '->' + str(self.dest)

class Digraph(object):
	"""
	A directed graph
	"""
	def __init__(self):
		self.nodes = set([])
		self.edges = {}
	def addNode(self, node):
		if node in self.nodes:
			raise ValueError('Duplicate node')
		else:
			self.nodes.add(node)
			self.edges[node] = []
	def addEdge(self, edge):
		src = edge.getSource()
		dest = edge.getDestination()
		if not(src in self.nodes and dest in self.nodes):
			raise ValueError('Node not in graph')
		self.edges[src].append(dest)
	def childrenOf(self, node):
		return self.edges[node]
	def hasNode(self, node):
		return node in self.nodes
	def __str__(self):
		res = ''
		for k in self.edges:
			for d in self.edges[k]:
				res = res + str(k) + '->' + str(d) + '\n'
		return res[:-1]

class PriorityQueue(object):
	"""
	Object that queues elements/nodes for expansion
	a pattern for entry is a tuple in the form: (distance, outdoor, node)
	it return the node with the lowest distance as first search key
	and lowest outdoor as second search key if distance is equal in nodes
	"""
	def __init__(self):
		self.data = []
	def push(self, item):
		self.data.append(item)
	def pop(self):
		self.data.sort(key = itemgetter(0, 1))
		return self.data.pop(0)
	def isEmpty(self):
		return self.data == []

#test:		
# pq = PriorityQueue()
# t1 = (1, 3, 'S')
# t2 = (2, 4, 'T')
# t3 = (2, 1, 'R')
# lst = [t1, t2, t3]
# for elem in lst:
	# pq.push(elem)
# print pq.data
# print pq.pop()
