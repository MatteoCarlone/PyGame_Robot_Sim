
from __future__ import print_function
import time
from sr.robot import *

R = Robot() # Initializing a Robot object

##############################

def drive(speed , seconds):

	
	'''
	Function that gives the robot the ability of move straight for a certain time with a defined speed 
	
	Arguments:
	
		speed = speed of the motors, that will be equal on each motor
		
		seconds = time interval in which the robot will move straight 
		
	This function has no returns
		
	'''

	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed 
	time.sleep(seconds) 
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
	
##############################

def turn(speed , seconds):

	'''
	Function that gives the robot the ability to turn on its axis 
	
	Arguments:
	
		speed = speed of the motors, which will be positive on one and negative on the other in order to create the rotation
		
		seconds = time interval in which the robot will rotate 
	
	This function has no returns 
	
	'''

	R.motors[0].m0.power = speed 
	R.motors[0].m1.power = -speed 
	time.sleep(seconds)
	R.motors[0].m0.power =0
	R.motors[0].m1.power =0
	
##############################

def find_golden_token(distance=0.8, angle=45):

	'''
	Function to detect the closest golden box to the robot in a cone which by default is 90 degrees (between -45 and 45 degrees) in a maximum distance of 0.8.
	The main purpose here is to have a threshold to stop the robot and avoid walls.
	
	Arguments:
	
		distance = the settable distance of the cone in which the robot can detect golden boxes (by deafault 0.8)
		
		angle = the settable angle of the cone in which the robot can detect golden boxes (by default 45)
		
	Returns:
	
		True = if the robot doesn't detect golden boxes 
		
		False = if the robot detect golden boxes
			
	'''

	dist = distance

	for token in R.see():
		
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -angle < token.rot_y < angle:
			
			dist = token.dist
		
		rot_y = token.rot_y
		
	if dist == distance:
		
		return False
	
	else:
		
		return True 
		
#############################

def find_silver_token():

	'''
	Function to detect the closest silver token to the robot in a cone in 40 degrees (between -20 and 20 degrees) at a maximum distance of 4. 
	
	Furthermore, thanks to the gold_in_between() function, the robot ignores the tokens silver behind the walls or that have obstacles that precede them.
	
	The main purpose here is to recognise tokens silver to approach.
	
	Returns:
	
		dist = the distance of the closest silver token, -1 if no silver tokens are detected or if they are preceded by obstacles (golden boxes) 
		
		rot_y = the angle in degrees between the robot and the silver token, -1 if no silver tokens are detected or if they are preceded by obstacles (golden boxes)
	
	'''
	
	dist = 4
	
	for token in R.see():
	
		if -20 < token.rot_y < 20:
		
			if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist:
			
				if gold_in_between(token.dist, token.rot_y):
				
					print("Looking for a new Silver!!")
					
				else:
					
					dist = token.dist 
					
					rot_y = token.rot_y
	if dist == 4:
	
		return -1, -1
		
	else:
		
		return dist, rot_y

#############################

def gold_in_between(dist, rot_y):
	
	'''
	This Function is used inside find_silver_token() to check the presence or absence of golden boxes between the robot and the silver tokens it is looking for.
	
	Arguments:
	
		dist = the distnace of the current silver token that the robot has seen 
		
		rot_y = the angle in degrees of the current silver token that the robot has seen
		
	Returns:
	
		False: if there aren't golden boxes between the robot and the current silver token that has been detected 
		
		True: if there's at least one golden box between the robot and the silver token that has been detected
	
	'''
	
	
	a_th = 5
	
	for token in R.see():
	
		if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist and rot_y-a_th < token.rot_y < rot_y + a_th:
		
			return True
			
	return False
	
#############################

def Silver_Approach(dist, rot_y):

	'''
	This Function approach the silver token when the robot detect one. At first The robot will verify if it is in the right direction of the silver token and, if it's not, it will adjust itself turning right and left. Secondly it will call the function Routine().
	
	Arguments:
	
		dist = the distance of the silver token that the robot has detected 
		
		rot_y = the angle of the silver token that the robot has detected 
	
	This function has no returns
	
	'''
	
	a_th = 2
	
	while rot_y < -a_th or rot_y > a_th :
	
		if rot_y < -a_th:
		
			turn(-2,0.5)
			
			print("left a bit!!")
			
		if rot_y > a_th:
		
			turn(2,0.5)
			
			print("right a bit!!")
			
		dist , rot_y = find_silver_token()
		
	Routine()
	
#############################

def Routine():

	'''
	Function that activates the Routine ( Grab , turn , release , turn ) if and only if the robot is close enough to the silver token (distance threshold: 0.4)
	if the the robot is far from the silver token it will drive.
	
	This function has no return
	
	'''

	d_th = 0.4
	
	dist , rot_y = find_silver_token()
	
	if dist > d_th or dist == -1:
	
		drive(75,0.1)
	
	else:
	
		R.grab()
		print("Gotta catch'em all!!")
		turn(20,3)
		R.release()
		drive(-20,0.9)
		turn(-20,3)

#############################

def Rotation():

	'''
	Function to calculate the distance between the robot and the nearest golden box, respectively, to its right and left, each at an angle of 30 degrees (between 75 and 105 degrees for its right and between -105 and -75 degrees for its left).
	
	The robot will rotate towards the furthest golden box until it no longer sees any golden box in cone of 91 degrees at a distance of 1 in front of it. 
	
	The angle and the distance of the cone are settable by passing the arguments to the function find_golden_token(..,..).
	
	Thanks to this feature the robot will always turn counter-clockwise.
	
	
	This function has no returns 
	
	'''

	dist_right = 7
	dist_left = 7
	
	for token in R.see():
	
		if 75 < token.rot_y < 105:
		
			if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist_right:
				
				dist_right = token.dist
				
		if -105 < token.rot_y < -75:
		
			if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist_left:
			
				dist_left = token.dist 
				
	if dist_right > dist_left:
	
		while find_golden_token(1,45.5):
		
			turn(10,0.1)
			
		
			
	else:
	
		while find_golden_token(1,45.5):
			
			turn(-10,0.1)
		
	
		
			
###########################

def main():

	while(1):   #Infinite cycle to run the robot endlessly 
	
		if find_golden_token() == False: 
		
			# No golden boxes are detected 
		
			dist, rot_y = find_silver_token() # Detecting Silver Tokens
			
			if rot_y != -1:
			
				# Silver token found 
			
				Silver_Approach(dist , rot_y) # Approaching the silver token
				
			else:
				
				# Silver token not found 
				
				drive(75,0.1) 
				
		else:
		
			# The Robot is close to a wall (golden boxes)
		
			Rotation() # The robot rotate counter-clockwise

###########################

main()
		

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

