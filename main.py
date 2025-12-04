# 1. go to "cmd" and input "python"
# 2. it will ask you to install python, just install
# 3. after installation, input "pip install pygame"
# 4. there you go

'''
https://www.peko-step.com/zhtw/tool/tfcolor.html (顏色轉換器)
'''


import pygame as pg
import math

##### initialize
H=600
W=800
SCALE=10
TIME=120 #FPS

# Ball 初始參數
ballX0=W/2+225
ballY0=H/2+175
ballRadius=20
ballMass=1
ballVx0=0
ballVy0=0

# Planet 初始參數
planetX0=W/2-80
planetY0=H/2-40
planetRadius=30
planetMass=120000
planetVx0=0
planetVy0=0

screen=pg.display.set_mode((W,H))
pg.display.set_caption("多元選修")
image_icon=pg.image.load('image/game_icon.png') #load icon
pg.display.set_icon(image_icon)


##### initialize end


##### def class

class Ball: # 類似一個package的自訂函數(們) 當成C++的struct
    def __init__(self,x,y,Radius,mass,vx=0,vy=0):
        self.x=x
        self.y=y
        self.Radius=Radius
        self.mass=mass
        self.vx=vx
        self.vy=vy
        self.start_x = x
        self.start_y = y
        
    def draw(self,screen):
        # self.x+=self.vx
        # self.y+=self.vy
        pg.draw.circle(screen,(255,0,255),(int(self.x),int(self.y)),radius=float(self.Radius))
        #pygame.draw.circle(畫在哪裡, 顏色, 圓心座標, 半徑)
        
class Planet:
    def __init__(self,x,y,Radius,mass,vx=0.5,vy=0):
        self.x=x
        self.y=y
        self.Radius=Radius
        self.mass=mass
        self.vx=vx
        self.vy=vy
        
    def draw(self,screen):
        # self.x+=self.vx
        # self.y+=self.vy
        pg.draw.circle(screen,(50, 180, 180),(int(self.x),int(self.y)),radius=float(self.Radius))

def apply_gravity(ball, planet,dt, G=100):
    dx = planet.x - ball.x
    dy = planet.y - ball.y #計算位移
    dist = math.sqrt(dx*dx + dy*dy) #計算距離

    force = G * planet.mass / (dist * dist)

    ax = force * (dx / dist)
    ay = force * (dy / dist)

    ball.vx += ax*dt
    ball.vy += ay*dt
    ball.x += ball.vx*dt
    ball.y += ball.vy*dt
##### def end

ball=Ball(x=ballX0,y=ballY0,Radius=20,mass=ballMass,vx=ballVx0,vy=ballVy0) #塞參數進去
planet=Planet(x=planetX0,y=planetY0,Radius=50,mass=planetMass,vx=planetVx0,vy=planetVy0)
clock=pg.time.Clock()
dt=0
dragging=False
start=False
def draggingball(ball, event, power=2):
    """
    ball: 物體(具有 x, y, vx, vy, radius)
    event: pygame 事件
    dragging: 是否正在拖曳
    power: 發射力量倍率
    """
    global dragging,start
    # 按下左鍵 → 判斷是否按到球
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        mx, my = pg.mouse.get_pos()
        # 判斷是否點到球
        if (mx - ball.x)**2 + (my - ball.y)**2 <= ball.Radius**2:
            dragging = True
        print("1")

    # 拖曳中 → 跟著滑鼠走
    # if event.type == pg.MOUSEMOTION and dragging:
    #     a=1
         #ball.x, ball.y = pg.mouse.get_pos()

    # 放開左鍵 → 給速度（發射）
    if event.type == pg.MOUSEBUTTONUP and event.button == 1 and dragging:
        dragging = False
        mx, my = pg.mouse.get_pos()

        # 速度 = 從球被拉的位置 → 放手瞬間回彈
        ball.vx = (ball.start_x - mx) * power
        ball.vy = (ball.start_y - my) * power
        print(ball.vx, ball.vy)
        start=True
        print("0")


def showScreen1():
    global dragging
    screen.fill((247,251,247))
    ball.draw(screen) #依照之前塞的參數畫出來
    planet.draw(screen)
    for event in pg.event.get():
        if event.type== pg.QUIT:
            pg.quit()
        draggingball(ball, event)
    ball.x+=ball.vx*dt
    ball.y+=ball.vy*dt
    ball.draw(screen)
    if start:apply_gravity(ball,planet,dt)
    if start:apply_gravity(planet,ball,dt)
        
    pg.display.flip()


while 1:
    dt=clock.tick(TIME)/1000 # 60fps 轉成秒
    showScreen1()

pg.quit()