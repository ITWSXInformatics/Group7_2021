import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
#import "process.py"


mapType = ""
while (mapType != "state" and mapType != "county"):
	mapType = input("State or County view? ")


if mapType == "county":
	usa = gpd.read_file('./map/counties/UScounties.shp')
elif mapType == "state":
	usa = gpd.read_file('./map/states/States_shapefile.shp')


usa.plot()
plt.show()
