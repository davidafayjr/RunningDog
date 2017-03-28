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
		#print(each_lat, each_lng)
		lat = each_lat 
		lng = each_lng
		#mydatabase.put("/location/", 'testuser', {"lat": lat, "lng": lng})
		mydatabase.put("/GeoFire/Jedi One", 'l', {"0": lat, "1": lng})
		sleep(.01)

if __name__ == "__main__":

	
	intial_lat = mydatabase.get("/GeoFire/Jedi One/l", "0")
	intial_lng = mydatabase.get("/GeoFire/Jedi One/l", "1")

	lat_a, lng_a = (intial_lat, intial_lng)

	lat_b, lng_b = (lat_a-0.0002, lng_a - 0.0008)
	
	lat_c, lng_c = (lat_b-0.0009, lng_b + 0.0006)
	
	lat_d, lng_d = (lat_c+ 0.0007, lng_c + 0.0003)
	
	
try:
	while True:

		runLeg(lat_a, lng_a, lat_b, lng_b, 50)
		runLeg(lat_b, lng_b, lat_c, lng_c, 50)
		runLeg(lat_c, lng_c, lat_d, lng_d, 50)
		runLeg(lat_d, lng_d, lat_a, lng_a, 50)
		
except KeyboardInterrupt:

	mydatabase.put("/GeoFire/Jedi One", 'l', {"0": intial_lat, "1": intial_lng})
			
except ConnectionError:

	mydatabase.put("/GeoFire/Red five", 'l', {"0": intial_lat, "1": intial_lng})
	
	

	