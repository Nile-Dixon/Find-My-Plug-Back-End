#FLASK LIBRARY AND FLASK PLUGINS
from flask import request, jsonify
from flask_restful import Resource, Api

#THIRD PARTY LIBRARIES
import jwt
import polyline
from shapely.geometry import Point, LineString


#STANDARD LIBRARIES 
import os
import secrets

#CUSTOM FILES
from models import db, Stations, Plugs
from functions import geolocate, search_for_directions

api = Api()


class DirectionsResource(Resource):
	def post(self):
		content = request.json 

		#GET DIRECTIONS FROM START POINT TO END POINT
		start_address = content['start_address'].replace(" ","+")
		end_address = content['end_address'].replace(" ","+")

		start_coords = geolocate(start_address)
		end_coords = geolocate(end_address)

		directions = search_for_directions(start_coords['lng'],start_coords['lat'],end_coords['lng'],end_coords['lat'])
		if directions['polyline'] == None:
			return {'status':'error','message':'Couldn\'t find directions.'}

		main_line = polyline.decode(directions['polyline'])
		main_line_string = LineString(main_line)

		#FIND THE CLOSEST ELECTRIC CHARGING STATION
		elec_stations = Stations.query.all()
		min_distance = 1000000
		closest_station = None

		for elec_station in elec_stations:
			elec_station_point = Point(elec_station.lat, elec_station.lng)
			station_distance = main_line_string.distance(elec_station_point)
			if station_distance <= min_distance:
				min_distance = station_distance
				closest_station = elec_station

		#GET DIRECTIONS TO AND FROM STATION 
		to_station_directions = search_for_directions(start_coords['lng'],start_coords['lat'],closest_station.lng, closest_station.lat)
		from_station_directions = search_for_directions(closest_station.lng, closest_station.lat, end_coords['lng'], end_coords['lat'])

		if to_station_directions['polyline'] == None or from_station_directions['polyline'] == None:
			return {'status':'error','message':'Couldn\'t find directions.'}

		station_directions_coords = polyline.decode(to_station_directions['polyline']) + polyline.decode(from_station_directions['polyline'])
		station_directions_list = to_station_directions['directions'] + from_station_directions['directions']


		return {
			'polyline' : polyline.decode(directions['polyline']), 
			'directions' : directions['directions'], 
			'closest_station' : closest_station.json(),
			'station_directions' : station_directions_list,
			'station_polyline' : station_directions_coords
		}



