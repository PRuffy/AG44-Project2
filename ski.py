import networkx as nx
import array 
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

		"""Creation of all node"""
		while tempParcoursData <= self.numberOfVertices:
			#Creating a node
			self.domain.add_node(tempParcoursData)
			#Creating the primary attributes of the node
			self.domain.node[tempParcoursData]['Number'] = int(data[tempParcoursData][0]) #This attribus is maybe useless. To remove if so.
			self.domain.node[tempParcoursData]['Name'] = data[tempParcoursData][1]
			self.domain.node[tempParcoursData]['Altitude'] = int (data[tempParcoursData][2])
			self.domain.node[tempParcoursData]['Discovered'] = False
			#Creating two empty list of neighbours and leaving edge
			self.domain.node[tempParcoursData]['Neighbours'] = []
			self.domain.node[tempParcoursData]['LeavingEdge'] = []
			self.domain.node[tempParcoursData]['PreviousNode'] = 0
			self.domain.node[tempParcoursData]['DistParcouru'] = 0
			tempParcoursData += 1

		tempParcoursData+=1

		tempDepartureNode = 0
		tempArrivalNode = 0
		tempEdgeNumber = 0

		"""Creation of the edge and add some properties to the node"""
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
			self.domain.edge[tempDepartureNode][tempArrivalNode]['Number' == tempEdgeNumber]['Usable'] = True
			self.domain.node[tempDepartureNode]['Neighbours'].append(tempArrivalNode)
			self.domain.node[tempDepartureNode]['LeavingEdge'].append(tempEdgeNumber)

			tempParcoursData += 1


	"""The function set the attributes usable of the edge to true or false depending on the level asked by the skier"""
	def setUsableEdge(self, level):
		departureNode = 0
		arrivalNode = 0
		edgeNumber = 0
		edgeType  = ''
		numberOfNeighbours = 0

		if level == 'N':
			for departureNode in self.domain.nodes():
				numberOfNeighbours = len(self.domain.node[departureNode]['Neighbours'])

				for arrayTraversal in range(0,numberOfNeighbours-1):
					arrivalNode = self.domain.node[departureNode]['Neighbours'][arrayTraversal]
					edgeNumber = self.domain.node[departureNode]['LeavingEdge'][arrayTraversal]
					self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = True

					
		
		if level == 'R':
			for departureNode in self.domain.nodes():
				numberOfNeighbours = len(self.domain.node[departureNode]['Neighbours'])

				for arrayTraversal in range(0,numberOfNeighbours-1):
					arrivalNode = self.domain.node[departureNode]['Neighbours'][arrayTraversal]
					edgeNumber = self.domain.node[departureNode]['LeavingEdge'][arrayTraversal]
					edgeType = self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Type']

					if edgeType == 'N':
						self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = False
					else:
						self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = True
						
			
		if level == 'B':
			for departureNode in self.domain.nodes():
				numberOfNeighbours = len(self.domain.node[departureNode]['Neighbours'])

				for arrayTraversal in range(0,numberOfNeighbours-1):
					arrivalNode = self.domain.node[departureNode]['Neighbours'][arrayTraversal]
					edgeNumber = self.domain.node[departureNode]['LeavingEdge'][arrayTraversal]
					edgeType = self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Type']

					if edgeType == 'N':
						self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = False
					else:
						if edgeType == 'R':
							self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = False
						else:
							self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = True
						
		if level == 'V':
			for departureNode in self.domain.nodes():
				numberOfNeighbours = len(self.domain.node[departureNode]['Neighbours'])

				for arrayTraversal in range(0,numberOfNeighbours-1):
					arrivalNode = self.domain.node[departureNode]['Neighbours'][arrayTraversal]
					edgeNumber = self.domain.node[departureNode]['LeavingEdge'][arrayTraversal]
					edgeType = self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Type']

					if edgeType == 'N' :
						self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = False
					else:
						if edgeType == 'R':
							self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = False
						else:
							if edgeType == 'B':
								self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = False
							else:
								self.domain.edge[departureNode][arrivalNode]['edgeNumber' == edgeNumber]['Usable'] = True

		return self.domain


	def dijkstra(self, departureNode, arrivalNode, level):
		domainCopy = nx.MultiDiGraph()
		domainCopy = self.setUsableEdge(level)

		def minimum(stack, domainCopy):
			minimalValue = 500
			nodereturn = stack[0]
			for nodeBCL in domainCopy.nodes():
				if nodeBCL in stack:
					if domainCopy.node[nodeBCL]['DistParcouru'] != -1 and minimalValue > domainCopy.node[nodeBCL]['DistParcouru']:
						nodereturn = nodeBCL
							
			return nodereturn


		for nodeBCL in domainCopy.nodes():
			domainCopy.node[nodeBCL]['DistParcouru'] = -1
			domainCopy.node[nodeBCL]['PreviousNode'] = 0

		domainCopy.node[departureNode]['DistParcouru'] = 0

		notSeen = []
		for i in range(1, self.numberOfVertices):
			notSeen.append(i)

		"""We pass in every node to check the minimum path to it's neighbours"""
		while notSeen != []:
			
			tempNode1 = minimum(notSeen, domainCopy)
			notSeen.remove(tempNode1)
			
			arrayTraversal = len(domainCopy.node[tempNode1]['Neighbours'])
			
			"""We check every neighbours of the node we're actually visiting"""
			for arrayCase in range (0,arrayTraversal-1):

				tempNode2 = domainCopy.node[tempNode1]['Neighbours'][arrayCase]
				tempEdgeNumber = domainCopy.node[tempNode1]['LeavingEdge'][arrayCase]
				edgeUsability = domainCopy.edge[tempNode1][tempNode2]['edgeNumber' == tempEdgeNumber]['Usable']
				
				"""If the edge is usable then we can modify the value of the neighbours"""
				if edgeUsability == True:
					
					"""We check if the node value is -1 or if the actual value is greater than the one it will have by coming form the arrival node
				   	If so we change the premvious node of the neighbours"""
					if domainCopy.node[tempNode2]['DistParcouru'] == -1:
						domainCopy.node[tempNode2]['DistParcouru'] = domainCopy.node[tempNode1]['DistParcouru']+domainCopy.edge[tempNode1][tempNode2]['edgeNumber' == tempEdgeNumber]['Time']+1
						domainCopy.node[tempNode2]['PreviousNode'] = tempNode1
					
					else:
						if domainCopy.node[tempNode2]['DistParcouru'] > domainCopy.node[tempNode1]['DistParcouru'] + domainCopy.edge[tempNode1][tempNode2]['edgeNumber' == tempEdgeNumber]['Time']:
							domainCopy.node[tempNode2]['DistParcouru'] = domainCopy.node[tempNode1]['DistParcouru']+domainCopy.edge[tempNode1][tempNode2]['edgeNumber' == tempEdgeNumber]['Time']
							domainCopy.node[tempNode2]['PreviousNode'] = tempNode1
				
		"""Starting from the arrivalNode we get the path by reading all the previous node until we find the departureNode"""		
		path = []
		tempNode = arrivalNode

		while tempNode != departureNode:
			print domainCopy.node[tempNode]
			path.append(tempNode)
			if domainCopy.node[tempNode]['PreviousNode']:
				tempNode = domainCopy.node[tempNode]['PreviousNode']
			else:
				break

		path.append(departureNode)
		path.reverse()

		print("Shortest path : "),
		print path
		print("Time needed in seconds :"),
		print domainCopy.node[arrivalNode]['DistParcouru']	


			
	def DFS(self,departureNode,level):
		for node in self.domain.nodes():
			self.domain.node[node]['Discovered'] = False


		domainCopy = self.setUsableEdge(level)
		tempStack = []
		accesibleNode = []
		tempStack.append(departureNode)
		tempNode = departureNode

		while tempStack != []:

			tempNode = tempStack.pop()

			if domainCopy.node[tempNode]['Discovered'] == False:

				domainCopy.node[tempNode]['Discovered'] = True
				accesibleNode.append(tempNode)

				
				while domainCopy.node[tempNode]['Neighbours'] != []:

					tempArrivalNode = domainCopy.node[tempNode]['Neighbours'].pop(0)
					tempEdgeNumber = domainCopy.node[tempNode]['LeavingEdge'].pop(0)

					if domainCopy.edge[tempNode][tempArrivalNode]['edgeNumber' == tempEdgeNumber]['Usable'] == True:
						tempStack.append(tempArrivalNode)

		print("Accesible nodes :"),
		print accesibleNode
