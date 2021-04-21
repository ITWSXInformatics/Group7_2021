from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import process_json as pj
import pandas as pd
import geopandas as gpd


def getState():
	usa = gpd.read_file('./map/counties/UScounties.shp')
	
	state = input("Enter state name: ")
	state = state.lower().capitalize()
	
	stateMap = usa[usa['state_name'] == state]
	
	if(stateMap.empty):
		print("State not found")
		return

	stateData = pj.ranking([state])
	df = pd.DataFrame.from_dict(data = stateData)
	print(df)

	merged = stateMap.set_index('state_name').join(df.set_index("name"))
	

	merged.plot(column = "Rank")
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
	
	states = open('Data/state_name.txt');
	stateNames = states.read()
	nameArray = stateNames.split("\n");

	dataArr = pj.ranking(nameArray)
	covidData = pd.DataFrame(dataArr)
	#print(covidData)

	if mapType == 1:
		usa = gpd.read_file('./map/counties/UScounties.shp')
		covidData.rename(columns = {'name': 'state_name'}, inplace=True)
		merged = usa.merge(covidData, on='state_name')

	elif mapType == 0:
		usa = gpd.read_file('./map/states/States_shapefile.shp')
		
		#print(usa)
		covidData["name"] = covidData["name"].str.upper()
		covidData.rename(columns = {'name': 'State_Name'}, inplace=True)
		merged = usa.merge(covidData, on='State_Name')

	#print(merged["Rank"])
	#merged.head()

	#df2 = merged[merged.applymap(lambda x: x[0] if isinstance(x, list) else x).duplicated('State_Name')]
	fig, ax = plt.subplots(1, figsize=(10, 6))
	ax.axis('off')
	ax.set_title("Vaccine Index Ranking")

	merged.plot(column="Rank", ax=ax, legend = True)
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
		else:
			inp = input("Select Option 0-2: ")	
		"""
		elif(inp == "﷽"):
		
			getCounty()
			break
		"""
		


showMenu()
