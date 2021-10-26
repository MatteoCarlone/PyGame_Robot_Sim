
from __future__ import print_function
import time
from sr.robot import *

R = Robot()

##########################

def drive(speed, seconds):

    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
	
    """
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
    
##########################
    
       
def turn(speed, seconds):

    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
	  
    """
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
    
##########################

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist= 0.8
    
    for token in R.see():
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and  -45 < token.rot_y < 45:
        
            dist=token.dist
            
	    rot_y=token.rot_y
	    
    if dist==0.8:
    
		return False
		
	
    else:
    
   		return True

##########################

def gold_in_between(dist_s,rot_y_s):				
					
	a_th = 5
	
	for token_g in R.see():
				
		if token_g.info.marker_type is MARKER_TOKEN_GOLD and token_g.dist < dist_s and rot_y_s-a_th < token_g.rot_y < rot_y_s + a_th :
	
			return True
						
	return False


##########################

def find_silver_token():

	dist = 4
	 
	
	for token in R.see():
	
		if(-30 < token.rot_y < 30):
		
			if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist:
			
				if(gold_in_between(token.dist, token.rot_y)):
				
					print("Ricerca")
					
				else:
				
					dist = token.dist
			
					rot_y = token.rot_y

	if dist == 4:
	
		return -1 ,-1 
		
	else:
		
		return dist , rot_y 
		
##########################

def Silver_Approach(d_s , rot_y_s):

	a_th = 2
	
	while( rot_y_s < -a_th or rot_y_s > a_th):
	
		if(rot_y_s < -a_th):
			
			turn(-2,0.5)
							
		if(rot_y_s > a_th):
	
			turn(2,0.5)
				
		d_s , rot_y_s = find_silver_token()
		
				
	Routine()		

##########################


def Routine():


	d_th_s = 0.4

	
	d, rot = find_silver_token()
		
	if(d > d_th_s or d == -1):
					
		drive(75,0.1)
		
						
	else:
					
		R.grab()
						
		turn(20,3)
		
		drive(20,0.9)
						
		R.release()
					
		drive(-20,0.9)
			
		turn(-20,3)



##########################


def Rotation():

	dist_right = 7 
	
	dist_left = 7
	
	for token in R.see():
	
		if(75 < token.rot_y < 105):
			
			if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist_right:
			
				dist_right = token.dist
			
			
		
		
		if(-105 < token.rot_y < -75):
			
			if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist_left:
			
				dist_left = token.dist
	
	if dist_right > dist_left:
	
		while(angle_rotation()):
		
			turn(10,0.1)	
	
	else:
		
		while(angle_rotation()):
		
			turn(-10,0.1)	


##########################


def angle_rotation():

	dist = 1
	
	for token in R.see():
	
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45.2 < token.rot_y < 45.2:
			
			dist = token.dist
			
	if dist == 1:
	
		return False
	
	else:
	
		return True

##########################

def main():

	while(1):
	
		if(find_golden_token()== False):  # No Gold
		
			d , rot = find_silver_token()	
		
			if(rot != -1): #Si Silver 
		
				Silver_Approach(d, rot)
			
			else:
			
				drive(75,0.1)
		 
				
		else: 		 # Vede Golden
		
		
			Rotation()
			
		

#############################

main()
