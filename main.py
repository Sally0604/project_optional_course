# 1. go to "cmd" and input "python"
# 2. it will ask you to install python, just install
# 3. after installation, input "pip install pygame"
# 4. there you go
import pygame as pg# finally!!! ahhahhaaahah
pg.init()
screen=pg.display.set_mode((800,600))
pg.display.set_caption("多元選修")
image_tomato=pg.image.load('image/tomato.png')
pg.display.set_icon(image_tomato)
running=True
while running:
    for event in pg.event.get():
        if event.type== pg.QUIT:
            running=False
    screen.fill((255,255,255))
    pg.display.flip()
pg.quit()