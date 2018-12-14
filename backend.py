from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import psycopg2
import pandas as pd
from geojson import Point, Feature, FeatureCollection
import json

MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoibWJyYW5kYWpza3kiLCJhIjoiY2pwM3MzeHdiMGw0dzNwcWkzam45dHc4dSJ9.8megQVVgaGmu-7ntpVFvvQ'
conn_string = "host='localhost' dbname='pdt_projekt' user='postgres' password='postgres'"

app = Flask(__name__)

def connectIntoPg():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return conn, cursor

def getPointsToGeoJSON(stations):
    features = list()
    columnsLength = len(stations)
    for i in range(columnsLength):
        pointProperties = {}
        pointProperties['title'] = stations['type'][i]
        features.append(Feature(geometry=Point((stations["lat"][i], stations["long"][i])), properties=pointProperties))
    feature_collection = FeatureCollection(features)
    return feature_collection


def near10Stations(lat, lon):
    conn, cursor = connectIntoPg()
    cursor.execute("""SELECT amenity, ST_X(way), ST_Y(way), 111.045 * DEGREES(ACOS(COS(RADIANS(""" + str(lat) + """))
        * COS(RADIANS(ST_Y(way)))
        * COS(RADIANS(ST_X(way)) - RADIANS(""" + str(lon) + """))
        + SIN(RADIANS(""" + str(lat) + """))
        * SIN(RADIANS(ST_Y(way)))))
        AS distance_in_km
        FROM planet_osm_point
        WHERE amenity = 'fuel' OR amenity = 'charging_station'
        UNION		
        SELECT amenity, ST_X(geo), ST_Y(geo), 111.045 * DEGREES(ACOS(COS(RADIANS(""" + str(lat) + """))
        * COS(RADIANS(ST_Y(geo)))
        * COS(RADIANS(ST_X(geo)) - RADIANS(""" + str(lon) + """))
        + SIN(RADIANS(""" + str(lat) + """))
        * SIN(RADIANS(ST_Y(geo)))))
        AS distance_in_km
        FROM stations
        ORDER BY distance_in_km ASC
        LIMIT 10;""")

    records = cursor.fetchall()
    stations = pd.DataFrame(records, columns=["type", "lat", "long", "distance"])
    geo = getPointsToGeoJSON(stations)
    cursor.close()
    conn.close()
    return geo

def distanceIn5km(lat, lon):
    conn, cursor = connectIntoPg()
    cursor.execute("""SELECT * FROM (SELECT amenity, ST_X(way), ST_Y(way), 111.045 * DEGREES(ACOS(COS(RADIANS(""" + str(lat) + """))
            * COS(RADIANS(ST_Y(way)))
            * COS(RADIANS(ST_X(way)) - RADIANS(""" + str(lon) + """))
            + SIN(RADIANS(""" + str(lat) + """))
            * SIN(RADIANS(ST_Y(way)))))
            AS distance_in_km
            FROM planet_osm_point
            WHERE amenity = 'fuel' OR amenity = 'charging_station'
            UNION		
            SELECT amenity, ST_X(geo), ST_Y(geo), 111.045 * DEGREES(ACOS(COS(RADIANS(""" + str(lat) + """))
            * COS(RADIANS(ST_Y(geo)))
            * COS(RADIANS(ST_X(geo)) - RADIANS(""" + str(lon) + """))
            + SIN(RADIANS(""" + str(lat) + """))
            * SIN(RADIANS(ST_Y(geo)))))
            AS distance_in_km
            FROM stations
            ORDER BY distance_in_km ASC) AS subquery
        WHERE distance_in_km <= 5;""")

    records = cursor.fetchall()
    stations = pd.DataFrame(records, columns=["type", "lat", "long", "distance"])
    geo = getPointsToGeoJSON(stations)
    cursor.close()
    conn.close()
    return geo

def addStations():
    conn, cursor = connectIntoPg()

    cursor.execute("""SELECT amenity, ST_X(way), ST_Y(way) FROM planet_osm_point
                    WHERE amenity = 'fuel' OR amenity = 'charging_station'
                    UNION 
                    SELECT amenity, ST_X(geo), ST_Y(geo) from stations;""")

    records = cursor.fetchall()
    stations = pd.DataFrame(records, columns=["type", "lat", "long"])
    geo = getPointsToGeoJSON(stations)

    cursor.execute("""SELECT amenity, SUM(amenityCount) FROM(SELECT amenity, COUNT(amenity) as amenityCount FROM planet_osm_point
	                    WHERE amenity = 'fuel' OR amenity = 'charging_station'
	                    GROUP BY amenity
	                    UNION 
	                    SELECT amenity, COUNT(amenity) as amenityCount from stations
	                    GROUP BY amenity) AS subquery
                    GROUP BY amenity;""")
    records = cursor.fetchall()
    groupedStations = pd.DataFrame(records, columns=["type", "count"]).to_json()

    cursor.close()
    conn.close()
    return geo, groupedStations

def getEl():
    conn, cursor = connectIntoPg()
    cursor.execute("""SELECT amenity, ST_X(way), ST_Y(way) FROM planet_osm_point
                    WHERE amenity = 'charging_station'
                    UNION 
                    SELECT amenity, ST_X(geo), ST_Y(geo) from stations;""")

    records = cursor.fetchall()
    print(records)
    stations = pd.DataFrame(records, columns=["type", "lat", "long"])
    geo = getPointsToGeoJSON(stations)
    cursor.close()
    conn.close()
    return geo

def getGas():
    conn, cursor = connectIntoPg()
    cursor.execute("""SELECT amenity, ST_X(way), ST_Y(way) FROM planet_osm_point
                    WHERE amenity = 'fuel';""")

    records = cursor.fetchall()
    stations = pd.DataFrame(records, columns=["type", "lat", "long"])
    geo = getPointsToGeoJSON(stations)
    cursor.close()
    conn.close()
    return geo

@app.route('/')
def frontend():
    gasStations, groupedStations = addStations()
    return render_template(
        'frontend2.html', 
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        gasStations = json.dumps(gasStations),
        groupedStations = groupedStations
    )

@app.route('/near10Gas', methods = ['POST'])
def near10Gas():
    lat = request.form['point_lat']    
    lon = request.form['point_lon']
    gasStations = near10Stations(lat, lon)
    return json.dumps(gasStations)

@app.route('/near5km', methods = ['POST'])
def near5km():
    lat = request.form['point_lat']  
    lon = request.form['point_lon']
    gasStations = distanceIn5km(lat, lon)
    return json.dumps(gasStations)

@app.route('/allData', methods = ['GET'])
def allData():
    gasStations, groupedStations = addStations()
    return json.dumps(gasStations)

@app.route('/gasStations', methods = ['GET'])
def allGasStations():
    gasStations = getGas()
    return json.dumps(gasStations)

@app.route('/elStations', methods = ['GET'])
def allElStations():
    elStations = getEl()
    return json.dumps(elStations)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)