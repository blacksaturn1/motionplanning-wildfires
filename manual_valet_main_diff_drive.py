import pygame
import math
from math import pi
from valet.robots.diffdrive import RobotDiff
from valet.environment import Envir

pygame.init()
start=(200,200)
dims=(800,800)
running=True

robot=RobotDiff(start,
            r"./valet/diff_drive.png",
            .1*3779.52)
robot.dt = .005
env=Envir(dims,robot,(0,0,0))

dt=0
lastime=pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        robot.move(event)
    dt = (pygame.time.get_ticks()-lastime)/1000
    lastime=pygame.time.get_ticks()
    pygame.display.update()
    env.map.fill(env.black)
    robot.move()
    robot.draw(env.map)

    env.write_info()
  