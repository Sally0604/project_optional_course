# 1. go to "cmd" and input "python"
# 2. it will ask you to install python, just install
# 3. after installation, input "pip install pygame"
# 4. there you go

'''
https://www.peko-step.com/zhtw/tool/tfcolor.html (顏色轉換器)
'''


import pygame as pg
import math
pg.init()
##### initialize
H=600 #螢幕高度
W=800 #螢幕寬度
background_image = pg.image.load('image/multiverse.png')
background_image = pg.transform.smoothscale(background_image, (W, H))
# 縮放圖片，符合螢幕大小
SCALE=10
TIME=2 # 60*TIME # 時間倍率

# 環境 初始變數
G=100 # 重力常數
POWER=2 # 彈弓

# Ball 初始參數(座標、半徑、質量、速度)
ballX0=W/2+225
ballY0=H/2+175
ballRadius=20
ballMass=1
ballVx0=0
ballVy0=0

# Planet 初始參數(座標、半徑、質量、速度)
planetX0=W/2-80
planetY0=H/2-40
planetRadius=50
planetMass=120000
planetVx0=0
planetVy0=0

# Target 初始參數(座標、半徑、質量、速度)
targetX0=W/2-300
targetY0=H/2-200
targetRadius=10
targetMass=1
targetVx0=0
targetVy0=0


screen=pg.display.set_mode((W,H)) #設定視窗大小
pg.display.set_caption("多元選修") #視窗標題
image_icon=pg.image.load('image/game_icon.png') #載入icon
pg.display.set_icon(image_icon) #設定icon
# reset button image (放右上角)
reset_img = pg.image.load('image/reset button.png').convert_alpha() #convert_alpha() 保留透明度
# scale to reasonable size
RESET_SIZE = 48
reset_img = pg.transform.smoothscale(reset_img, (RESET_SIZE, RESET_SIZE))
reset_margin = 10
reset_rect = reset_img.get_rect()


##### initialize end


class Ball: # 類似一個package的自訂函數(們) 當成C++的struct
    def __init__(self,x,y,Radius,mass,vx=0,vy=0,color=(255,0,255,255),type=None,img=None):
        self.x=x
        self.y=y
        self.Radius=Radius
        self.mass=mass
        self.vx=vx
        self.vy=vy
        self.start_x = x
        self.start_y = y
        self.color=color
        self.type=type
        self.img = pg.image.load(img).convert_alpha() if img else None
        if self.img:
            self.img = pg.transform.scale(self.img, (Radius*2, Radius*2))
        self.tri_surf = pg.Surface((W, H), pg.SRCALPHA)
        
    def draw(self,screen):
        # self.x+=self.vx
        # self.y+=self.vy
        pg.draw.circle(self.tri_surf,self.color,(int(self.x),int(self.y)),radius=float(self.Radius))
        if self.img:
            screen.blit(self.img, (self.x - self.Radius, self.y - self.Radius))
        screen.blit(self.tri_surf, (0, 0))
        #pg.draw.circle(畫在哪裡, 顏色, 圓心座標, 半徑)

ballArray=[]
ball=Ball(x=ballX0,y=ballY0,Radius=ballRadius,mass=ballMass,vx=ballVx0,vy=ballVy0,color= (220, 220, 220, 80),type="ball",img="image/space_cat.png") 
planet=Ball(x=planetX0,y=planetY0,Radius=planetRadius,mass=planetMass,vx=planetVx0,vy=planetVy0,color=(50, 180, 180,0),type="planet", img="image/Jupiter.png") 
target=Ball(x=targetX0,y=targetY0,Radius=targetRadius,mass=targetMass,vx=targetVx0,vy=targetVy0,color=(0, 255, 0,255),type="target")

ballArray.append(ball)
ballArray.append(planet)
ballArray.append(target)

clock=pg.time.Clock() #計時器   
dt=0
dragging=False
start=False

def reset(): # 重置遊戲
    global start
    ball.x=ballX0
    ball.y=ballY0
    ball.vx=ballVx0
    ball.vy=ballVy0
    planet.x=planetX0
    planet.y=planetY0
    planet.vx=planetVx0
    planet.vy=planetVy0
    start=False

    # restore original images if they were changed (e.g., pop image)
    if hasattr(ball, 'img'):
        ball.img = pg.image.load('image/space_cat.png').convert_alpha()
        ball.img = pg.transform.scale(ball.img, (ball.Radius*2, ball.Radius*2))

    if hasattr(planet, 'img'):
        planet.img = pg.image.load('image/Jupiter.png').convert_alpha()
        planet.img = pg.transform.scale(planet.img, (planet.Radius*2, planet.Radius*2))
    # reset any per-object surfaces
    ball.tri_surf = pg.Surface((W, H), pg.SRCALPHA)

def changePosition(): # 改變位置
    ball.x+=ball.vx*dt
    ball.y+=ball.vy*dt
    planet.x+=planet.vx*dt
    planet.y+=planet.vy*dt
    if start:apply_gravity(ball,planet,dt)
    if start:apply_gravity(planet,ball,dt)

def apply_gravity(ball, planet,dt, g=G): # 重力影響
    dx = planet.x - ball.x
    dy = planet.y - ball.y #計算位移
    dist = math.sqrt(dx*dx + dy*dy) #計算距離

    accleration = g * planet.mass / (dist * dist) #計算重力加速度

    ax = accleration * (dx / dist)
    ay = accleration * (dy / dist)

    ball.vx += ax*dt #v=v0+at
    ball.vy += ay*dt

def drawDraggingLine(ball): # 畫出拖曳線
    mx, my = pg.mouse.get_pos()

    dx = mx - ball.x
    dy = my - ball.y
    dist = math.sqrt(dx*dx + dy*dy)

    # 距離太短就不畫
    if dist < 1:
        return

    # 單位向量（球 → 滑鼠）
    ux = dx / dist
    uy = dy / dist

    # 垂直單位向量（旋轉 90°）
    px = -uy
    py = ux

    # 等腰三角形的底邊點
    left_x  = ball.x + px * ball.Radius
    left_y  = ball.y + py * ball.Radius

    right_x = ball.x - px * ball.Radius
    right_y = ball.y - py * ball.Radius

    tri_surf = pg.Surface((W, H), pg.SRCALPHA)
    color = (220, 220, 220, 80)
    # 畫三角形（顏色可調）
    pg.draw.polygon(
        tri_surf,
        color,
        [(mx, my), (left_x, left_y), (right_x, right_y)]
    )
    screen.blit(tri_surf, (0, 0))

def draggingball(ball, event, power=POWER): # 處理拖曳與發射
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
        print("mouseDown")


    # 放開左鍵 → 給速度（發射）
    if event.type == pg.MOUSEBUTTONUP and event.button == 1 and dragging:
        dragging = False
        mx, my = pg.mouse.get_pos()

        # 速度 = 從球被拉的位置 → 放手瞬間回彈
        ball.vx = (ball.x - mx) * power
        ball.vy = (ball.y - my) * power
        print(ball.vx, ball.vy)
        start=True
        print("mouseUp")

def end(failureType,b): # 遊戲結束
    global start
    ball.img = pg.image.load('image/space_cat_pop.png')
    ball.img = pg.transform.scale(ball.img, (ball.Radius*2*3, ball.Radius*2*3 ))
    ball.draw(screen)
    ball.vx = 0
    ball.vy = 0
    start = False
    if failureType == "collision":
        if b.type == "target":
            print("You Win! Reached the Target!")
        elif b.type == "planet":
            print("Game Over: Collision detected!")
    
    # elif failureType == "out_of_bounds":
    #     print("Game Over: Ball is out of bounds!")

def iscollide(ball, planet): # 碰撞偵測
    dx = planet.x - ball.x
    dy = planet.y - ball.y
    tolerance = 20 * (planet.type == "planet")   # 容差值，降低遊戲難度，允許些微重疊(只適用於行星)
    distance = math.sqrt(dx*dx + dy*dy)
    return distance + tolerance <= (ball.Radius + planet.Radius) 

def isOutOfBounds(ball):
    return (ball.x < 0 or ball.x > W or ball.y < 0 or ball.y > H)

def showScreen1():
    global dragging, start
    # screen.fill((247,251,247))
    changePosition()
    for event in pg.event.get():
        if event.type== pg.QUIT:
            pg.quit()
        # 處理 reset 按鈕點擊
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            reset_pos = (W - reset_rect.width - reset_margin, reset_margin)
            reset_hitbox = reset_rect.move(reset_pos)
            if reset_hitbox.collidepoint(mx, my):
                reset()
                # don't start dragging when clicking the reset button
                continue
        draggingball(ball, event)

    if dragging: # 如果正在拖曳 就畫出拖曳線 (要先畫拖曳線 再畫球免得被蓋住)
        drawDraggingLine(ball)
    
    for b in ballArray:
        b.draw(screen)

    for b in ballArray:
        if b.type!="ball" and iscollide(ball, b) and start:
            end("collision",b)
    
    # if isOutOfBounds(ball) and start:
    #     end("out_of_bounds", ball)
    
    # draw reset button at top-right
    reset_pos = (W - reset_rect.width - reset_margin, reset_margin)
    screen.blit(reset_img, reset_pos)

    pg.display.flip()


while 1:
    dt=clock.tick(60*TIME)/1000 # 60fps 轉成秒
    screen.blit(background_image, (0, 0))
    showScreen1()

pg.quit()