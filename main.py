import os
from ski import *

def getGraphData():
	data=[]
	
	with open("./dataski.txt","r") as ski_file:
		skiData=ski_file.read()	#read the file

		lignes=skiData.split("\n") #parse line by line

		for case in lignes:	#parse each line
			elem=case.split("	")
			data.append(elem)

	ski_file.close()
	
	return(data)

		
if __name__ == "__main__":

	domainData = getGraphData()
	
	Graph = skiDomain()
	Graph.createGraph(domainData)
	Graph.dijkstra(3,1,'N')
	#Graph.DFS(6,'V')
	