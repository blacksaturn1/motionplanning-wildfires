import pygame
import math
import numpy as np
from math import pi
from valet.robots.ackermann import RobotAckermann
from valet.robots.wumpus import Wumpus
from valet.environment import Envir
from valet.lattice import Lattice
from valet.astar_planner import AStar
from valet.prm_planner import PRM
import time


pygame.init()
# start=(100,450,0)
# start=(100,100,0)
# start=(100,250,0)
# start=(100,100,0)
# start=(550, 550,0)
# start=(100,100,0)
# start=(550, 550,0)

start=(25,25,0)

# goal=(550, 650,0)
# goal=(400, 500,0)
# goal=(575, 650,0)
goal=(600, 620,0)
# dims=(800,800)
cells=250
dimensionsForConversion=cells
dims=(dimensionsForConversion,dimensionsForConversion)

running=True
debug=False
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
env.getrandom_obstacles()


lastime=pygame.time.get_ticks()
# lattice = Lattice(start,goal,env.obstacles,robot,env.map,env.write_text_info)
# lastState = lattice.search()
# time.sleep(2)
wumpus_goal=env.getrandom_obstacle()

total_time_wumpus=0
total_time_firetruck=0
dt=0
prm=PRM(start,goal,env.obstacles,robot,env.map,env.write_text_info)
prm.sample()
prm.create_network()
dt = (pygame.time.get_ticks()-lastime)/1000
total_time_firetruck+=dt
lastime=pygame.time.get_ticks()
# env.goal=wumpus_goal
env.draw_environment()
if debug:
    for node in prm.planner.nodes:
        node.draw(env.map, 10, 1)
env.draw_goal(wumpus_goal,env.yel)
robot.draw(env.map)
wumpus.draw(env.map)
# env.write_info()
pygame.display.update()
wumpusDiscreteGoal = env.convert_x_to_column(wumpus_goal[0],15)-1,env.convert_y_to_row(wumpus_goal[1],15)




lastime=pygame.time.get_ticks()
astar = AStar(wumpus_start,wumpusDiscreteGoal,env.obstacles,wumpus,env.map,env.write_text_info2)
lastState2 = astar.search()
dt = (pygame.time.get_ticks()-lastime)/1000
total_time_wumpus+=dt
lastime=pygame.time.get_ticks()
time.sleep(2)
robot_nextMove=None
robot_lastMove=None
firetruck_running=False
firetruck_waypoint=1
while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    #     robot.move(event)
    dt = (pygame.time.get_ticks()-lastime)/1000
    lastime=pygame.time.get_ticks()
    pygame.display.update()

    if not firetruck_running:
        goal = env.getburning_obstacle()
    if goal is not None:
        env.draw_goal(goal,env.blue)


##########################################################
    lastime=pygame.time.get_ticks()




    if robot_nextMove is None:
        if goal is not None:
            if not firetruck_running:
                if robot_lastMove is not None:
                    start = robot_lastMove.get_location()
                prm.get_path(start,goal)
                firetruck_running=True
                firetruck_waypoint=1
            else:
                firetruck_waypoint+=1
            for node in prm.search.path:
                pygame.draw.circle(env.map, env.blue, node.get_coords(), 5 + 2, width=0)
            pygame.display.update()
            #time.sleep(5)
            if len(prm.search.path)>0 and len(prm.search.path)>firetruck_waypoint:
                goal_local = prm.search.path[firetruck_waypoint].get_coords()
                goal_lattice = (goal_local[0],goal_local[1],0)
                env.draw_goal(goal_lattice,env.white)
                if robot_lastMove is not None:
                    start = robot_lastMove.get_location()
                lattice = Lattice(start,goal_lattice,env.obstacles,robot,env.map,env.write_text_info)
                robot_lastState = lattice.search()
            else:
                firetruck_running=False
                firetruck_waypoint=1
                env.obstacle_state[goal[2]]=env.green
                goal=None
    else:
        robot_lastMove=robot_nextMove
    
    if goal is not None and len(prm.search.path)>0:
        robot_nextMove = lattice.step2()
        lattice.currentState=robot_nextMove
        # if robot_nextMove is None and goal is not None and firetruck_waypoint==1:
        #     env.obstacle_state[goal[2]]=env.green
    
    if robot_nextMove is not None:
        robot_lastMove=robot_nextMove

    robot.drive(robot_nextMove)

    dt = (pygame.time.get_ticks()-lastime)/1000
    total_time_firetruck+=dt


##############################################################################
    lastime=pygame.time.get_ticks()

    nextMove2 = astar.step2()
    wumpus.drive(nextMove2)
    #astar.currentState=nextMove2
    
    
    time.sleep(.1)
    env.draw_environment()
    if debug:
        for node in prm.planner.nodes:
            node.draw(env.map, 15, 1)
    robot.draw(env.map)
    wumpus.draw(env.map)
    env.draw_goal(wumpus_goal,env.yel)
    env.write_info()
    if nextMove2.c==wumpusDiscreteGoal[0] and nextMove2.r==wumpusDiscreteGoal[1]:
        env.obstacle_state[wumpus_goal[2]]=env.red
        # wumpus.drive(nextMove2)
        # TODO: get a non-burning obstacle
        wumpus_goal=env.getrandom_obstacle()
        wumpusDiscreteGoal = env.convert_x_to_column(wumpus_goal[0],15)-1,env.convert_y_to_row(wumpus_goal[1],15)
        env.draw_environment()
        robot.draw(env.map)
        wumpus.draw(env.map)
        env.draw_goal(wumpus_goal,env.yel)
        env.write_info()
        pygame.display.update()
        #wumpusDiscreteGoal=(35,35)
        wumpus_start = (nextMove2.c,nextMove2.r)
        astar = AStar(wumpus_start,wumpusDiscreteGoal,env.obstacles,wumpus,env.map,env.write_text_info2)
        lastState2 = astar.search()
        pygame.display.update()
    else:
        lastMove2=nextMove2
    
    dt = (pygame.time.get_ticks()-lastime)/1000
    total_time_wumpus+=dt


    


    