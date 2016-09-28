from pico2d import *
import math

def handle_events():
    global running
    global cur_x, cur_y, radius

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            cur_x, cur_y = event.x, 600 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            cur_y = cur_y + 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            cur_y = cur_y - 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            cur_x = cur_x - 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            cur_x = cur_x + 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if(radius >= 20):
                radius = radius - 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            if(radius <= 300):
                radius = radius + 10

def rot():
    global r, x, y, cur_x, cur_y, rot
    global angle
    r = angle * math.pi / 180

    x = cur_x + (math.cos(r) * radius)
    y = cur_y + (math.sin(r) * radius)

    angle = angle + 1


open_canvas()
character = load_image('run_animation.png')



running = True
x, y = 0, 0
cur_x, cur_y = 400, 300
angle = 0
radius = 100
r = 0
frame = 0
hide_cursor()
while (running):
    clear_canvas()
    character.clip_draw(frame * 100, 0, 100, 100, x, y)
    update_canvas()
    frame = (frame + 1) % 8
    rot()
    delay(0.05)
    handle_events()

close_canvas()