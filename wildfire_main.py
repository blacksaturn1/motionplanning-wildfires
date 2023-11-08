import pygame
import math
import numpy as np
from math import pi
from valet.robots.ackermann import RobotAckermann
from valet.robots.wumpus import Wumpus
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

start=(100,100,0)

# goal=(550, 650,0)
# goal=(400, 500,0)
# goal=(575, 650,0)
goal=(600, 620,0)
# dims=(800,800)
cells=250
dimensionsForConversion=cells
dims=(dimensionsForConversion,dimensionsForConversion)

running=True

robot=RobotAckermann(start,
            r"./valet/firetruck.png",
            # 35,goal)
            .1*3779.52,goal)

wumpus=Wumpus((700,700,0),
            r"./valet/wumpus.png",
            4*5)


env=Envir(dims,robot,goal)
# env.map.fill(env.black)
env.getrandom_obstacles()
env.draw_environment()
# env.draw_obstacles()
# env.draw_goal()
# env.drawGrid()
robot.draw(env.map)
wumpus.draw(env.map)
# env.write_info()
pygame.display.update()


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
    if nextMove is None:
        
        env.goal=env.getrandom_goal()
        goal=env.goal
        start = lastMove.get_location()
        
        env.draw_environment()
        robot.draw(env.map)
        wumpus.draw(env.map)
        env.write_text_info("Resetting goal...")

        pygame.display.update()
        time.sleep(2)
        lattice = Lattice(start,goal,env.obstacles,robot,env.map,env.write_text_info)
        lastState = lattice.search()
        nextMove = lattice.step2()
        # env.map.fill(env.black)
        # env.draw_obstacles()
        pygame.display.update()
        time.sleep(2)
    else:
        lastMove=nextMove




    robot.drive(nextMove)
    lattice.currentState=nextMove
    time.sleep(.5)
    env.map.fill(env.black)
    env.draw_environment()
    robot.draw(env.map)
    wumpus.draw(env.map)
    env.write_info()
    