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

class Missile:
    def __init__(self, x, y, color, x2, y2):
        self.x = x
        self.y = y
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen

        self.state = 'launched'
        self.target = [x2, y2]
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    def get_x(self):
        return self.pen.xcor()

    def get_y(self):
        return self.pen.ycor()

def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)

def fire_enemy_missile():
    x_base = random.randint(-500, 500)
    y_base = 300
    info = Missile(color='red', x=x_base, y=y_base, x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)

def move_missile(missiles):
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()

def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue

        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.get_x(), our_missile.get_y()) < our_missile.radius * 10:
                enemy_missile.state = 'dead'

base = turtle.Turtle()
base.hideturtle()
base.speed(0)
base.penup()
base.setpos(x=BASE_X, y=BASE_Y)
pic_path = os.path.join(BASE_PATH, 'images', 'base.gif')
window.register_shape(pic_path)
base.shape(pic_path)
base.showturtle()

base_health = 2000


def game_over():
    return base_health < 0


def check_impact():
    global base_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue

        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius * 10:
            base_health -= 100


window.onclick(fire_missile)

while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missile(missiles=our_missiles)
    move_missile(missiles=enemy_missiles)















