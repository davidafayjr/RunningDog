# from firebase import firebase
from time import sleep
import numpy as np
import pyrebase
import sys
import random

global DRONE_NAME


config = {
  "apiKey": "AIzaSyCLWJMUXvEE8c-272i9RlNM07dLehvWIiY",
  "authDomain": "myfirstmapboxapp.firebaseapp.com",
  "databaseURL": "https://myfirstmapboxapp-11599.firebaseio.com/",
  "storageBucket": "projectId.appspot.com"

}

firebase = pyrebase.initialize_app(config)

#mydatabase = firebase.FirebaseApplication('https://myfirstmapboxapp-11599.firebaseio.com/', None)
mydatabase = firebase.database()


def createSteps(a, b, number_of_steps):

	delta = b - a
	step = delta/number_of_steps
	return step

def runLeg(start_lat, start_lng, stop_lat, stop_lng, number_of_steps):
	'''
	simulate movement between to locaions and transmit the locations to firebase
	call isThisPointInANoFlyZone(lat, lng) to check it the location is in a no-fly zone
	''' 

	lat_step = createSteps(start_lat, stop_lat, number_of_steps)
	lng_step = createSteps(start_lng, stop_lng, number_of_steps)

	indexes = list(range(0,number_of_steps-1))
	each_lat = start_lat
	each_lng = start_lng

	for index in indexes:
		each_lat = each_lat + lat_step
		each_lng = each_lng + lng_step
		print("%s [%s, %s]" % (DRONE_NAME, each_lat, each_lng))
		lat = each_lat 
		lng = each_lng
		# mydatabase.put("/location/", 'testuser', {"lat": lat, "lng": lng})
		# mydatabase.put("/GeoFire/Jedi One", 'l', {"0": lat, "1": lng})
		
		if not isThisPointInANoFlyZone(lat, lng):

			data = {
			    "GeoFire/%s/l/" % DRONE_NAME: {
			        "0": lat,
			        "1": lng
			    }
			    
			}		

			mydatabase.update(data)
			# mydatabase.child("GeoFire").child("Jedi One").child("l")
			# mydatabase.update(data)
			sleep(.01)

def isThisPointInANoFlyZone(lat, lng):
	'''
	compare the current lat/lng to the NoFlyZones from firebase database
	if in a no-fly zone return false 
	'''


	allNoFlyZones = mydatabase.child("NoFlyZones").get()

	for each_noflyzone in allNoFlyZones.each():

		polygon_list = each_noflyzone.val().split()

		if pointInsidePolygon(polygon_list, lat, lng):

			print("Flying in %s" % each_noflyzone.key())

			return True

		

	return False


def pointInsidePolygon(polygon_list, lat, lng):
	'''
	helper function for isThisPointInANoFlyZone(lat, lng)
	cast a line from the curren point and counts how many of the 
	edges of the polygon it intersects with lineIntersect() function
	'''
 
	inside = False
	next_index = 0

	for current_point in polygon_list:
		
		next_index=(next_index+1) % len(polygon_list)
		(p1_lng, p1_lat, p1_alt) = current_point.split(",")
		(p2_lng, p2_lat, p2_alt) = polygon_list[next_index].split(",")
		inside = lineIntersect(inside, float(lng), float(lat), float(p1_lng), float(p1_lat), float(p2_lng), float(p2_lat))
	
	return inside

def lineIntersect(inside, x, y, p1_x, p1_y, p2_x, p2_y):
	'''
	helper function for pointInsidePolygon()
	'''
	
	if y > min(p1_y, p2_y):
		if y <= max(p1_y, p2_y):
			if x <= max(p1_x, p2_x):
				if p1_y != p2_y:
					xinters = (y-p1_y) * (p2_x-p1_x)/(p2_y - p1_y) + p1_x
					if p1_x==p2_x or x<=xinters:
						inside = not inside
	
	return inside

if __name__ == "__main__":

	global DRONE_NAME
	#global OFFSETS
	offsets = [0.0002, 0.0008, 0.0009, 0.0003, 0.0010, 0.0004]

	

	if len(sys.argv) < 2:
		print("not enough arguments")
		sys.exit()

	DRONE_NAME = sys.argv[1]

	for i, each in enumerate(offsets):

		offsets[i] = each+np.random.uniform(0.0001, 0.002)

		offsets[i] = float("{0:.4f}".format(offsets[i]))
		
		n = random.randrange(1,3)

		if n%2 :
			offsets[i] = offsets[i]*-1
			# print(offsets[i])

		offsets[i] = float("{0:.4f}".format(offsets[i]))

	# print(offsets)
	# sys.exit()

	# intial_lat = mydatabase.get("/GeoFire/Jedi One/l", "0")
	# intial_lng = mydatabase.get("/GeoFire/Jedi One/l", "1")
	intial_lat = mydatabase.child("/GeoFire/%s/l/0" % DRONE_NAME).get()
	intial_lng = mydatabase.child("/GeoFire/%s/l/1" % DRONE_NAME).get()
	print(intial_lat.val(), intial_lng.val())

#	sys.exit()
	
	lat_a, lng_a = (float(intial_lat.val()), float(intial_lng.val()))

	lat_b, lng_b = (lat_a+offsets[0], lng_a +offsets[1])
	
	lat_c, lng_c = (lat_b+offsets[2], lng_b +offsets[3])
	
	lat_d, lng_d = (lat_c+offsets[4], lng_c+offsets[5])
	
	
try:
	while True:

		runLeg(lat_a, lng_a, lat_b, lng_b, 45)
		runLeg(lat_b, lng_b, lat_c, lng_c, 45)
		runLeg(lat_c, lng_c, lat_d, lng_d, 45)
		runLeg(lat_d, lng_d, lat_a, lng_a, 45)
		
except KeyboardInterrupt:

	# mydatabase.put("/GeoFire/Jedi One", 'l', {"0": intial_lat, "1": intial_lng})
	
	data = {
		    "GeoFire/%s/l/" % DRONE_NAME: {
		        "0": intial_lat.val(),
		        "1": intial_lng.val()
		    }
		    
	}		

	mydatabase.update(data)

except ConnectionError:

	data = {
		    "GeoFire/%s/l/" % DRONE_NAME: {
		        "0": intial_lat.val(),
		        "1": intial_lng.val()
		    }
		    
	}		

	mydatabase.update(data)
	