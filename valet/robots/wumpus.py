import pygame
from valet.robots.robot import Robot
from typing import List, Optional, Tuple
from valet.states.discrete_state import DiscreteState

import math

class Wumpus(Robot):
    def __init__(self,startpos, robotImg,width) -> None:
        self.m2p=3779.52
        self.w=width

        self.x=self.convert_column_to_x(startpos[0],15)
        self.y=self.convert_row_to_y(startpos[1],15)
        test_c = self.convert_x_to_column(self.x,15)
        test_r = self.convert_y_to_row(self.y,15)
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
    
    def convert_column_to_x(self,column, square_width):
        x = 1 * (square_width/2.0 ) + square_width * column
        return x

    def convert_row_to_y(self,row, square_height):
        y = 1 * (square_height/2.0) + square_height * row 
        return y
    
    def convert_x_to_column(self,x, square_width):
        
        column = int(x /square_width)

        return column

    def convert_y_to_row(self,y, square_height):
        row = int(y /(square_height))
        return row
    
    
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
    
    def get_neighbors(self,location:Tuple[float,float]):
        neighbors:List[State]=[]
        stepRange=10
        for uldr in range(0,4,1):
            x,y = location
            #up
            if uldr == 0:
                y-=1
            elif uldr == 1:
                x+=1
            elif uldr == 2:
                y+=1
            elif uldr == 3:
                x-=1
            if (x >=0 and y>=0) and (x <=49 and y<=49):
                state = DiscreteState((x,y),self.img)
                neighbors.append(state)
        return neighbors

    def drive(self, nextMove:DiscreteState):
        if nextMove is None:
            return
        #self.theta =nextMove.theta
        #self.x=nextMove.x+10
        #self.y=nextMove.y+10
        self.x=nextMove.xx
        self.y=nextMove.yy
        self.rotated=pygame.transform.rotozoom(self.img,0,1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))