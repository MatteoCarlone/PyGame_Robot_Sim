##### Stats ######

import math
from sr.robot import *
import sys
import time

start_time = time.time()

print("--- %s seconds ---" % (time.time() - start_time))

counter = 0

laps = " "

dist_right = " "

dist_left = " "

file_laps = open("laps.txt","w")

l =  open("dist_left.txt","w")

r =  open("dist_right.txt","w")

def Lap_Counter(Grab):
    
	global counter, laps

	if Grab:

		counter = counter + 1

		print("Counter: ", counter)

		if (((counter%7) == 0)):
        
			laps = ('Laps: ' + str(math.floor(counter/7)) + " Time: " + str((time.time() - start_time)) + '\n')
        
			file_laps.write(laps)

def Goal_Distances_left(see):
    
	global counter, dist_left, l
    
	dist = 100
    
	for token in see:
        
		if token.dist < dist and -100 < token.rot_y < -80:
		
			if token.info.marker_type == "gold-token":
                
				dist = token.dist
            
	dist_left = ('Dist: ' + str(dist) + "   Time: " + str((time.time() - start_time))+ "   Lap:  " + str(math.floor(counter/7)) + '\n')
                
	l.write(dist_left)



def Goal_Distances_right(see):
                         
	global counter, dist_right , r
    
	dist = 100
    
	for token in see:
        
		if token.dist < dist and 80 < token.rot_y < 100:

			if token.info.marker_type == "gold-token":
                
				dist = token.dist                   
                             
	dist_right = ('Dist: ' + str(dist) + "   Time: " + str((time.time() - start_time)) + "   Lap:  " + str(math.floor(counter/7)) + '\n')
                
	r.write(dist_right)
                
def Wrong_Direction(pointed, pre_pointed):

	global counter

	if(pre_pointed == pointed):
        
		wd = ("Wrong Direction!! " + "   Time: " + str((time.time() - start_time)) + "   Lap:  " + str(math.floor(counter/7)) + '\n')
           
		file_laps.write(wd)


