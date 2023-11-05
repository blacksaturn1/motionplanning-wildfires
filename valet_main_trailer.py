import pygame
import math
from math import pi
from valet.robots.trailer import RobotTrailer
from valet.environment import Envir
from valet.lattice import Lattice
import time


pygame.init()
# start=(100,450,0)
# start=(100,100,0)
# start=(100,250,0)
# start=(100,100,0)
# start=(550, 550,0)
# start=(100,100,0)
# start=(550, 550,0)

start=(150,100,0)

# goal=(550, 650,0)
# goal=(400, 500,0)
# goal=(575, 650,0)

goal=(250, 100,0)
goal=(600, 620,0)
goal=(250, 250,0)
goal=(250, 450,0)
goal=(600, 620,0)
cells=250
dimensionsForConversion=5*cells
dims=(dimensionsForConversion,dimensionsForConversion)
running=True

robot=RobotTrailer(start,
            (r"./valet/ackermann2.png",r"./valet/trailer.png"),
            # 35,goal)
            .1*3779.52,goal)

env=Envir(dims,robot,goal)
env.obstacles:list[pygame.Rect] = [
            pygame.Rect(300, 200, 200, 200),  
            pygame.Rect(200, 600, 200, 40),
            pygame.Rect(0, 650, 800, 160),
            pygame.Rect(650, 600, 150, 40),
        ]



env.getrandom_obstacles()
# env.obstacles:list[pygame.Rect] = [
#             pygame.Rect(300, 200, 200, 200),  
#             pygame.Rect(200, 600, 200, 40),
#             pygame.Rect(0, 650, 800, 160),
#             pygame.Rect(650, 600, 150, 40),
#         ]
env.map.fill(env.black)
env.draw_obstacles()
env.draw_goal()
robot.draw(env.map)
pygame.display.update()
time.sleep(10)
# robot=RobotTrailer(start,
#             (r"./valet/ackermann2.png",r"./valet/trailer.png"),
#             # 35,goal)
#             .1*3779.52,goal)
# robot.draw(env.map)
# pygame.display.update()
# time.sleep(2)

dt=0
lastime=pygame.time.get_ticks()
lattice = Lattice(start,goal,env.obstacles,robot,env.map,env.write_text_info)
lastState = lattice.search()
time.sleep(2)


while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    #     robot.move(event)
    dt = (pygame.time.get_ticks()-lastime)/1000
    lastime=pygame.time.get_ticks()
    pygame.display.update()
    
    #robot.move()
    nextMove = lattice.step2()
    robot.drive(nextMove)
    lattice.currentState=nextMove
    time.sleep(.15)
    env.map.fill(env.black)
    env.draw_obstacles()
    env.draw_goal()

    robot.draw(env.map)
    env.write_info()
    