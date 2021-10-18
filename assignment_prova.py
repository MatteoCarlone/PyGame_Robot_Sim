from __future__ import print_function

import time

from sr.robot import *



R = Robot()



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

def find_silver_token():    # MODIFY:  ANGLE CONTROL
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist = 3  # modificato da noi

    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -70 < token.rot_y < 70:
            dist=token.dist
	    rot_y=token.rot_y
    if dist == 3:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -60 < token.rot_y < 60:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist , rot_y 
   	
   	
def Rotation():

	dist , rot_y = find_golden_token()
	
	if rot_y < 0 :
	
		turn(30 ,1) 
		
	if rot_y > 0 :
	
		turn(-30 ,1)
		
def Silver_Approach(d_silver , rot_y_silver):

	d_th_silver = 0.4    
	
	
	a_th = 2
	
			
	if(rot_y_silver < -a_th):
	
		turn(2, 0.5)
					
	if(rot_y_silver > a_th):
	
		turn(-2, 0.5)
        				
	if(d_silver < d_th_silver):
      
        			
		R.grab()
		
		turn(20,3.6)
        	
        R.release()
        
        turn(-20,3.6)


		




def main():
	
	d_th_golden = 0.5
	
	d_th_silver = 0.4    
	
	
	a_th = 2
	
	while(1):
	
		
		d_silver , rot_y_silver = find_silver_token()
		
		d_golden , rot_y_golden = find_golden_token()
		
		
		
		if rot_y_golden != -1:
		
			drive(20,0.1) 
		
			if(rot_y_silver != -1): #  vedo silver 
			
				print("TROVATO!!")	
			
				
        		while(d_silver>d_th_silver or rot_y_silver> a_th or rot_y_silver<-a_th):
	
					if(rot_y_silver > a_th):
			
						turn(5,1)
			
					if(rot_y_silver < -a_th):
		
						turn(-5,1)
			
					if(d_silver > d_th_silver):
		
						drive(20, 1)
			
					else:
			
						R.grab()
			
						turn(20,3.6)
        	
        				R.release()
        
       					turn(-20,3.6)

			
			
			
				dist , rot_y = find_token()
        		
				
		else:    # minore soglia verde 
			
			Rotation()
			
			
        			
		       			
        			
        		
# Grabba e fai routine anche quando non scontri animali 					
				
					
				
main()
	
	



   	
   	
   	

