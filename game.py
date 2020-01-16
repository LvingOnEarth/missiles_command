import random
import turtle
import os

BASE_PATH = os.path.dirname(__file__)

window = turtle.Screen()
window.setup(1200 + 3, 700 + 3)
window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
window.screensize(1200, 768)
window.tracer(n=2)

BASE_X, BASE_Y = 0, -300

ENEMY_COUNT = 5

our_missiles = []
enemy_missiles = []

def create_missile(color, x, y, x2, y2):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color(color)
    missile.penup()
    missile.setpos(x=x, y=y)
    missile.pendown()
    heading = missile.towards(x2, y2)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile,
            'target': [x2, y2],
            'state': 'launched',
            'radius': 0}
    return info

def move_missile(missiles):
    for info in missiles:
        state = info['state']
        missile = info['missile']
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                info['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            info['radius'] += 1
            if info['radius'] > 5:
                missile.clear()
                missile.hideturtle()
                info['state'] = 'dead'
            else:
                missile.shapesize(info['radius'])
        elif state == 'dead':
            missile.clear()
            missile.hideturtle()


    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)

def fire_missile(x, y):
    info = create_missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)

def fire_enemy_missile():
    x_base = random.randint(-500, 500)
    y_base = 300
    info = create_missile(color='red', x=x_base, y=y_base, x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()

def check_interceptions():
    for our_info in our_missiles:
        if our_info['state'] != 'explode':
            continue
        our_missile = our_info['missile']

        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info['missile']
            if enemy_missile.distance(our_missile.xcor(), our_missile.ycor()) < our_info['radius'] * 10:
                enemy_info['state'] = 'dead'

window.onclick(fire_missile)

while True:
    window.update()
    check_enemy_count()
    check_interceptions()
    move_missile(missiles=our_missiles)
    move_missile(missiles=enemy_missiles)















