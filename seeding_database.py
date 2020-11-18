import json 
from app import app
from models import db, Plugs, Stations
from functions import generate_random_string

stations = []

with open("data/stations.json","r") as file_to_read:
	stations = json.load(file_to_read)


with app.app_context():
	for station in stations:
		new_station = Stations(
			station['id'],
			station['name'],
			station['phone'],
			station['address'],
			station['city'],
			station['state'],
			station['zip_code'],
			station['latitude'],
			station['longitude']
		)
		db.session.add(new_station)
		if station['ev_connector_types'] != None:
			for plug_type in station['ev_connector_types']:
				new_plug = Plugs(
					generate_random_string(),
					station['id'],
					plug_type
				)
				db.session.add(new_plug)
		db.session.commit()

print("Finished")