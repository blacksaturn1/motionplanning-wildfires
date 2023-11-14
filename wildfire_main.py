import pygame
import math
import numpy as np
from math import pi
from valet.robots.ackermann import RobotAckermann
from valet.robots.wumpus import Wumpus
from valet.environment import Envir
from valet.lattice import Lattice
from valet.astar_planner import AStar
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
wumpus_start=(49,49)
wumpus_start=(48,48)

wumpus=Wumpus(wumpus_start,
            r"./valet/wumpus_13.png",
            3*5)


env=Envir(dims,robot,goal)
# env.map.fill(env.black)

env.getrandom_obstacles()




dt=0
lastime=pygame.time.get_ticks()
# lattice = Lattice(start,goal,env.obstacles,robot,env.map,env.write_text_info)
# lastState = lattice.search()
# time.sleep(2)


wumpus_goal=env.getrandom_obstacle()
# env.goal=wumpus_goal
env.draw_environment()
env.draw_goal(wumpus_goal,env.red)
env.draw_obstacles()
# env.draw_goal()
# env.drawGrid()
robot.draw(env.map)
wumpus.draw(env.map)
# env.write_info()
pygame.display.update()
#time.sleep(5)

wumpusDiscreteGoal = env.convert_x_to_column(wumpus_goal[0],15)-1,env.convert_y_to_row(wumpus_goal[1],15)
#wumpusDiscreteGoal=(35,35)

astar = AStar(wumpus_start,wumpusDiscreteGoal,env.obstacles,wumpus,env.map,env.write_text_info2)
lastState2 = astar.search()
time.sleep(2)

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    #     robot.move(event)
    dt = (pygame.time.get_ticks()-lastime)/1000
    lastime=pygame.time.get_ticks()
    pygame.display.update()
    
    # #robot.move()
    # nextMove = lattice.step2()
    # if nextMove is None:
        
    #     env.goal=env.getrandom_goal()
    #     goal=env.goal
    #     start = lastMove.get_location()
        
    #     env.draw_environment()
    #     robot.draw(env.map)
    #     wumpus.draw(env.map)
    #     env.write_text_info("Resetting goal...")

    #     pygame.display.update()
    #     time.sleep(2)
    #     lattice = Lattice(start,goal,env.obstacles,robot,env.map,env.write_text_info)
    #     lastState = lattice.search()
    #     nextMove = lattice.step2()
    #     # env.map.fill(env.black)
    #     # env.draw_obstacles()
    #     pygame.display.update()
    #     time.sleep(2)
    # else:
    #     lastMove=nextMove
    #robot.drive(nextMove)
    #lattice.currentState=nextMove

    nextMove2 = astar.step2()
    if nextMove2.c==wumpusDiscreteGoal[0] and nextMove2.r==wumpusDiscreteGoal[1]:
        env.obstacle_state[wumpus_goal[2]]=env.red
        # env.goal=env.getrandom_obstacle()
        # goal=env.goal
        # start = lastMove2.get_location()
        
        # env.draw_environment()
        # robot.draw(env.map)
        # wumpus.draw(env.map)
        # env.write_text_info("Resetting goal...")

        # pygame.display.update()
        # time.sleep(2)
        # astar = AStar(start,goal,env.obstacles,robot,env.map,env.write_text_info)
        # lastState = astar.search()
        # nextMove = astar.step2()

        # env.map.fill(env.black)
        # env.draw_obstacles()
        pygame.display.update()
        time.sleep(2)
    else:
        lastMove2=nextMove2

    wumpus.drive(nextMove2)
    #astar.currentState=nextMove2
    
    
    time.sleep(1)
    env.map.fill(env.black)
    env.draw_environment()
    robot.draw(env.map)
    wumpus.draw(env.map)
    env.draw_goal(wumpus_goal,env.red)
    env.write_info()
    