# Standard imports
from math import atan2, cos, sin

# Local imports
from body import Body
from view import pos_to_pix
from general import sec_to_practical_time_string


def draw_body(app, canvas, body: Body) -> None:
    """Draws a white circle representing the body.

    Args:
        body: A Body object which will be drawn
        canvas: Frame to draw on
        app: Containg canvas
    """
    pixel_pos = pos_to_pix(app, body.pos)

    x0 = pixel_pos[0] - body.radius*app.view_zoom
    y0 = pixel_pos[1] + body.radius*app.view_zoom
    x1 = pixel_pos[0] + body.radius*app.view_zoom
    y1 = pixel_pos[1] - body.radius*app.view_zoom

    canvas.create_oval(x0,y0,x1,y1, fill='white', outline='')

def draw_force(app, canvas, body: Body) -> None:
    # Not in use. Doesn't look good as is
    """Draws a red arrow representing the body's force.

    Args:
        body: A Body object which will be used
                to draw it's force
        canvas: Frame to draw on
        app: Containg canvas
    """
    force_x, force_y = body.force
    if force_x == 0 and force_y == 0:
        return
    else:
        angle = atan2(force_y, force_x)

        start = body.pos
        start_x, start_y = start
        end_x = start_x + cos(angle)*20
        end_y = start_y + sin(angle)*20
        end = (end_x, end_y)


        start_pix = pos_to_pix(app, start)
        end_pix = pos_to_pix(app, end)
        
        canvas.create_line(start_pix[0], start_pix[1], 
                           end_pix[0], end_pix[1], 
                           fill='red',arrow='last')

def draw_trail(app, canvas, body: Body) -> None:
    """Draws a green line representing the body's trail.

    Args:
        body: A Body object which will be used
                to draw it's recent trail.
        canvas: Frame to draw on
        app: Containg canvas
    """
    pix_list = []
    # Convert the trail positons to pixel coords
    for pos in body.trail_positions:
        pix = pos_to_pix(app, pos)
        pix_list.append(pix)

    canvas.create_line(pix_list, fill='green')

def draw_name(app, canvas, body: Body) -> None:
    """Draws the name of the body above it"""
    
    text_pos = pos_to_pix(app, body.pos)
    text_x = text_pos[0]
    text_y = text_pos[1] - 12

    canvas.create_text(text_x, text_y,
                       text=body.name, 
                       font=('Helvetica', 8, 'bold'), 
                       fill='white', justify='center')

def draw_time_passed(app, canvas) -> None:
    y = (int(app.sim_sec_passed) // (60*60*24*365))
    d = (int(app.sim_sec_passed) // (60*60*24)) % 365
    h = (int(app.sim_sec_passed) // (60*60)) % 24
    m = (int(app.sim_sec_passed) // 60) % 60
    s = (int(app.sim_sec_passed)) % 60

    canvas.create_text(app.width/2, 25,
                       text=(f'{y:>4} years | {d:>3} days | ' 
                             f'{h:>2} hours {m:>2} min {s:>2} sec'), 
                       font=('Courier', 10, 'bold'), 
                       fill='white', justify='center')

def draw_sim_info(app, canvas) -> None:
    fps = int(app.frames_per_sec)

    simrate = sec_to_practical_time_string(app.desired_simrate)

    canvas.create_text(app.width-100, 40,
                       text=(f'Simrate: {simrate} per 1s\n'
                             f'FPS :{fps}'), 
                       font=('Helvetica', 10, 'bold'), 
                       fill='white', justify='right')

def is_in_frame(app, pos: tuple[int, int]) -> bool:
    """Return true if pos (x,y) is in app frame"""
    pos_x, pos_y = pos
    
    if 0 < pos_x < app.width and 0 < pos_y < app.height:
        return True
    else:
        return False

def redraw_all(app, canvas) -> None:
    """Called everytime any app variable is changed"""
    # Background
    canvas.create_rectangle(0,0,app.width, app.height, fill='black')

    for body in app.bodies:
        
        # Check if part of trail is in frame and draw if it is
        for point in body.trail_positions:
            point_pix = pos_to_pix(app, point)
            if is_in_frame(app, point_pix):
                draw_trail(app, canvas, body)
                break
            else:
                continue

        # Check if body is in frame and draw if it is
        body_coverage = (body.pos[0] + body.radius, body.pos[1] + body.radius)
        body_coverage_pix = pos_to_pix(app, body_coverage)
        if is_in_frame(app, body_coverage_pix):
            draw_body(app, canvas, body)
            draw_name(app, canvas, body)
        else:
            pass

    # Simulation info
    draw_time_passed(app, canvas)
    draw_sim_info(app,canvas)

    # Controls info
    canvas.create_text(app.width/2, app.height - 48, 
                       text=('<Space> to pause | <+> and <-> to change simrate | <MouseWheel> to zoom\n'
                             '<LeftMouseButton> to move view | <RightMouseButton> to place down a Sun'), 
                       font=('Courier', 12), 
                       fill='white', justify='center')

    # Draw PAUSED
    if app.sim_paused:
        canvas.create_text(app.width/2, app.height-app.height/8, 
                    text="PAUSED", 
                    font=('Helvetica', 42, 'bold'), 
                    fill='white', justify='center')
