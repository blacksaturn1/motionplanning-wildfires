import pygame
from valet.robots.robot import Robot
from typing import List, Optional, Tuple
from valet.states.state import State

import math

class Wumpus(Robot):
    def __init__(self,startpos, robotImg,width) -> None:
        self.m2p=3779.52
        self.w=width
        self.x=startpos[0]+10
        self.y=startpos[1]+10
        self.theta=0
        self.vl=0.00 * self.m2p
        self.vr=0.00 * self.m2p
        self.maxspeed=250#0.02 * self.m2p
        self.minspeed=0.01 * self.m2p
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
        self.dt = 0.75
    def draw(self,map:pygame.Surface):
        map.blit(self.rotated,self.rect)
    
    def move(self,event=None):
        if event is not None:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_KP4:
                    self.vl+=0.001*self.m2p
                elif event.key == pygame.K_KP1:
                    self.vl-=0.001*self.m2p
                elif event.key == pygame.K_KP6:
                    self.vr+=0.001*self.m2p
                elif event.key == pygame.K_KP3:
                    self.vr-=0.001*self.m2p
                elif event.key == pygame.K_KP8:
                    self.vr+=0.001*self.m2p
                    self.vl+=0.001*self.m2p
                elif event.key == pygame.K_KP5:
                    self.vr=0
                    self.vl=0
        self.x+=(self.vl + self.vr)/2*math.cos(self.theta)*self.dt
        # y is opposite direction of screen
        self.y-=(self.vl + self.vr)/2*math.sin(self.theta)*self.dt
        self.theta += (self.vr-self.vl)/self.w*self.dt
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
    
    def get_write_info(self):
        txt = f"Vl = {self.vl} Vr = {self.vr} THETA={self.theta}"
        return txt
    
    def get_neighbors(self,location:Tuple[float,float,float]):
        neighbors:List[State]=[]
        stepRange=10
        for vl in range(-self.maxspeed,self.maxspeed+stepRange,stepRange):
            for vr in range(-self.maxspeed,self.maxspeed+stepRange,stepRange):
                x,y,theta = location
                x+=(vl + vr)/2*math.cos(theta)*self.dt
                # y is opposite direction of screen
                y-=(vl + vr)/2*math.sin(theta)*self.dt
                theta += (vr-vl)/self.w*self.dt
                state = State((x,y),theta,self.img)
                neighbors.append(state)
        return neighbors

    def drive(self, nextMove:State):
        if nextMove is None:
            return
        self.theta =nextMove.theta
        self.x=nextMove.x
        self.y=nextMove.y
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))