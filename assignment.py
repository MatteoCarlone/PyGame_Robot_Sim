
##################################################################### FIRST ASSIGNMENT RESEARCH TRACK #######################################################################


################################# IMPORTING LIBRARIES #################################


from __future__ import print_function
import time
from sr.robot import *


#########################################


R = Robot()    # Initializing a Robot object.


################################# DEFINING FUNCTIONS #################################

def drive(speed , seconds):

	
	'''
	Function that gives the robot the ability of move straight for a certain time with a defined speed 
	
	Arguments:
	
		speed = speed of the motors, that will be equal on each motor to move straight
		
		seconds = time interval in which the robot will move straight 
		
	This function has no returns
		
	'''

	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed 
	time.sleep(seconds) 
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
	
#########################################

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
	
#########################################

def find_golden_token(distance=0.9, angle=45):

	'''
	Function to detect the closest golden box to the robot in a cone which by default is 90 degrees (between -45 and 45 degrees) in a maximum distance of 0.9.
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
		
#########################################

def find_silver_token():

	'''
	Function to detect the closest silver token to the robot in a cone in 140 degrees (between -70 and 70 degrees) at a maximum distance of 1.2. 
	
	Furthermore, thanks to the gold_in_between() function, the robot ignores the tokens silver behind the walls or that have obstacles that precede them.
	
	The main purpose here is to recognise tokens silver to approach.
	
	Returns:
	
		dist = the distance of the closest silver token, -1 if no silver tokens are detected or if they are preceded by obstacles (golden boxes) 
		
		rot_y = the angle in degrees between the robot and the silver token, -1 if no silver tokens are detected or if they are preceded by obstacles (golden boxes)
	
	'''
	
	dist = 1.2
	
	for token in R.see():
	
		if -70 < token.rot_y < 70:
		
			if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist:
			
				if gold_in_between(token.dist, token.rot_y):
				
					print("Looking for a new Silver!!")
					
				else:
					
					dist = token.dist 
					
					rot_y = token.rot_y
	if dist == 1.2:
	
		return -1, -1
		
	else:
		
		return dist, rot_y

#########################################

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
	
#########################################

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
	
#########################################

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

#########################################

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
		
	
			
################################# MAIN FUNCTION #################################


def main():

	'''
	The idea is to have an infinite loop to make the robot work continuously:

	* The First step is to look for the gold boxes, the robot behavior will be different if it is close to a gold box or to a silver token.

	* Second step, check if a silver token is in the robot's field of vision or not.

	* the Third step dependes by the second one:

		* If the robot see a silver token, it will approach it in order to grab it. This control is made with the statement " if rot_y != -1 " because find_silver_token()
		  returns -1 if no silver token are detected.

		* If the robot doesn't see a silver token, it will drive straight ahead.

	* Fourth step, strictly related to the First, if the robot is close to a golden box, it will call the Rotation() function to turn counter-clockwise with respect to the path.

	'''

	while(1):   # Infinite cycle to run the Robot endlessly 
	
		if find_golden_token() == False:     # No Golden Boxes are detected , First Step.
		
		
			dist, rot_y = find_silver_token() 	# Detecting Silver Tokens, Second Step.
			
			if rot_y != -1:    #  Third Step. 
			
				# Silver token found. 
			
				Silver_Approach(dist , rot_y) 	# Approaching the Silver Token.
				
			else:
				
				# Silver Token not found 
				
				drive(75,0.1)  # Drive straight ahead.
				
		else:
		
			# The Robot is close to a wall (Golden Boxes).
		
			Rotation() # Rotate counter-clockwise

#########################################

main()
		

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

