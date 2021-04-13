import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import process


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
	print("3. search county")
	inp = input("Select Option 0-3: ")


	while(1):
		if(inp == "0"):
			dispMap(0)
			break
		elif(inp == "1"):
			dispMap(1)
			break	
		elif(inp == "2"):
			print("z")
			break
		elif(inp == "3"):
			print("s")
			break
		else:
			inp = ""
			inp = input("Select Option 0-3: ")




showMenu()
#﷽