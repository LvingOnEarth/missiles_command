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

def drawMissile(missiles):
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

        dead_missile(missiles)

def dead_missile(missiles):
    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)
    return missiles

def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('white')
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = missile.towards(x, y)
    missile.setheading(heading)
    missile.showturtle()

    info = {'missile': missile,
            'target': [x, y],
            'state': 'launched',
            'radius': 0}
    our_missiles.append(info)

def fire_enemy_missile():
    if len(enemy_missiles) < ENEMY_COUNT:
        x_base = random.randint(-300, 300)
        y_base = 300
        e_missile = turtle.Turtle()
        e_missile.speed(0)
        e_missile.color('red')
        e_missile.penup()
        e_missile.setpos(x_base, y_base)
        e_missile.pendown()
        heading = e_missile.towards(BASE_X, BASE_Y)
        e_missile.setheading(heading)

        info = {'missile': e_missile,
                'target': [BASE_X, BASE_Y],
                'state': 'launched',
                'radius': 0}
        enemy_missiles.append(info)

window.onclick(fire_missile)

while True:
    window.update()

    fire_enemy_missile()

    drawMissile(our_missiles)
    drawMissile(enemy_missiles)















