import pygame
import math
from math import pi
from valet.environment import Envir
from valet.lattice import Lattice
from valet.robots.diffdrive import RobotDiff
import time


pygame.init()

start=(100,100,0)
goal=(600, 620,0)
dims=(800,800)

robot=RobotDiff(start,
            r"./valet/diff_drive.png",
            .1*3779.52)

env=Envir(dims,robot,goal)
env.map.fill(env.black)
env.draw_obstacles()
env.draw_goal()
robot.draw(env.map)
# env.write_info()
pygame.display.update()

running=True


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
    time.sleep(.25)
    env.map.fill(env.black)
    env.draw_obstacles()
    env.draw_goal()
    robot.draw(env.map)
    env.write_info()



  