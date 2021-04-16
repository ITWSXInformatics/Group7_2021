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

#def getCounty():
#	county = input("Enter county name: ")


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
		#elif(inp == "3"):
		#	getCounty()
		#	break
		else:
			inp = input("Select Option 0-3: ")

showMenu()
#﷽