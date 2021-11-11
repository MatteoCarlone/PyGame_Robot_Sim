
# Python Robotics Simulator  <img src="https://media4.giphy.com/media/dWlLf9EAC8u5Nd0ku4/giphy.gif?cid=ecf05e479junsdcbh0eayqrrx90l4oo4lj83zpqi9yrught2&rid=giphy.gif&ct=s" width="50"></h2>
## First Assignment of the course [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635). 
###  Professor. [Carmine Recchiuto](https://github.com/CarmineD8).

-----------------------

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).

The project aims to make a holonomic robot move inside a maze without hitting walls made of golden boxes. Furthermore, inside the maze, there are many silver tokens that the robot have to grab, move them behind him and then start again with the search for the next tokens. 

#### Holonomic Robot

![alt text](https://github.com/MatteoCarlone/my_Research_Track/blob/main/sr/robot.png)

#### Silver Token 

![alt text](https://github.com/MatteoCarlone/my_Research_Track/blob/main/sr/token_silver.png)

#### Gold Box

![alt text](https://github.com/MatteoCarlone/my_Research_Track/blob/main/sr/token.png)

#### Map 

<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/map.png" > 

The main difficulties I faced in this project were three:

* make the robot move on the map always in the correct direction (in my case counterclockwise)

* avoid walls (golden boxes)

* detect the silver tokens in order to grab them by paying attention to any gold boxes in between

The robot is able to do this thanks to two motors parallel to each other and the ability to see around itself and recognize in particular golden boxes and silver tokens. Its vision can also be limited to see only in some directions rather than others at different distances.

This project helped me to improve my knowledge of python especially in managing and creating multiple functions at the same time. It was also a first approach to the world of robotics in preparation for the study and use of [**ROS**](http://wiki.ros.org) (Robot-Operating-Systems) which is a set of software libraries and tools that help build robot applications.


Installing and running <img src="https://media3.giphy.com/media/LwBuVHh34nnCPWRSzB/giphy.gif?cid=ecf05e47t4j9mb7l8j1vzdc76i2453rexlnv7iye9d4wfdep&rid=giphy.gif&ct=s" width="50"></h2>
-----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

```bash

$ python run.py assignment.py

```

Troubleshooting <img src="https://media0.giphy.com/media/3oFzlYuazAesniYNVe/giphy.gif?cid=ecf05e471tnvpnr5e4tdm3z3h65f3kboyrg4veeoi2ssj9ct&rid=giphy.gif&ct=s" width="50"></h2>
-----------------------


When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

---

<h1 align = "center"> Features </h1>


## Motors ##

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

Two main functions have been designed to drive straight and to rotate the robot on its axis:

* `drive(speed , seconds)` : This function gives the robot the ability of move straight for a certain time with a defined speed.

    `Arguments` : 

    * speed : the speed of the motors, that will be equal on each motor in order to move straight.

    * seconds : the time interval in which the robot will move straight.

    This function has no `Returns` .


* `turn(speed , seconds)` : This function gives the robot the ability to turn on its axis.
    
    `Arguments` :

    * speed : the speed of the motors, that will be positive for one and negative for the other in order to make the rotation.

    * seconds : the time interval in which the robot will rotate.
    
    This function has no `Returns` .
    
* `Silver_Approach(dist, rot_y)` : This function has been implemented to get closer to the silver token when the robot detects one with its particular visual perception, a feature that I will describe later. At first, the robot checks if it is in the right direction to reach the silver token and if not, it will adapt itself turning left and right. Second, it will call the Routine() function to complete its purpose, take the silver token it saw.

    `Arguments` :
    
    * dist : The distance of the silver token that the robot has detected.
    
    * rot_y : the angle in dregrees of the silver token that the robot has detected 
    
    This function has no `Returns` .
    
    
## The Grabber ##

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

A function has been created to clean the main function of the code from the routine that the robot does when it has to grab a silver token.

* `Routine()` : When the robot is close enough to a silver token (in particular at a distance of 0.4), thanks to this function, it will grab the token (method: `R.grab ()`), it will turn 180 ° ( function: `turn ()`), will release the token (method: `R.release ()`), go back for a while (function: `drive ()`) and finally turn 180 ° again to continue the ride in the maze.
    
    This function has no `Returns` .
    
```python
    R.grab()
    print("Gotcha!!")
    turn(20,3)
    R.release()
    drive(-20,0.9)
    turn(-20,3)
```
<h5>The Routine turns out to be: </h5>

<p align="center">
    
<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/Grab.gif" width="400" height="225.3">
    
</p>

## Vision ##

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python

markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

Two main functions are designed to recognize the `Marker` object closest to the robot and whether it is gold or silver. 


* `find_golden_token(distance=0.9, angle=45°)` : This function detects the closest golden box to the robot in a cone wich by default is 90° (between -45° and 45°) in a maximum distance of 0.9. The main purpose here is to have a threshold to stop the robot ad avoid walls.
    
    `Arguments` :
    
    *  distance = the settable distance of the cone in which the robot can detect golden boxes (by default 0.8).
    
    *  angle = the settable angle in degrees of the cone in which the robot can detect golden boxes (by default 45°)
    
    `Returns` : 

    *  `False` : if the robot doesn't detect golden boxes 

    *  `True` : if the robot detect golden boxes 


* `find_silver_token()` : This function detects the closest silver token to the robot in a 140° cone (between -70 ° and 70°) at a maximum distance of 1.2. Furthermore, thanks to the `gold_in_between()` function, the robot ignores the tokens silver behind the walls or that have obstacles that precede them. The main purpose here is to recognise tokens silver to approach.

    `Returns` :

    *  dist : The distance of the closest silver token, `-1` if no silver tokens are detected or if they are preceded by obstacles (golden boxes).

    *  rot_y : The angle in degrees between the robot and the silver token, `-1` if no silver tokens are detected or if they are preceded by obstacles (golden boxes).


* `gold_in_between(dist, rot_y)` : This function is used inside `find_silver_token()` to check the presence or absence of golden boxes between the robot and the silver tokens it is looking for. 

    `Arguments` :

    * dist : The distance of the current silver token that the robot has seen.

    * rot_y : The angle in degrees of the current silver token that the robot has seen.

    `Returns` :

    * `False` : if there aren't golden boxes between the robot and the current silver token that the robot has seen.


    * `True` : if there's at least one golden box between the robot and the current silver token that the robot has seen.


## Rotation ##

A function called `Rotation()` has been implemented to move the robot counter-clockwise and to follow the maze without ever going back. 

* `Rotation()` : When the robot is close to the wall it calculates (using the `R.see()` method) the distance between it and the nearest golden box, respectively, to its right and left, each at an angle of 30° (between 75° and 105° for its right and between -105° and -75° for its left). 

    This function has no `Returns` .

<p align="center">
    
<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/rotation.jpeg" width="486.75" height="266.625">
    
</p>

The Robot will rotate towards the furthest golden box until it no longer sees any golden box in a 91° cone at a distance of 1 in front of it. 

The angle and the distance fo the cone are settable by passing the arguments to the function `find_golden_token(distance = ... , angle = ...)` .
    
<p align="center">
    
<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/finish_rot.jpeg" width="486.75" height="266.625">
    
</p>

<h5> The Rotation turns out to be: </h5>

<p align="center">
    
<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/rotation.gif" width="486.75" height="266.625">
    
</p>

MAIN Function
---------

Before start coding it was very useful to create a Flowchart to have clear ideas on the main actions that the robot has to do in its path inside the maze.

![FlowChart](https://user-images.githubusercontent.com/81308076/139292559-a076b5e5-06ac-4153-b2c1-8f0a6afffaa7.png)

The idea of the `main()` function is to have an infinite loop to make the robot work continuously:

* The First step is to look for the gold boxes, the robot behavior will be different if it is close to a gold box or to a silver token.
    
* Second step, check if a silver token is in the robot's field of vision or not.
    
* the Third step dependes by the second one:
    
	* If the robot see a silver token, it will approach it in order to grab it. This control is made with the statement " if rot_y != -1 " because find_silver_token() returns -1 if no silver token are detected.
		
	* If the robot doesn't see a silver token, it will drive straight ahead.
		
* Fourth step, strictly related to the First, if the robot is close to a golden box, it will call the Rotation() function to turn counter-clockwise with respect to the path.


Results
---------

I thought the results of the code and therefore of the project would be well represented with a video that shows the behaviour of the robot during the first lap of the track.

https://user-images.githubusercontent.com/81308076/139293325-9dfea8ab-4a7c-4481-aa39-1c1f78bff8f4.mp4

Possible improvements ![ezgif-4-0c80dd65ae1b](https://user-images.githubusercontent.com/81308076/139424213-cf5eea84-d903-4c21-bd66-cc046236b222.gif)
------

The greatest difficulty of this assignment was surely that there are many ways to satisfy the professor request. During the coding, in fact, I implemented many functions ( still visible in the history of this project ) just because I had more than one idea of how the robot could move inside the arena.

The code is now clean and short but also the way the robot moves in the environment is simple, its way of turning and detecting the silver tokens could be made more complex but smarter with some improvements:

1. __Online Control__ : The idea is to never stop detecting the silver tokens knowing that the robot will ignore gold boxes, a remnant of this idea lies in the gold_in_between () function, which in the final version of the project turns out to be an all too precise control. The result of this method is that the robot will not move around the arena giving priority to the golden boxes but its real target, the silver tokens. Furthermore, thanks to the control on possible obstacles in front of the tokens, the robot could have a very wide view to detect them. As I have already mentioned, I tried to implement this method with good results, the robot detected silver tokens in a 300 ° cone also seeing behind it (not completely to avoid approaching tokens already grabbed). Unfortunately, in some cases, the robot detected silver tokens already approached and I decided to stop this implementation. However, This failure brought to me another possible improvement that I've never tried yet.

2. __Already Grabbed Token__ : I'm not sure if this improvement is feasible but I think the `code` attribute of the` MarkerInfo` objects (described in the **vision feature**) could be very useful to ignore the silver tokens that the robot has already grabbed by saving their code. This idea added to the **Online Control** will let the robot have a 360° view without ever going back.


[sr-api]: https://studentrobotics.org/docs/programming/sr/
