'''
Cette carte de la Bretagne a ete creer pour Maman / Anne pour noel 2017. 

CARTOGRAPY: Un programme pour generer des jolies cartes avec python2. Ecrit par Robyn et Lucas.

!! D'abord!! Fait attention a changer le fichier de travail pour tout creer dans le bon fichier!

Pour plus de details sur les types de routes, etc...:
    http://wiki.openstreetmap.org/wiki/Map_Features
'''
import overpy
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import fiona
from fiona.crs import from_epsg
from geopy.geocoders import Nominatim
import os
import shutil

home_dir = os.getcwd()
wd_output = os.path.join(home_dir, 'cartograpy', 'bretagne', 'output')
wd_files = os.path.join(home_dir, 'cartograpy', 'bretagne', 'shapefiles')
if not os.path.exists(wd_output):
    os.makedirs(wd_output)
if not os.path.exists(wd_files):
    os.makedirs(wd_files)
os.chdir(wd_files)

# Inserer les coordonees de la Bretagne
north = 49.038 + 0.03
east = -0.890
west = -5.202 - 0.05
south = 46.90437

# Telecharger les donnees de "openstreetmap", si elles n'existent pas encore.
'''Pseudocode:
if len(os.list files or whatever) < 1:
    do the following until '#Dessine la carte\' section
'''
api = overpy.Overpass()
q1 = 'way(' + str(south) + ',' + str(west) + ',' + \
    str(north) + ',' + str(east) + ') ['
q2 = '"];(._;>;);out body;'

trunk = api.query(q1 + '"highway"="trunk' + q2)
motorway = api.query(q1 + '"highway"="motorway' + q2)
primary = api.query(q1 + '"highway"="primary' + q2)
secondary = api.query(q1 + '"highway"="secondary' + q2)
trunk_link = api.query(q1 + '"highway"="trunk_link' + q2)
motorway_link = api.query(q1 + '"highway"="motorway_link' + q2)
primary_link = api.query(q1 + '"highway"="primary_link' + q2)
secondary_link = api.query(q1 + '"highway"="secondary_link' + q2)

# Ecrire les donnees dans trois Shapefiles
schema = {'geometry': 'LineString', 'properties': {
    'Name': 'str:80', 'Type': 'str:80'}}
shapeout = "bretagne_highway.shp"
with fiona.open(shapeout, 'w',
                crs=from_epsg(4326),
                driver='ESRI Shapefile',
                schema=schema) as output:
    for result in [trunk, motorway, primary]:
        for way in result.ways:
            line = {'type': 'LineString', 'coordinates': [
                (node.lon, node.lat) for node in way.nodes]}
            prop = {'Name': way.tags.get(
                "name", "n/a"), 'Type': way.tags.get("highway", "n/a")}
            output.write({'geometry': line, 'properties': prop})

shapeout = "bretagne_road.shp"
with fiona.open(shapeout, 'w',
                crs=from_epsg(4326),
                driver='ESRI Shapefile',
                schema=schema) as output:
    for result in [secondary, secondary_link]:
        for way in result.ways:
            line = {'type': 'LineString', 'coordinates': [
                (node.lon, node.lat) for node in way.nodes]}
            prop = {'Name': way.tags.get(
                "name", "n/a"), 'Type': way.tags.get("highway", "n/a")}
            output.write({'geometry': line, 'properties': prop})

shapeout = "bretagne_links.shp"
with fiona.open(shapeout, 'w',
                crs=from_epsg(4326),
                driver='ESRI Shapefile',
                schema=schema) as output:
    for result in [trunk_link, motorway_link, primary_link]:
        for way in result.ways:
            # the shapefile geometry use (lon,lat)
            line = {'type': 'LineString', 'coordinates': [
                (node.lon, node.lat) for node in way.nodes]}
            prop = {'Name': way.tags.get(
                "name", "n/a"), 'Type': way.tags.get("highway", "n/a")}
            output.write({'geometry': line, 'properties': prop})

# Dessine la carte
m = Basemap(projection='tmerc', resolution='f',
            llcrnrlon=west, llcrnrlat=south,
            urcrnrlon=east, urcrnrlat=north,
            lon_0=(east + west) / 2, lat_0=(north + south) / 2)

plt.close()
fig = plt.figure(figsize=(24.25, 18.25), dpi=300)
rect = [0.015, 0.033, 0.97, 0.934]
ax = fig.add_axes(rect)
m.drawmapboundary(fill_color='#E1E1E1', linewidth=0)
m.drawcoastlines(linewidth=0.5, color="#E1E1E1")
m.fillcontinents(color="#FFFFFF")
m.readshapefile('bretagne_road', 'roads',
                linewidth=0.45, color="#A0A0A0")
m.readshapefile('bretagne_highway', 'highway',
                linewidth=0.6, color="#202020")
m.readshapefile('bretagne_links', 'highway',
                linewidth=0.3, color="#202020")
fig.savefig(os.path.join(wd_output, 'bretagne.pdf'), dpi=300)
# fig.savefig(os.path.join(wd_output, 'bretagne.eps'), dpi=300)
