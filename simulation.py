# Standard imports
from time import time

# Local imports
from body import merge_bodies, Body
from view import pix_to_pos


def init_simulation(app) -> None:
    # SIM CONSTANTS
    app.TIME_AT_SIM_START = time()

    app.MAX_TIME_TO_SIM = 60*60*10  # Never simulate more this many secs 
                                    # at a time  (see simulate_bodies())

    app.MAX_SIMRATE = 60*60*24*100  # Limit the speed of simulation

    app.timer_delay = 20   # Basically sets a min frametime of 20ms (50FPS).
                           # This desides how often timer_fired(app) is called

    # SIM VARIABLES (Start Values)
    app.sim_paused = False
    app.frametime = app.timer_delay/1000  # Seconds
    app.frames_per_sec = 1/app.frametime
    
    app.desired_simrate = 60*60  # Start simrate at 1h per 1s
    app.sec_to_sim_per_sec = app.desired_simrate
    app.actual_simrate = app.sec_to_sim_per_sec  # Actual simrate changes
                                                 # when sim starts
    app.sec_to_sim_per_frame = app.actual_simrate / app.frames_per_sec

    # Used in: update_frametime_adjust_sec_to_sim_per_frame()
    app.sim_sec_passed = 0
    app.prev_sim_sec_passed = 0
    app.prev_real_sec_passed = 0

    # Used for calclutation paused sim time:
    app.paused_at = 0
    app.upaused_at = 0
    app.paused_sec_passed = 0  # How many seconds the sim has been passed

def change_desired_simrate(app, option) -> None:
    """Changes the sec_to_sim_per_sec (desired_simrate)"""

    if option == "increase" and app.desired_simrate != app.MAX_SIMRATE:
        if app.desired_simrate < 10:                # If < 10s, + 1s
            app.desired_simrate += 1
        elif app.desired_simrate < 60:              # If < 1m, + 10s
            app.desired_simrate += 10 
        elif app.desired_simrate < 60*10:           # If < 10m, + 1m
            app.desired_simrate += 60
        elif app.desired_simrate < 60*60:           # If < 1h, + 10m
            app.desired_simrate += 60*10
        elif app.desired_simrate < 60*60*24:        # If < 1d, + 1h
            app.desired_simrate += 60*60
        elif app.desired_simrate < 60*60*24*5:      # If < 5d, + 1d
            app.desired_simrate += 60*60*24
        elif app.desired_simrate < app.MAX_SIMRATE:    # If < 1y, + 5d
            app.desired_simrate += 60*60*24*5
        else:
            pass
    elif option == "decrease" and app.desired_simrate != 1:
        if app.desired_simrate > 60*60*24*5:        # If > 5d, - 5d
            app.desired_simrate -= 60*60*24*5
        elif app.desired_simrate > 60*60*24:        # If > 1d, - 1d
            app.desired_simrate -= 60*60*24
        elif app.desired_simrate > 60*60:           # If > 1h, - 1h
            app.desired_simrate -= 60*60
        elif app.desired_simrate > 60*10:           # If > 10m, - 10m
            app.desired_simrate -= 60*10
        elif app.desired_simrate > 60:              # If > 1m, - 1m
            app.desired_simrate -= 60
        elif app.desired_simrate > 10:              # If > 10s, - 10s
            app.desired_simrate -= 10
        elif app.desired_simrate > 1:               # If > 1s, - 1s
            app.desired_simrate -= 1
        else:
            pass
    else:
        pass

    app.sec_to_sim_per_sec = app.desired_simrate

def pause_sim(app) -> None:
    app.sim_paused = True
    app.paused_at = time()

def unpause_sim(app) -> None:
    app.sim_paused = False
    app.unpaused_at = time()
    app.paused_sec_passed += app.unpaused_at - app.paused_at

def place_sun(app, mouse_pos: tuple[int, int]) -> None:
    app.num_of_new_suns += 1
    if app.sun.static:
        app.sun.static = False
    else:
        pass

    x, y = pix_to_pos(app, mouse_pos)
    new_sun =  Body(pos_x=x, pos_y=y,
                    speed_x=0, speed_y=0,
                    mass=1.9885*10**30, density=1408,
                    name = f"New Sun {app.num_of_new_suns}")
    app.bodies.append(new_sun)

def current_actual_simrate(app) -> float:
    """Return current actual simrate"""

    sim_passed  = app.sim_sec_passed
    real_passed = time() - app.TIME_AT_SIM_START - app.paused_sec_passed

    sim_passed_since  = sim_passed  - app.prev_sim_sec_passed
    real_passed_since = real_passed - app.prev_real_sec_passed

    simrate = sim_passed_since/real_passed_since

    app.prev_sim_sec_passed  = sim_passed
    app.prev_real_sec_passed = real_passed 

    return simrate

def update_frametime_adjust_sec_to_sim_per_frame(func):
    """Updates frametime and adjust sec_to_sim_per_frame
    
    The frametime varies from frame to frame due to 
    varying simulation exec time. This in turn makes
    it neccesary to adjust app.sec_to_sim_per_frame,
    so that the actual_simrate stays somewhat constant
    and somewhat equal to the desired_simrate.
    """
    def wraper(app):
        if not app.sim_paused:
            # Time the func
            func_start = time()
            func(app)
            func_end = time()

            # Add the seconds that where just simulated to the total
            app.sim_sec_passed += app.sec_to_sim_per_frame

            # Calculate current frametime
            # (Add app.timer_delay/1000 which is the programs already
            # existing execution delay in seconds.)
            app.frametime = (func_end - func_start) + app.timer_delay/1000

            # Calculate new FPS using the current frametime
            app.frames_per_sec = 1/(app.frametime)

            # Calculate new sec_to_sim_per_frame based on actual simrate
            app.actual_simrate = current_actual_simrate(app)
            app.sec_to_sim_per_frame *= app.sec_to_sim_per_sec/app.actual_simrate

    return wraper

def simulate_bodies(bodies, time: int | float, max_time: int) -> None:
    """Modifies bodies list after simulated time
    
    Not using return of new list due to perfomance
    """
    
    # If it wants to simulate more than max_time
    # we have to split it up into max_time chuncks 
    # for a somewhat accurate simulation
    if time > max_time:
        repeat = int(time/(max_time))
    else:
        repeat = 1

    for _ in range(repeat):
        for body in bodies:
            # Check if this body eats a smaller body
            for other_body in bodies:
                if (body is not other_body and
                    body.collision_with(other_body) and
                    body.mass >= other_body.mass):
                    merge_bodies(body, other_body, bodies)
            # Calculate new postion
            if not body.static:
                body.pos = body.pos_after(time)
        # Give all bodies their new speeds given new force and pos
        for body in bodies:
            body.force = body.force_from(bodies)
            body.speed = body.speed_after(time)
            body.update_trail()

@update_frametime_adjust_sec_to_sim_per_frame
def timer_fired(app) -> None:
    """Called every app.timer_delay ms"""
    # Every time app.bodies is changed, the app redraws the frame
    # Thus the exec. time of timer_fired is basically the frametime
    if not app.sim_paused:
        simulate_bodies(app.bodies, app.sec_to_sim_per_frame, app.MAX_TIME_TO_SIM)
    else: 
        pass
