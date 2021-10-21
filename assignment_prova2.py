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
    
     
def find_silver_token():  

    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    
    dist = 5 # modificato da noi

    for token in R.see():
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
        
            dist=token.dist
            
	    rot_y=token.rot_y
	    
    if dist == 5:
    
		return -1, -1
	
    else:
    
    	return dist, rot_y
    

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
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45 < token.rot_y < 45:
        
            dist=token.dist
            
	    rot_y=token.rot_y
	    
    if dist==0.8:
    
		return -1, -1
		
	
    else:
    
   		return dist , rot_y
   		
   	
##########################

def golden_for_rotation():

	dist = 1 
	
	for token in R.see():
	
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45.1 < token.rot_y < 45.1:
			
			dist = token.dist
			
	if dist == 1:
	
		return False
	
	else:
	
		return True

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
	
		while(golden_for_rotation()):
		
			turn(2,0.5)	
	
	else:
		
		while(golden_for_rotation()):
		
			turn(-2,0.5)	
		
		
##########################

def silver_priority():

	dist_s = 5
	
	dist_g = 5
	
	a_th = 3
	
	for token in R.see():
	
		#if(-130 < token.rot_y < -80 or 80 < token.rot_y < 130):
		if(-130 < token.rot_y < 130):
		
			if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist_s:
		
				dist_s = token.dist
			
				rot_y_s = token.rot_y
		
		
	for token in R.see():
	
		if(dist_s != 5):
	
			if(token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist_s and rot_y_s-a_th < token.rot_y < rot_y_s + a_th):
			
				return -1, -1
				
						
	if (dist_s == 5):
	
		return -1 ,-1
		
	else:
		
		return dist_s , rot_y_s

##########################

	
	


##########################

def front_silver():

	dist = 5
	
	for token in R.see():
	
		if(-5 < token.rot_y < 5):
		
			if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist:
		
				dist = token.dist
			
				rot_y = token.rot_y

	if dist == 5:
	
		return -1 ,-1
		
	else:
		
		return dist , rot_y

#########################





#########################

def main():

	d_th_g = 0.5
	
	d_th_s = 0.4
	
	a_th = 2
	
	while(1):
		
		d_s , rot_y_s = find_silver_token()
		
		
		d_g , rot_y_g = find_golden_token()
		
		if(rot_y_g == -1): # non vede gold
		
			if(rot_y_s != -1 and -20 < rot_y_s < 20 and d_s < 3): #vede un silver di fronte
			
						
				print("TROVATO! di fronte a me")
				
				print(rot_y_s)
				
				while(rot_y_s < -a_th or rot_y_s > a_th):
				
				
					if(rot_y_s < -a_th):
						
						turn(-2,0.5)
							
					if(rot_y_s > a_th):
					
						turn(2,0.5)
							
					d_s , rot_y_s = find_silver_token()
						
				if(d_s > d_th_s):
					
					drive(20,0.1)
						
				else:
					
					R.grab()
						
					turn(20,3.1)
						
					R.release()
						
					turn(-20,3.1)
				
				
								
			drive(30,0.1) # non vede silver di fronte 
			
		else: # vede gold
			
			dist_ds , rot_ds = silver_priority()
			
			if(rot_ds!=-1 and dist_ds != -1): # se vede silver negli intervalli giusti senza beccare un gold 
			
				
				print("TROVATO! dopo gold")
				
				print(rot_ds)
				
				print("compreso eh")
				
				if(rot_ds < -a_th):
					
					print("Ruotando")
				
					turn(-3,0.5)
					
				if(rot_ds > a_th):
						
					print("Ruotando")
						
					turn(3,0.5)
				
				d_s , rot_y_s = front_silver()
				
				while(rot_y_s == -1):
				
					if(rot_ds < -a_th):
					
						print("Ruotando")
				
						turn(-3,0.5)
						
						d_s , rot_y_s = front_silver()
								
					if(rot_ds > a_th):
						
						print("Ruotando")
						
						turn(3,0.5)
							
						d_s , rot_y_s = front_silver()
						
				if(d_s > d_th_s):
				
					drive(20,0.1)
				
				else:
				
					R.grab()
					
					turn(20,3)
					
					R.release()
					
					turn(-20,3.1)
						
			else: # se non vede silver 
			
				print("Non ho visto nulla")
				
				Rotation()
				
						
					
				
					
#######################			
			
		
main()			






















 
    
