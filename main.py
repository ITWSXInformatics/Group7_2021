import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import process_json


def getState():
	usa = gpd.read_file('./map/counties/UScounties.shp')
	state = input("Enter state name: ")
	state = state.lower().capitalize()
	stateMap = usa[usa['state_name'] == state]
	if(stateMap.empty):
		print("State not found")
	else:
		stateMap.plot()
		plt.show()

"""
def getCounty():
	usa = gpd.read_file('./map/counties/UScounties.shp')
	county = input("Enter county name: ")
	county = county.lower().capitalize()

	#needs state as well cuz some counties are in multiple states
	state = input("Enter state name: ")
	state = state.lower().capitalize()

	countyMap = usa[usa['name'] == county]
	countyMap = countyMap[countyMap["state_name"] == state]
	if(countyMap.empty):
		print("County not found")
	else:
		countyMap.plot()
		plt.show()
"""
def dispMap(mapType):
	if mapType == 0:
		usa = gpd.read_file('./map/counties/UScounties.shp')
	elif mapType == 1:
		usa = gpd.read_file('./map/states/States_shapefile.shp')
	usa.plot()
	plt.show()
	

def showMenu():
	print("Menu:")
	print("0. State level view")
	print("1. County level view")
	print("2. search state")
	inp = input("Select Option 0-2: ")


	while(1):
		if(inp == "0"):
			dispMap(0)
			break
		elif(inp == "1"):
			dispMap(1)
			break	
		elif(inp == "2"):
			getState()
			break
		"""
		elif(inp == "﷽"):
		
			getCounty()
			break
		"""
		else:
			inp = input("Select Option 0-3: ")

showMenu()
