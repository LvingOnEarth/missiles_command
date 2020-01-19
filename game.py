import random
import turtle
import os

BASE_PATH = os.path.dirname(__file__)
BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5

window = turtle.Screen()
window.setup(1200 + 3, 700 + 3)
window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
window.screensize(1200, 768)
window.tracer(n=2)

class Missile:
    def __init__(self, x, y, color, x2, y2):
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

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()

class Building:
    INITIAL_HEALTH = 2000

    def __init__(self, pos, pic):
        self.health = self.INITIAL_HEALTH
        self.pos = pos
        self.pic = pic

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.setpos(x=pos[0], y=pos[1])
        pic_path = os.path.join(BASE_PATH, 'images', self.pic[0])
        window.register_shape(pic_path)
        self.pen.shape(pic_path)

    def health_state(self):
        if self.pic[0] == 'base.gif':
            return

        if self.health < self.INITIAL_HEALTH * 0.3:
            self.draw(self.pic[2])

        elif self.health < self.INITIAL_HEALTH * 0.8:
            self.draw(self.pic[1])


    def draw(self, pic_name):
        pic_path = os.path.join(BASE_PATH, 'images', pic_name)
        if self.pen.shape() != pic_path:
            window.register_shape(pic_path)
            self.pen.shape(pic_path)

    def show(self):
        self.pen.showturtle()

    def hide(self):
        self.pen.hideturtle()

class Base(Building):
    INITIAL_HEALTH = 3000

    def open_base(self):
        for missile in our_missiles:
            if missile.distance(self.pos[0], self.pos[1]) < 50:
                self.draw('base_opened.gif')
                break
        else:
            self.draw('base.gif')

def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y + 15, x2=x, y2=y)
    our_missiles.append(info)

def fire_enemy_missile():
    x_base = random.randint(-500, 500)
    y_base = 300
    random_build_target = random.choice(buildings)
    x_target = random_build_target.pos[0]
    y_target = random_build_target.pos[1]
    info = Missile(color='red', x=x_base, y=y_base, x2=x_target, y2=y_target)
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
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


def game_over():
    for build in buildings:
        if build.health <= 0:
            buildings.remove(build)
            build.hide()

    if len(buildings) == 0:
        return True


def check_impact():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue

        for build in buildings:
            if enemy_missile.distance(build.pos[0], build.pos[1]) < enemy_missile.radius * 10:
                build.health -= 200

def create_building():
    # base = Base(info_base)

    for info in info_buildings:
        if info['name'][0] != 'base.gif':
            build = Building(info['pos'], info['name'])
        else:
            build = Base(info['pos'], info['name'])
        buildings.append(build)

def build_show():
    for build in buildings:
        build.show()


def check_building_health():
    for build in buildings:
        build.health_state()

our_missiles = []
enemy_missiles = []
buildings = []
# info_base = {'name': ['base.gif'], 'pos': [0, -300]}
info_buildings = [{'name': ['base.gif'], 'pos': [0, -300]},
                  {'name': ['house_1.gif', 'house_2.gif', 'house_3.gif'], 'pos': [-200, -300]},
                  {'name': ['kremlin_1.gif', 'kremlin_2.gif', 'kremlin_3.gif'], 'pos': [-400, -300]},
                  {'name': ['nuclear_1.gif', 'nuclear_2.gif', 'nuclear_3.gif'], 'pos': [200, -300]},
                  {'name': ['skyscraper_1.gif', 'skyscraper_2.gif', 'skyscraper_3.gif'], 'pos': [400, -300]}]

create_building()

window.onclick(fire_missile)


def base_open():
    buildings[0].open_base()


while True:
    window.update()
    if game_over():
        continue
    build_show()
    base_open()
    check_impact()
    check_enemy_count()
    check_interceptions()
    check_building_health()
    move_missile(missiles=our_missiles)
    move_missile(missiles=enemy_missiles)















