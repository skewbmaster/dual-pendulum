import pygame, os, sys, random
from math import *
from pygame.locals import *
pygame.init()

width=1920
height=1080

r1 = 250
r2 = 275
m1 = 30
m2 = 10
a1 = pi/2
a2 = pi/2
ox = width//2
oy = 300
a1_v = 0
a2_v = 0
g = 1.5
damp = 1

tx1, ty1 = -1, -1
pps = [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]



black = (0, 0, 0)
dark_grey = (35, 35, 37)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 150)
dark_green=(0, 100, 75)
blue = (0, 0, 255)
grey = (200, 200, 200)

Clock = pygame.time.Clock();FPS = 144

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|NOFRAME)
pygame.display.set_caption("Double Pendulum")

backgSurface=pygame.Surface((width,height))

backgSurface.fill(black)

def getColour(deg):
  return 127.5*(sin(radians(deg))+1)

time=90
trail=True
fancyTrail=False
pendulumDisplay=True

while True:

    num1 = (0-g)*(2*m1+m2)*sin(a1)
    num2 = (0-m2)*g*sin(a1-2*a2)
    num3 = (0-2)*sin(a1-a2)*m2
    num4 = a2_v*a2_v*r2+a1_v*a1_v*r1*cos(a1-a2)
    den = r1*(2*m1+m2-m2*cos(2*a1-2*a2))
    a1_a = (num1+num2+num3*num4) / den

    num1 = 2*sin(a1-a2)
    num2 = (a1_v*a1_v*r1*(m1+m2))
    num3 = g*(m1+m2)*cos(a1)
    num4 = a2_v*a2_v*r2*m2*cos(a1-a2)
    den = r2*(2*m1+m2-m2*cos(2*a1-2*a2))
    a2_a = (num1*(num2+num3+num4)) / den

    a1_a /= 2
    a2_a /= 2
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit(),sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                trail = not trail
                
            elif event.key == pygame.K_RETURN:
                backgSurface.fill(black)
                time = 90
                
            elif event.key == pygame.K_BACKSPACE:
                fancyTrail = not fancyTrail
                
            elif event.key == pygame.K_TAB:
                pendulumDisplay = not pendulumDisplay

    if trail:
        screen.blit(backgSurface,(0,0))
    else:
        screen.fill(black)

    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    a1_v *= damp
    a2_v *= damp
    
    
    x1 = ox+r1*sin(a1)
    y1 = oy+r1*cos(a1)

    x2 = x1+r2*sin(a2)
    y2 = y1+r2*cos(a2)

    if pendulumDisplay:
        pygame.draw.lines(screen,white,False,((ox,oy),(x1,y1),(x2,y2)),2)
        pygame.draw.circle(screen,white,(int(x1),int(y1)),7)
        pygame.draw.circle(screen,white,(int(x2),int(y2)),7)
    #pygame.draw.circle(backgSurface,grey,(int(x2),int(y2)),1)

    pygame.display.update()

    if fancyTrail:
        if pps[-1][0] != -1:
            backgSurface.fill(black)
            ppsa = pps
            ppsa.append([x2,y2])
            rt, gt, bt = getColour(time), getColour(time+120), getColour(time+240)
            pygame.draw.aalines(backgSurface, (rt,gt,bt), False, ppsa, 3)
            #pygame.draw.aaline(backgSurface, (int(rt/1.5),int(gt/1.5),int(bt/1.5)), ppsa[1], ppsa[2], 3)
            #pygame.draw.aaline(backgSurface, (rt//2, gt//2, bt//2), ppsa[0], ppsa[1], 3)

        for i in range(len(pps)-1):
            if pps[i][0] != -1:
                pps[i+1][0] = pps[i][0]
                pps[i+1][1] = pps[i][1]
            else:
                break

        pps[0][0] = x2
        pps[0][1] = y2
            
    if tx1!=-1:
        if not fancyTrail:
            pygame.draw.aaline(backgSurface,(getColour(time),getColour(time+120),getColour(time+240)),(tx1,ty1),(x2,y2),3)   
        
    tx1 = x2
    ty1 = y2
        
    Clock.tick(FPS)

    time-=0.25
