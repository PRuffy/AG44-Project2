import networkx as nx

class skiDomain(object):
	"""docstring for skiDomain"""
	def __init__(self):
		numberOfEdge =0
		numberOfVertices = 0
		domain = nx.MultiDiGraph()
	

	"""That function read the data obtain by the function getgraphData in the main"""
	"""It create the graph starting by the node then the edge"""

	def createGraph(self, data):
		self.numberOfVertices = int(data[0][0])
		self.numberOfEdge = int(data[self.numberOfVertices+1][0])
		self.domain = nx.MultiDiGraph()

		#timeOfParcours return the time in second
		def timeOfParcours(departure,arrival,edgeNumber):
			def busEdge():
				if self.domain.node[departure]['Name'] == "arc2000" or self.domain.node[arrival]['Name'] == "arc2000":
					return 40*60
				else:
					return 30*60
			return{
				'TK' : (1+(4*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'TS' : (1+(4*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'TSD' : (1+(3*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'TC' : (2+(3*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'TPH' : (4+(2*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'BUS' : busEdge(),
				'V' : ((5*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'B' : ((4*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'R' : ((3*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'N' : ((2*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
				'KL' : (10*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100,
				'SURF' :((10*self.domain.edge[departure][arrival]['Number' == edgeNumber]['length'])/100)*60,
			}[self.domain.edge[departure][arrival]['Number' == edgeNumber]['Type']]
		tempParcoursData = 1

		while tempParcoursData <= self.numberOfVertices:
			#Creating a node
			self.domain.add_node(tempParcoursData)
			#Creating the primary attributes of the node
			self.domain.node[tempParcoursData]['Numnber'] = int(data[tempParcoursData][0]) #This attribus is maybe useless. To remove if so.
			self.domain.node[tempParcoursData]['Name'] = data[tempParcoursData][1]
			self.domain.node[tempParcoursData]['Altitude'] = int (data[tempParcoursData][2])

			#Creating two empty list of neighbours and leaving edge
			self.domain.node[tempParcoursData]['Neighbours'] = []
			self.domain.node[tempParcoursData]['LeavingEdge'] = []
			tempParcoursData += 1

		tempParcoursData+=1

		tempDepartureNode = 0
		tempArrivalNode = 0
		tempEdgeNumber = 0

		while tempParcoursData <= self.numberOfEdge+self.numberOfVertices+1:

			tempEdgeNumber = int(data[tempParcoursData][0])
			tempDepartureNode = int(data[tempParcoursData][3])
			tempArrivalNode = int(data[tempParcoursData][4])

			self.domain.add_edge(tempDepartureNode,tempArrivalNode, Number = tempEdgeNumber)
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['Name'] = data[tempParcoursData][1]
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['Type'] = data[tempParcoursData][2]
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['edgeNumber'] = tempEdgeNumber

			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['DepartureNode'] = tempDepartureNode
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['ArrivalNode'] = tempArrivalNode
			#The length is given in meters
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['length'] = abs(self.domain.node[tempDepartureNode]['Altitude']-self.domain.node[tempArrivalNode]['Altitude'])
			#The time is given in second
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['Time'] = timeOfParcours(tempDepartureNode,tempArrivalNode,tempEdgeNumber)

			self.domain.node[tempArrivalNode]['Neighbours'].append(tempArrivalNode)
			self.domain.node[tempArrivalNode]['Neighbours'].append(tempEdgeNumber)

			tempParcoursData += 1

	"""That function create a copy of the graph and remove all the edge forbidden"""
	"""Then the copy is return"""
	"""We assume that the level is a simple character"""
	"""It give the level of the skier wich means it can only be V B R or N"""
	"""We also assume that every skilift can be used"""
	def modifyGraph(self, level):
		domainCopy = self.domain.copy()
		domainCopyReturn = self.domain.copy()

		if level == 'V':
			for depatureNode in range(1, self.numberOfVertices):
				parcoursNeighbours = 0
				while domainCopy.node[depatureNode]['LeavingEdge'] != []:
					edgeType = domainCopy.edge[depatureNode][domainCopy.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopy.node[depatureNode]['LeavingEdge'][parcoursNeighbours]]['Type']

					if edgeType == 'B' or edgeType == 'R' or edgeType == 'N':
						domainCopyReturn.remove_edge(domainCopyReturn.edge[depatureNode][domainCopyReturn.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopyReturn.node[depatureNode]['LeavingEdge'][parcoursNeighbours]])
						domainCopyReturn.node[depatureNode]['Neighbours'].pop(0)
						domainCopyReturn.node[depatureNode]['LeavingEdge'].pop(0)

					domainCopy.remove_edge(domainCopy.edge[depatureNode][domainCopy.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopy.node[depatureNode]['LeavingEdge'][parcoursNeighbours]])
					domainCopy.node[depatureNode]['Neighbours'].pop(0)
					domainCopy.node[depatureNode]['LeavingEdge'].pop(0)

		elif level == 'B':

			for depatureNode in range(1, self.numberOfVertices):
				parcoursNeighbours = 0
				while domainCopy.node[depatureNode]['LeavingEdge'] != []:
					edgeType = domainCopy.edge[depatureNode][domainCopy.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopy.node[depatureNode]['LeavingEdge'][parcoursNeighbours]]['Type']

					if edgeType == 'R' or edgeType == 'N':
						domainCopyReturn.remove_edge(domainCopyReturn.edge[depatureNode][domainCopyReturn.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopyReturn.node[depatureNode]['LeavingEdge'][parcoursNeighbours]])
						domainCopyReturn.node[depatureNode]['Neighbours'].pop(0)
						domainCopyReturn.node[depatureNode]['LeavingEdge'].pop(0)

					domainCopy.remove_edge(domainCopy.edge[depatureNode][domainCopy.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopy.node[depatureNode]['LeavingEdge'][parcoursNeighbours]])
					domainCopy.node[depatureNode]['Neighbours'].pop(0)
					domainCopy.node[depatureNode]['LeavingEdge'].pop(0)

		elif level == 'R':

			for depatureNode in range(1, self.numberOfVertices):
				parcoursNeighbours = 0
				while domainCopy.node[depatureNode]['LeavingEdge'] != []:
					edgeType = domainCopy.edge[depatureNode][domainCopy.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopy.node[depatureNode]['LeavingEdge'][parcoursNeighbours]]['Type']

					if edgeType == 'N':
						domainCopyReturn.remove_edge(domainCopyReturn.edge[depatureNode][domainCopyReturn.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopyReturn.node[depatureNode]['LeavingEdge'][parcoursNeighbours]])
						domainCopyReturn.node[depatureNode]['Neighbours'].pop(0)
						domainCopyReturn.node[depatureNode]['LeavingEdge'].pop(0)

					domainCopy.remove_edge(domainCopy.edge[depatureNode][domainCopy.node[depatureNode]['Neighbours'][parcoursNeighbours]]["edgeNumber" == domainCopy.node[depatureNode]['LeavingEdge'][parcoursNeighbours]])
					domainCopy.node[depatureNode]['Neighbours'].pop(0)
					domainCopy.node[depatureNode]['LeavingEdge'].pop(0)
		
		
		return domainCopyReturn


	def dijkstra(self, depatureNode, arrivalNode, level):
		domainCopy = self.modifyGraph(level)


		pass

	def DFS(self,depatureNode,level):
		for node in self.domain.nodes():
			self.domain.node[node]['Discovered'] = "False"


		domainCopy = self.modifyGraph(level)
		tempStack = []
		accesibleNode = []
		tempStack.push(depatureNode)
		tempNode = depatureNode


		while tempStack != []:
			tempStack.pop()
			if domainCopy.node[tempNode]['Discovered'] != "True":
				self.domain.node[tempNode]['Discovered'] != "True"
				accesibleNode.push(tempNode)
				for tempNeighbours in domainCopy.node[tempNode]['Neighbours']:
					tempStack.push(tempNeighbours)


		print (accesibleNode)
		