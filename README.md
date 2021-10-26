
# Python Robotics Simulator  <img src="https://media4.giphy.com/media/dWlLf9EAC8u5Nd0ku4/giphy.gif?cid=ecf05e479junsdcbh0eayqrrx90l4oo4lj83zpqi9yrught2&rid=giphy.gif&ct=s" width="50"></h2>
## First Assignment of the course [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635). 
###  Professor. [Carmine Ricchiuto](https://github.com/CarmineD8).

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

![alt text](https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/map.png)

The main difficulties I faced in this project were three:

* make the robot move on the map always in the correct direction (in my case counterclockwise)

* avoid walls (golden boxes)

* detect the silver tokens in order to grab them by paying attention to any gold boxes in between

The robot is able to do this thanks to two motors parallel to each other and the ability to see around itself and recognize in particular golden boxes and silver tokens. Its vision can also be limited to see only in some directions rather than others at different distances.

This project helped me to improve my knowledge of python especially in managing and creating multiple functions at the same time. It was also a first approach to the world of robotics in preparation for the study and use of ROS (Robot-Operating-Systems) which  is a set of software libraries and tools that help build robot applications.


Installing and running <img src="https://media3.giphy.com/media/LwBuVHh34nnCPWRSzB/giphy.gif?cid=ecf05e47t4j9mb7l8j1vzdc76i2453rexlnv7iye9d4wfdep&rid=giphy.gif&ct=s" width="50"></h2>
-----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

```bash

$ python run.py assignment.py

```

Troubleshooting <img src="https://media0.giphy.com/media/ssm0SSwVbICGc/giphy.gif?cid=6c09b952305418f647c5754bccce27a04b88bd537f9e1735&rid=giphy.gif&ct=s" width="50"></h2>
-----------------------


When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

Features
---------

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

Two main functions have been designed to drive straight and to rotate the robot on its axis:

* `drive(speed , seconds)` : This function gives the robot the ability of move straight for a certain time with with a defined speed.

    `Arguments` : 

    * 

    *

    `Returns` :

    *


* `turn(speed , seconds)` : This function gives the robot the ability to turn its self on its axis.
    
    `Arguments`

    * 

    *

    `Returns`

    *    


### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

A function has been created to clean the main of the code from the routine that the robot does when it has to grab a silver token.

* `Routine()` : This function 
    
 
    `Returns`

    *    

<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/Grab.gif">


### Vision ###

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

* `find_silver_token()` :

    `Returns`

    *  

    *  

* `find_golden_token()` :

    `Returns`

    *  

    *  


### Rotation ###

A function called `Rotation()` has been implemented to move the robot counter-clockwise and to follow the maze without ever going back. 
When the robot is close to the wall it calculates (using the `R.see()` method) the distance between it and the nearest golden box, respectively, to its right and left, each at an angle of 30 ° (between 75 ° and 105 ° for his right and between -105 ° and -75 ° for his left).

<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/rotation.jpeg" width="649" height="355.5">

The Robot will rotate towards the furthest golden box until it no longer sees any golden box in a 90° cone at a distance of 1 in front of it.

<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/finish_rot.jpeg" width="649" height="355.5">

The Rotation turns out to be:

<img src="https://github.com/MatteoCarlone/my_Research_Track/blob/main/images/rotation.gif" width="649" height="355.5">

###  ###

Results
---------

https://user-images.githubusercontent.com/81308076/138707707-600e8095-5c70-4a8d-97cd-6d168d9cfd0d.mp4



[sr-api]: https://studentrobotics.org/docs/programming/sr/
