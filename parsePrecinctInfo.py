from pandas import read_csv
from flask import Flask
import json

app = Flask(__name__)


df = read_csv('nypp.csv', header=0)[['Precinct', 'the_geom']]
prec_map ={}
for ind, row in df.iterrows():
    prec_map[row['Precinct']] =  row['the_geom']


json.dumps([{'precinct': key, 'polygons': value} for key, value in prec_map.items()])

