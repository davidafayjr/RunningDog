# RunningDog
flyingDrones.py
Simulates a drone sending location information to a firebase database.
Gets no-fly zone information from firebase database and compares current 
location against the no-fly zones and prevents the simulated drone form entering.
runningDog.py
This was used to test the native communiation between Firebase and Android without Geofire
this demonstrates the differnce between animated movement in our app and just simply location updates.  You can see the blinky movement of this compared to the smooth movement of the animated drones. 

## Dependancies
1.  Anaconda Python with Numpy
1.  prebase library form here https://github.com/thisbejim/Pyrebase

## Running flyingDrones.py
1.  in linux shell type 
	python flyingDrones.py <drone name from firebase library>

## Running runningDog.py
1.  in linux shell 
	python runningDog.py


## Group 17 Code links

https://github.com/davidafayjr/mapboxprototyping

https://github.com/davidafayjr/RunningDog

https://github.com/davidafayjr/droneSimulator

https://github.com/davidafayjr/firebasewebsocket

https://github.com/davidafayjr/easywsclient

https://github.com/davidafayjr/cfcts_sketch

https://github.com/GSBhub/cfcts_sketch
