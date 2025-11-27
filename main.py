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
TIME=0.01
ballVx0=0.5
ballVy0=0
ballMass=1
planetMass=81.3*SCALE
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
        
    def draw(self,screen):
        self.x+=self.vx
        self.y+=self.vy
        pg.draw.circle(screen,(255,0,255),(int(self.x),int(self.y)),radius=float(self.Radius))
        #pygame.draw.circle(畫在哪裡, 顏色, 圓心座標, 半徑)
        
class Planet:
    def __init__(self,x,y,Radius,mass):
        self.x=x
        self.y=y
        self.Radius=Radius
        self.mass=mass
        
    def draw(self,screen):
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
##### def end

ball=Ball(x=W/2,y=H/2,Radius=20,mass=ballMass,vx=ballVx0,vy=ballVy0) #塞參數進去
planet=Planet(x=300,y=200,Radius=50,mass=planetMass)
clock=pg.time.Clock()
dt=0
dragging=False

def showScreen1():
    global dragging
    screen.fill((247,251,247))
    ball.draw(screen) #依照之前塞的參數畫出來
    planet.draw(screen)
    for event in pg.event.get():
        if event.type== pg.QUIT:
            pg.quit()
        
        ##### dragging ball
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左鍵
                mx, my = pg.mouse.get_pos()
                # 判斷滑鼠是否點在 ball 上（用距離判斷）
                if (mx - ball.x)**2 + (my - ball.y)**2 <= ball.Radius**2:
                    dragging = True

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # 左鍵放開
                dragging = False

        if event.type == pg.MOUSEMOTION:
            if dragging:
                ball.x, ball.y = pg.mouse.get_pos()
        ### dragging ball end

    apply_gravity(ball,planet,dt)
    pg.display.flip()


while 1:
    dt=clock.tick(60)/1000 # 60fps 轉成秒
    showScreen1()

pg.quit()