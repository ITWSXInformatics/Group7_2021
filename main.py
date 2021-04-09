import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

usa = gpd.read_file('./map/UScounties.shp')

usa.plot()
plt.show()