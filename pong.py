# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user40_zv97bmv9cXMQxkw.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT /2]
    x = random.randrange(2, 4)
    y = random.randrange(1, 3)
    if direction == RIGHT:
        ball_vel = [x, - y]
    elif direction == LEFT:
        ball_vel = [-x, -y]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)
    paddle1_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle2_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle1_vel = 0
    paddle2_vel = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line((WIDTH / 2, 0),(WIDTH / 2, HEIGHT), 1, "White")
    canvas.draw_line((PAD_WIDTH, 0),(PAD_WIDTH, HEIGHT), 1, "White")
    canvas.draw_line((WIDTH - PAD_WIDTH, 0),(WIDTH - PAD_WIDTH, HEIGHT), 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= 0 and paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= 0 and paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles canvas.draw_line(point1, point2, line_width, line_color)
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos], [HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "white") 
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "white")
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos <= ball_pos[1] <= (paddle1_pos + PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        elif ball_pos[0] <=  BALL_RADIUS + PAD_WIDTH:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos <= ball_pos[1] <= (paddle2_pos + PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), (146, 50), 50, "white", "sans-serif") 
    canvas.draw_text(str(score2), (438, 50), 50, "white", "sans-serif")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 5
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = vel
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = - vel
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = vel
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = - vel
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0

def reset():
    new_game()
    
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", reset)

# start frame
new_game()
frame.start()