# Solar System Sim
This is one of my assignments from the autumn 2022 [INF100](https://www.uib.no/en/course/INF100) course at [The University of Bergen (UiB)](https://www.uib.no/en). We were given a graphics library, `uib_inf100_graphics.py` *(based on Tkinter)*, and had a few weeks to create whatever user intractable program we wanted. This is my result :P 

All code *(except `uib_inf100_graphics.py`*\*) is my own unless stated otherwise.


*\*The graphics library `uib_inf100_graphics.py` (created by [Torstein Strømme](https://torstein.stromme.me/)) is a fork of `cmu_112_graphics.py` originally created for the course CMU 15-112 by developers from [Carnegie Mellon University](Carnegie%20Mellon%20University).*


## What is it?
This is my humble attempt at creating a simulation of our solar system via Newtonian gravitation. A simulation in which you can mess around by placing down other Sun like celestial bodies.

![Screenshot from program](https://i.imgur.com/KxJlZz6.png) 
All units in the program are in SI units https://en.wikipedia.org/wiki/International_System_of_Units

I've capped the simulation at 50FPS (20ms frame-time) as this gives the most consistent FPS, from the basic solar system, to when multiple suns have been added (at least on my system). Better this than starting at several hundreds FPS, and then dropping to 50 after adding 20 suns to the simulation.


## How do I use it?
1. Install the latest version of python from https://www.python.org/downloads/
2. Install the Tkinter library via the terminal `pip install tk`
3. Start *Solar System Sim* via the terminal `python main.py`

The controls are displayed inside the application.


## How does it work?
The simulation starts with all planets aligned in a vertical line with the sun. All the planets start at their perihelion (their furthest distance from the Sun).  For every frame, the program calculates the force pull between all the celestial bodies. The program then calculates the acceleration for every individual body, which is further used to calculate the speed knowing how long the frame time is. The celestial bodies position is calculated based on it's previous position, its last known speed, and the current frame time. 

The frame of reference is a static coordinate system with origin at the start position of the Sun. All velocities are relative to this coordinate system.


## Known issues:
- Some orbits (especially Mercury and Neptune) get out of hand after a few decades. There could be many reasons for this, both from the physical models and code.
- Game lags out if too many Suns are placed down. Need to improve performance.
- When moving the app window things glitch out (I think a solution would be to pause the game when the window is being moved, but I have not figured out how using `uib_inf100_graphics.py`)


## Things to do:
- `body.py` should probably be merged with `simulation.py`.
- `view.py` should probably be merged with `draw.py`.
- To many destructive functions IMO. Should probably do more pure functions where applicable.
- The bodies can be dictionaries instead of Body objects, and the methods from the Body class should be functions.
- Make my own render framework based on Tkinter, instead of using `uib_inf100_graphics.py`.
