from flask import Flask, request
import requests, json, re

app = Flask(__name__)

@app.route("/")
def basicRoute():
    return {"restaurants": "/restaurants/"}

@app.route("/restaurants/")
def restaurantsRoute():
    if request.args.get('q', ''):
        q = requests.utils.unquote(request.args.get('q', ''))
        response = requests.post("https://lz4.overpass-api.de/api/interpreter",
        f"""[out:json];node[amenity=restaurant][name~{"'"+q+"'"}];out meta;""".encode("UTF-8")
        )
        
        return json.loads(response.text)

    elif (request.args.get('lat', '') and request.args.get('lon', '')):
        minLat = request.args.get('lat', '')
        minLon = request.args.get('lon', '')
        lat = re.search("^(\d+).(.*)$", minLat)
        lon = re.search("^(\d+).(.*)$", minLon)

        if lat[2] == '9': maxLat = str(int(lat[1])+1)
        else: maxLat = lat[1]+'.'+str(int(lat[2])+1)

        if lon[2] == '9': maxLon = str(int(lon[1])+1)
        else: maxLon = lon[1]+'.'+str(int(lon[2])+1)

        response = requests.post("https://lz4.overpass-api.de/api/interpreter",
        f"""[out:json];node[amenity="restaurant"]({minLat}, {minLon}, {maxLat}, {maxLon});out meta;""".encode("UTF-8")
        )
        
        return json.loads(response.text)

    return 'Préciser des paramètres.'