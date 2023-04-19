# Standard imports
from time import time


def init_view(app) -> None:
    app.view_center_pix = (app.height/2 , app.height/2)
    app.view_center_pos = (0.0,0.0)
    app.origin_pos = (0,0)
    app.origin_pix = (app.width/2, app.height/2)
    app.view_zoom = 6.01612851*10**(-9)  # This makes a 900px * 900px = 1AU * 1AU at start
    app.meter_per_pixel = 1/app.view_zoom
    app.last_mouse_pix = None
    app.last_move_call = 0

def change_view_center(app, new_view_center_pos: tuple) -> None:
    """Changes the app view center.

    Set the app view center position to be the
    passed 'new_view_center_pos' argument. 
    The method also updates the origin_pix since 
    this will change when the canvas view center changes.

    Args:
        new_view_center_pos: Contains x and y pos coords.
    """
    app.view_center_pos = new_view_center_pos
    
    origin_pix_x = (app.view_center_pix[0] 
                    - app.view_center_pos[0]*app.view_zoom)
    
    origin_pix_y = (app.view_center_pix[1] 
                    + app.view_center_pos[1]*app.view_zoom)
    
    app.origin_pix = (origin_pix_x, origin_pix_y)

def zoom_view(app, event) -> None:
    mouse_x, mouse_y = pix_to_pos(app, (event.x, event.y))
    center_x, center_y = app.view_center_pos

    # Scroll up (increase zoom) by 10%
    if event.num == 4 or event.delta == 120:
        app.view_zoom = app.view_zoom * 1.1
        new_x = center_x + (mouse_x - center_x)/8
        new_y = center_y + (mouse_y - center_y)/8
        app.meter_per_pixel = 1/app.view_zoom
        change_view_center(app, (new_x, new_y))
    
    # Scroll down (decrease zoom) by 10%
    if event.num == 5 or event.delta == -120 and app.view_zoom > 0:
        app.view_zoom = app.view_zoom * 0.9
        new_x = center_x - (mouse_x - center_x)/8
        new_y = center_y - (mouse_y - center_y)/8
        app.meter_per_pixel = 1/app.view_zoom
        change_view_center(app, (new_x, new_y))

def move_view(app, event) -> None:
    # If 100ms has passed since last move
    # set current mouse pixel position as
    # last mouse pixel position making
    # the movement of the view less
    # stuttery
    if (time() - app.last_move_call) > 0.100:
        app.last_mouse_pix = (event.x, event.y)
        app.last_move_call = time()


    last_x, last_y = app.last_mouse_pix
    curr_x, curr_y = event.x, event.y
    view_center_x, view_center_y = pos_to_pix(app, app.view_center_pos)

    # If mouse moves right, move view center left
    if (curr_x > last_x):
        view_center_x = view_center_x - abs(curr_x - last_x)
    # If mouse moves left, move view center right
    elif (curr_x < last_x):
        view_center_x = view_center_x + abs(curr_x - last_x)

    # If mouse moves up, move view center up
    if (curr_y > last_y):
        view_center_y = view_center_y - abs(curr_y - last_y)
    # If mouse moves down, move view center down
    elif (curr_y < last_y):
        view_center_y = view_center_y + abs(curr_y - last_y)

    new_view_center = (view_center_x, view_center_y)
    new_view_center = pix_to_pos(app, new_view_center)
    change_view_center(app, new_view_center)

    app.last_mouse_pix = (curr_x, curr_y)

def pos_to_pix(app, pos: tuple[int, int]) -> tuple[int, int]:
    """Converts positon coords to pixel coords

    Args:
        pos: The postion coords (x, y) and will
                be converted.
    
    Returns:
        A tuple containg pixel coords (x, y)
    """
    pos_x, pos_y = pos
    origin_pix_x, origin_pix_y = app.origin_pix

    pix_x = round(origin_pix_x + pos_x*app.view_zoom)
    pix_y = round(origin_pix_y - pos_y*app.view_zoom)
    return (pix_x ,pix_y)

def pix_to_pos(app, pix: tuple[int, int]) -> tuple[int, int]:
    """Converts pixel coords to positions coords

    Args:
        pix: The pixel coords (x, y) and will
                be converted.
    
    Returns:
        A tuple containg position coords (x, y)
    """
    pix_x, pix_y = pix
    origin_pix_x, origin_pix_y = app.origin_pix

    pos_x =  round((pix_x - origin_pix_x) / app.view_zoom)
    pos_y = round((-pix_y + origin_pix_y) / app.view_zoom)
    return (pos_x ,pos_y)
