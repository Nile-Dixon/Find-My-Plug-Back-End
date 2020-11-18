import requests
import random
import os
from dotenv import load_dotenv
import re

load_dotenv(verbose=True)

def generate_random_string():
	charbank = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
	ret_string = ""
	for x in range(10):
		ret_string += charbank[random.randint(0,len(charbank) - 1)]
	return ret_string

def geolocate(text):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + text + '&key=' + os.getenv('GEOLOCATION_API_KEY')
	r = requests.get(url)
	data = r.json()
	if 'results' not in data:
		return None
	lat = data['results'][0]['geometry']['location']['lat']
	lng = data['results'][0]['geometry']['location']['lng']
	return {'lat' : lat, 'lng' : lng}


def search_for_directions(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
	try:
		
		coords_one = str(y_coord_1) + ','  + str(x_coord_1)
		coords_two = str(y_coord_2) + ','  + str(x_coord_2)

		directions_list = []

		url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + coords_one + '&destination=' + coords_two + '&key=' + os.getenv('GEOLOCATION_API_KEY')
		r = requests.get(url)
		data = r.json()
		if "routes" not in data:
			return {
				'polyline' : None,
				'directions' : []
			}
		steps = data['routes'][0]['legs'][0]['steps']
		direction_polyline = data['routes'][0]['overview_polyline']['points']
		for step in steps:
			directions_list.append(step['html_instructions'])

		return {
			'polyline' : direction_polyline,
			'directions' : directions_list
		}

			
	except:
		return {
			'polyline' : None,
			'directions' : []
		}