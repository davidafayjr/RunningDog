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
		print(each_lat, each_lng)
		lat = each_lat 
		lng = each_lng
		mydatabase.put("/", 'dog', {"lat": lat, "lng": lng})
		#mydatabase.put("/GeoFire/Red three", 'l', {"0": lat, "1": lng})
		sleep(.01)

if __name__ == "__main__":

	
	intial_lat = mydatabase.get("/dog/", "lat")
	intial_lng = mydatabase.get("/dog/", "lng")

	lat_a = 39.701464
	lng_a = -83.743603
	
	lat_b = 39.698953
	lng_b = -83.741411
	
	lat_c = 39.698810
	lng_c = -83.741691

	lat_d = 39.7010129
	lng_d = -83.744331

	try:
		while True:

			runLeg(lat_a, lng_a, lat_b, lng_b, 50)
			runLeg(lat_b, lng_b, lat_c, lng_c, 10)
			runLeg(lat_c, lng_c, lat_d, lng_d, 50)
			runLeg(lat_d, lng_d, lat_a, lng_a, 20)
		
	except KeyboardInterrupt:

		mydatabase.put("/", 'dog', {"lat": intial_lat, "lng": intial_lng})
	