# Standard imports
import platform

# Local imports
from uib_inf100_graphics import *
from view import move_view, zoom_view
from simulation import change_desired_simrate, pause_sim, unpause_sim, place_sun


def init_control(app) -> None:
    if platform.system() == 'Windows':
        right_mouse_btn_press   = "<Button-3>"
        right_mouse_btn_release = "<B3-ButtonRelease>"
    elif platform.system() == 'Darwin':
        right_mouse_btn_press   = "<Button-2>"
        right_mouse_btn_release = "<B2-ButtonRelease>"
    #TODO: Add linux support

    # Bind RMB release to right_mouse_released()
    app._theRoot.bind(right_mouse_btn_release, lambda event:
        right_mouse_released(app, App.MouseEventWrapper(event)))

    # Bind mouse wheel scroll to mouse_wheel_scrolled() by Torstein Strømme
    app._theRoot.bind("<MouseWheel>", lambda event:
                      mouse_wheel_scrolled(app, event))

    # FOR FUTURE USE
    # # Bind RMB press to right_mouse_pressed() by Torstein Strømme
    # app._theRoot.bind(right_mouse_btn_press, lambda event:
    #     right_mouse_pressed(app, App.MouseEventWrapper(event)))
    

    # Change mouse pull rate
    app.mouse_movedDelay = 1  # Milliseconds

def right_mouse_released(app, event) -> None:
    place_sun(app, (event.x, event.y))

def mouse_dragged(app, event) -> None:
    move_view(app, event)

def mouse_wheel_scrolled(app, event) -> None:
    zoom_view(app, event)

def key_pressed(app, event) -> None:
    # Simrate change
    if event.key == '+':
        change_desired_simrate(app, 'increase')
    
    if event.key == '-':
        change_desired_simrate(app, 'decrease')
    
    if event.key == 'Space':
        if not app.sim_paused:
            pause_sim(app)
        else:
            unpause_sim(app)


# FOR FUTURE USE:
# def size_changed(app):
#     # This only kick in when window has moved, not when it
#     # starts to move.
#     pause_sim(app)
#
# def right_mouse_pressed(app, event) -> None:
#     pass
#
# def mouse_pressed(app, event) -> None:
#     pass
#
# def mouse_released(app, event) -> None:
#     pass
#
# def mouse_moved(app, event) -> None:
#     pass