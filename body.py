# Standard imports
from random import randrange
from math import atan2, cos, sin, sqrt

# Local imports
from general import ranges_overlap

# Math/Phys constants
PI = 3.141592653589793  # Pi with 15 decimals (JPL's accuracy)
G = 6.674 * 10**(-11)   # The gravitational constant (Nm²/kg²)


def init_bodies(app) -> None:
    # - All start on the same line (pos_x = 0)
    # - All values are from https://nssdc.gsfc.nasa.gov/planetary/factsheet
    # - All units are the SI-standards (m, s, kg)
    # - All except sun start at Perihelion distance from sun
    #   with perihelion speed (max orbital velociy).
    app.sun = Body(pos_x=0, pos_y=0,
                   speed_x=0, speed_y=0,
                   mass=1988500*10**24, density=1408,
                   name = "Sun")

    # MERCURY
    mercury = Body(pos_x=0, pos_y=46.000*10**9,
                   speed_x=58970, speed_y=0,
                   mass=0.33010*10**24, density=5427,
                   name = "Mercury")

    # VENUS
    venus = Body(pos_x=0, pos_y=107.480*10**9,
                 speed_x=35260, speed_y=0,
                 mass=4.8673*10**24, density=5243,
                 name = "Venus")

    # EARTH
    earth = Body(pos_x=0, pos_y=147.095*10**9,
                 speed_x=30290, speed_y=0,
                 mass=5.9722*10**24, density=5514,
                 name = "Earth")

    # MARS
    mars = Body(pos_x=0, pos_y=206.650*10**9,
                speed_x=26500, speed_y=0,
                mass=0.64169*10**24, density=3934,
                name = "Mars")

    # JUPITER
    jupiter = Body(pos_x=0, pos_y=740.595*10**9,
                   speed_x=13720, speed_y=0,
                   mass=1898.13*10**24, density=1326,
                   name = "Juptier")
    
    # SATURN
    saturn = Body(pos_x=0, pos_y=1357.554*10**9,
                  speed_x=10140, speed_y=0,
                  mass=568.32*10**24, density=687,
                  name = "Saturn")
    
    # URANUS
    uranus = Body(pos_x=0, pos_y=2732.696*10**9,
                  speed_x=7130, speed_y=0,
                  mass=86.811*10**24, density=1270,
                  name = "Uranus")

    # NEPTUNE
    neptune = Body(pos_x=0, pos_y=4471.050*10**9,
                  speed_x=5470, speed_y=0,
                  mass=102.409*10**24, density=1638,
                  name = "Neptun")
 
    app.bodies = [app.sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    app.num_of_new_suns = 0

class Body:
    """Class for celestial bodies"""
    def __init__(self, pos_x: int, pos_y: int, speed_x: int, speed_y: int, 
                       mass:  int, density: int, name="", static=False) -> None:
        # Init Defined values
        self.name = name
        self.pos = (pos_x, pos_y)
        self.speed = (speed_x, speed_y)
        self.mass = mass
        self.density = density
        self.static = static
        
        # Default start values
        self.radius = round(((self.mass/self.density)*(3/(4*PI)))**(1/3))
        self.force = (0, 0)
        self.trail_positions = [self.pos, self.pos]
        self.trail_length = 0
        self.max_trail_length = 11**11
        self.trail_accuracy = 5 * 10**9  # This gives good curve on trail and good perf.

    def distance_to(self, other_body) -> int:
        """Returns the shortest distance between this body and other_body"""
        this_x, this_y = self.pos
        other_x, other_y = other_body.pos
        
        delta_x = (this_x - other_x)
        delta_y = (this_y - other_y)

        distance = round(sqrt(delta_x**2 + delta_y**2))
        return  distance

    def angle_towards(self, other_body) -> float:
        """Returns the angle from this body towards other_body with 0 beeing straight down.
        
        atan2(y,x) returns the arc tangent (in radians) of two numbers,
        but takes into account their signs (+ or -), to determine the
        quadrant the angle is in (unit circle)
        
        More info: https://www.medcalc.org/manual/atan2-function.php
        """
        this_x, this_y = self.pos
        other_x, other_y = other_body.pos
        
        delta_x = (other_x - this_x)
        delta_y = (other_y - this_y)

        return atan2(delta_y, delta_x) 

    def collision_with(self, other_body) -> bool:
        """Returns True if this body has collided with other_body"""
        distance = self.distance_to(other_body)

        if distance <= self.radius or distance <= other_body.radius:
            return True
        else:
            return False

    def force_from(self, other) -> tuple[int, int]:
        """Returns the force the other body(ies) is subjecting on to this body"""
        force_x = 0
        force_y = 0
        
        if isinstance(other, Body):
            distance = self.distance_to(other)
            angle = self.angle_towards(other)

            if self.collision_with(other):
                return (force_x, force_y)
            else:
                force = (G * self.mass * other.mass) / distance**2
                force_x = round((force * cos(angle)))
                force_y = round((force * sin(angle)))
                return (force_x, force_y)
        elif isinstance(other, list):
            for other_body in other:
                force_x = round(force_x + self.force_from(other_body)[0])
                force_y = round(force_y + self.force_from(other_body)[1])
            return (force_x, force_y)

    def speed_after(self, time: int | float) -> tuple[int, int]:
        """
        Returns new speed in x and y direction based on all the forces
        acting on the object, and the time that they have acted
        """
        force_x, force_y = self.force
        speed_x, speed_y = self.speed
        
        accel_x = force_x / self.mass
        accel_y = force_y / self.mass
        new_speed_x = round(speed_x + accel_x*time)  # v = v_0 + a*t
        new_speed_y = round(speed_y + accel_y*time)  # v = v_0 + a*t

        return (new_speed_x, new_speed_y)

    def pos_after(self, time: int | float) -> tuple[int, int]:
        """Returns the new x and y positions after a given time"""
        speed_x, speed_y = self.speed
        pos_x, pos_y = self.pos
        
        new_pos_x = round(pos_x + (speed_x * time))  # s = v*t
        new_pos_y = round(pos_y + (speed_y * time))  # s = v*t

        return (new_pos_x, new_pos_y)

    def update_trail(self) -> None:
        # This method needs refactoring lol
        # - self.trail_positions[-1] is always current position
        # - self.trail_positions[-2] is last saved position 
        #   self.trail_accuracy away from current position

        pos_x, pos_y = self.pos
        prev_x, prev_y = self.trail_positions[-2]
        delta_x = pos_x - prev_x
        delta_y = pos_y - prev_y
        dist_traveled = sqrt(delta_x**2 + delta_y**2)

        if dist_traveled > self.trail_accuracy:
            # Save this position
            self.trail_positions[-1] = self.pos    # [-2] see top method comment
            
            # Last item is always current position
            self.trail_positions.append(self.pos)  # [-1] see top method comment
            
            self.trail_length += dist_traveled
        else:
            self.trail_positions[-1] = self.pos

        while self.trail_length > self.max_trail_length and len(self.trail_positions) >= 2:
            first_x, first_y = self.trail_positions[0]
            secnd_x, secnd_y = self.trail_positions[1]
            delta_x = first_x - secnd_x
            delta_y = first_y - secnd_y
            self.trail_length -= dist_traveled
            del self.trail_positions[0]

def merge_bodies(body_1: Body, body_2: Body, body_list: list[Body]) -> None:
    """body_1 eats body_2 in an inelastic collision"""
    
    new_mass = body_1.mass + body_2.mass
    
    speed_1_x, speed_1_y = body_1.speed
    speed_2_x, speed_2_y = body_2.speed

    # Set new speeds
    new_speed_1_x = round(((body_1.mass*speed_1_x) + (body_2.mass * speed_2_x)) / new_mass)
    new_speed_1_x = round(((body_1.mass*speed_1_y) + (body_2.mass * speed_2_y)) / new_mass)
    body_1.speed = (new_speed_1_x, new_speed_1_x)

    # Set new mass
    body_1.mass = new_mass

    # Set new radius
    body_1.radius = round(((body_1.mass/body_1.density)*(3/(4*PI)))**(1/3))
    
    body_list.remove(body_2)

def create_bodies(amount: int, mass_min: int, mass_max: int, density: int, dist_origin: int) -> list[Body]:
    """Returns a list of psudo random celestial bodies."""
    bodies = []
    blocked_areas = []

    for _ in range(amount):
        mass = randrange(mass_min, mass_max)
        radius = round(((mass/density)*(3/(4*PI)))**(1/3))

        # Create random start postion
        pos_x = randrange(-dist_origin, dist_origin)
        pos_y = randrange(-dist_origin, dist_origin)

        # Create an area of coordinates where other bodies cant spawn. Padded with 10% of radius
        range_x = range(pos_x - round(radius*1.1), pos_x + round(radius*1.1))
        range_y = range(pos_y - round(radius*1.1), pos_y + round(radius*1.1))
        body_area = (range_x, range_y)

        # Go through all blocked_areas and make sure this bodys area does not overlap with any
        # of the blocked areas. If it does, make a new spawn point for the body and repeat untill
        # there are no overlaps
        pos_changed = True
        while pos_changed:
            pos_changed = False
            for area in blocked_areas:
                while ranges_overlap(body_area[0], area[0]) and ranges_overlap(body_area[1], area[1]):
                    pos_x = randrange(-dist_origin, dist_origin)
                    pos_y = randrange(-dist_origin, dist_origin)
                    range_x = range(pos_x - round(radius*1.1), pos_x + round(radius*1.1))
                    range_y = range(pos_y - round(radius*1.1), pos_y + round(radius*1.1))
                    body_area = (range_x, range_y)
                    pos_changed = True

        # Add the body's area of coordinats to blocked lists
        blocked_areas.append(body_area)

        # Add body to list
        bodies.append(Body(pos_x, pos_y, mass, density))

    return bodies
