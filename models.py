from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime, timedelta, date

db = SQLAlchemy()


class Stations(db.Model):
	id = db.Column(db.String(20), primary_key = True)
	name = db.Column(db.String(100))
	phone = db.Column(db.String(50))
	address = db.Column(db.String(200))
	city = db.Column(db.String(100))
	state = db.Column(db.String(5))
	zip_code = db.Column(db.String(12))
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)

	def __init__(self, id, name, phone, address, city, state, zip_code, lat, lng):
		self.id = id
		self.name = name
		self.phone = phone
		self.address = address
		self.city = city
		self.state = state
		self.zip_code = zip_code
		self.lat = lat
		self.lng = lng

	def json(self):
		station_plugs = Plugs.query.filter_by(station_id = self.id).all()
		return {
			'id' : self.id,
			'name' : self.name,
			'address' : self.address,
			'city' : self.city,
			'state' : self.state,
			'zip_code' : self.zip_code,
			'lat' : self.lat,
			'lng' : self.lng,
			'phone' : self.phone,
			'plug_types' : [plug.json() for plug in station_plugs]
		}


class Plugs(db.Model):
	id = db.Column(db.String(100), primary_key = True)
	station_id = db.Column(db.String(20))
	type = db.Column(db.String(20))

	def __init__(self, id, station_id, type):
		self.id = id
		self.station_id = station_id
		self.type = type

	def json(self):
		return {
			'type' : self.type
		}


