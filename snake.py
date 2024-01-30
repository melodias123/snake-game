import asyncio
import random
import pywebcanvas as pwc

SCALE=5
canvas=pwc.Canvas(width=10000,height=600)
canvas.background.fill(color="#92A8D1")

state=1

class SnakeBody :
    def __init__(self,x_pos,y_pos):
        self.x_pos,self.y_pos=x_pos,y_pos
        self.rect=pwc.Rect(x=0,y=0,width=5*SCALE,height=5*SCALE,color="black")

    def draw(self):
        self.rect.x=self.x_pos*SCALE
        self.rect.y=(self.y_pos*SCALE)-self.rect.height
        self.rect.color="blue"
        canvas.render(self.rect)


class Snake:
    def __init__(self,head_x_pos,head_y_pos):
        self.head_x_pos,self.head_y_pos=head_x_pos,head_y_pos
        self.velocity=[1,0]
        self.time=0
        self.parts=[]
        self.history=[]
        self.size=1

    def calculate(self):
        self.head_x_pos=self.head_x_pos+self.velocity[0]*SCALE
        self.head_y_pos=self.head_y_pos+self.velocity[1]*SCALE
        head_part=SnakeBody(self.head_x_pos,self.head_y_pos)
        self.parts=[head_part]
        self.history.append([self.head_x_pos,self.head_y_pos])
        for i in range(self.size):
            part=SnakeBody(*self.history[-(i+1)])
            self.parts.append(part)
    def draw(self):
            for part in self.parts:
                part.draw()
class Food:
    def __init__(self):
        self.rect=pwc.Rect(x=0,y=0,width=5*SCALE,height=5*SCALE,color="green")
        self.x_pos,self.y_pos=random.randint(0,(800/SCALE)),random.randint(0,(600/SCALE))

    def draw(self):
        self.rect.x =self.x_pos * SCALE
        self.rect.y = self.y_pos *SCALE-self.rect.height
        self.rect.color="red"
        canvas.render(self.rect)

snake=Snake(50,50)
food=Food()
async def delay():
    if not state == 1:
        return
    await asyncio.sleep(0.25)


def check_fail():
    global state

    if snake.head_x_pos < 0 or (
            snake.head_x_pos * SCALE >= 800 or (
            snake.head_y_pos <= 0 or (
            snake.head_y_pos * SCALE > 600
    )
    )):
        return True

    for pos_1 in snake.history[-snake.size:]:
        count = 0
        for pos_2 in snake.history[-snake.size:]:
            if pos_1 == pos_2:
                count += 1
        if count > 1:
            return True
def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1+w1 < x2 or x1 > x2+w2:
        return False
    if y1 > y2+h2 or y1+h1 < y2:
        return False
    return True
def check_eat():
    if check_collision(snake.parts[0].rect.x,snake.parts[0].rect.y,snake.parts[0].rect.width,snake.parts[0].rect.height,food.rect.x,food.rect.y,food.rect.width,food.rect.height):
        return True

async def on_refresh():
    global state
    global snake
    global food

    canvas.clear()

    if state == 1:
        food.draw()
        snake.calculate()
        snake.draw()
        if check_fail():
            state = 0
        if check_eat():
            snake.size += 1
            food = Food()
def controls(e):
    global snake
    if not state==1:
        return
    if e.code=='KeyW':
        snake.velocity=[0,-1]
    elif e.code=='KeyS':
        snake.velocity = [0,1]
    elif e.code == 'KeyA':
        snake.velocity = [-1,0]
    elif e.code == 'KeyD':
        snake.velocity = [1, 0]

pwc.add_event_handler("keydown",controls)
loop=pwc.Loop()
loop.add_task("delay",delay)
loop.add_task("on_refresh",on_refresh)
loop.run()

