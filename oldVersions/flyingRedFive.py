from firebase import firebase
from time import sleep
import numpy as np

mydatabase = firebase.FirebaseApplication('https://myfirstmapboxapp-11599.firebaseio.com/', None)

def createSteps(a, b, number_of_steps):

	delta = b - a
	step = delta/number_of_steps
	return step

def runLeg(start_lat, start_lng, stop_lat, stop_lng, number_of_steps):

	lat_step = createSteps(start_lat, stop_lat, number_of_steps)
	lng_step = createSteps(start_lng, stop_lng, number_of_steps)

	indexes = list(range(0,number_of_steps-1))
	each_lat = start_lat
	each_lng = start_lng

	for index in indexes:
		each_lat = each_lat + lat_step
		each_lng = each_lng + lng_step
		print("Red Five [%s, %s]" % (each_lat, each_lng))
		lat = each_lat 
		lng = each_lng
		#mydatabase.put("/location/", 'testuser', {"lat": lat, "lng": lng})
		mydatabase.put("/GeoFire/Red five", 'l', {"0": lat, "1": lng})
		sleep(.01)

def pointInsidePolygon(polygon_list, lat, lng):
 
	inside = false
	next_index = 0

	for current_point in polygon_list
		next_index=(next_index+1) % len(polygon_list)
		(p1_lng, p1_lat, p1_alt) = current_point.split(",")
		(p2_lng, p2_lat, p2_alt) = polygon_list[next_index].split(",")
		inside = lineIntersect(inside, float(lng), float(lat), float(p1_lng), float(p1_lat), float(p2_lng), float(p2_lat))
	
	return inside

def lineIntersect(inside, x, y, p1_x, p1_y, p2_x, p2_y):
	
	if y > min(p1_y, p2_y)
		if y <= max(p1_y, p2_y)
			if x <= max(p1_x, p2_x)
				if p1_y != p2_y
				xinters = (y-p1_y) * (p2_x-p1_x)/(p2_y - p1_y) + p1_x
					if p1_x==p2_x or x<=xinters
					inside = not inside
	
	return inside

if __name__ == "__main__":

	
	intial_lat = mydatabase.get("/GeoFire/Red five/l", "0")
	intial_lng = mydatabase.get("/GeoFire/Red five/l", "1")

	lat_a, lng_a = (intial_lat, intial_lng)

	lat_b, lng_b = (lat_a-0.0012, lng_a - 0.0003)
	
	lat_c, lng_c = (lat_b-0.0006, lng_b + 0.0015)
	
	lat_d, lng_d = (lat_c+ 0.0017, lng_c - 0.0003)
	
try:
	while True:

		runLeg(lat_a, lng_a, lat_b, lng_b, 50)
		runLeg(lat_b, lng_b, lat_c, lng_c, 50)
		runLeg(lat_c, lng_c, lat_d, lng_d, 50)
		runLeg(lat_d, lng_d, lat_a, lng_a, 50)
		
except KeyboardInterrupt:

	mydatabase.put("/GeoFire/Red five", 'l', {"0": intial_lat, "1": intial_lng})

except ConnectionError:

	mydatabase.put("/GeoFire/Red five", 'l', {"0": intial_lat, "1": intial_lng})