import pygame
import math
from math import pi
from valet.states.ackermannState import AckermannState
from valet.robots.robot import Robot
from typing import List, Optional, Tuple


class RobotTrailer(Robot):
    def __init__(self,startpos, robotImg,width,goalPositionAndOrientation) -> None:
        self.m2p=25#3779.52
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.x2=startpos[0]-70
        self.y2=startpos[1]
        self.x_goal=goalPositionAndOrientation[0]
        self.y_goal=goalPositionAndOrientation[1]
        self.orientation=goalPositionAndOrientation[2]
        self.theta=0
        self.theta2=0
        self.v=0.00 * self.m2p
        self.psi = 0
        self.psi_max=60
        self.maxspeed=100#0.02 * self.m2p
        self.minspeed=0.01 * self.m2p
        self.img = pygame.image.load(robotImg[0])
        self.img2 = pygame.image.load(robotImg[1])
        self.rotated = self.img
        self.rotated2 = self.img2
        self.l = 2.8 *self.m2p
        self.l2 = 20 *self.m2p
        self.dt = 0.4
        self.distanceToGoal=0.0
        
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
        self.rect2=self.rotated2.get_rect(center=(self.x-80,
                                                self.y))
        
    def draw(self,map:pygame.Surface):
        map.blit(self.rotated,self.rect)
        map.blit(self.rotated2,self.rect2)
        pygame.draw.line(map, (255, 255, 0), (self.x,self.y), (self.x2,self.y2), width=3)

    def get_write_info(self):
        txt = f"V = {int(self.v)} PSI={int(self.psi)} THETA={int(self.theta)} THETA2={int(self.theta2)} DTG: {float(self.distanceToGoal)}"
        return txt
    
    def get_neighbors(self,location:Tuple[float,float,float]):
        neighbors:List[AckermannState]=[]
        psi_increment = 5
        # x,y,theta = location
        # distanceToGoal = ((self.x_goal- x)**2 + (self.y_goal- y)**2)**.5
        for v in [self.maxspeed,-self.maxspeed]:
            for psi in range (-self.psi_max,self.psi_max+psi_increment,psi_increment):
                x,y,theta = location
                thetadelta=((v/self.l)*math.tan(math.radians(psi)))*self.dt
                thetadelta = thetadelta % (2*pi)
                if thetadelta > math.pi:
                    thetadelta = (2*math.pi) - thetadelta
                    thetadelta = -1 * thetadelta
                
                theta = self.theta + thetadelta
                x+=v*math.cos(theta)*self.dt
                # y is opposite direction of screen
                y-=v*math.sin(theta)*self.dt
                state = AckermannState((x,y),theta,psi,v,self.img)
                neighbors.append(state)
        return neighbors

    def drive(self, nextMove:AckermannState):
        if nextMove is None:
            return
        self.v=nextMove.v
        self.psi = nextMove.psi
        self.theta = nextMove.theta
        self.x=nextMove.x
        self.y=nextMove.y
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
        
        self.theta2+=self.v/90*math.sin(self.theta-self.theta2)*self.dt
        
        # self.theta2=math.atan2(self.y2 - self.y,self.x2 - self.x)
        # self.theta2=math.atan2(self.y2 - self.y,self.x2 - self.x)

        # self.theta2 = self.theta2 % (2*pi)
        # if self.theta2 > math.pi:
        #         self.theta2 = (2*math.pi) - self.theta2
        #         self.theta2 = -1 * self.theta2

        xdiff = 3*self.m2p*math.cos(self.theta2)
        ydiff = -3*self.m2p*math.sin(self.theta2)
        self.x2, self.y2 = (self.x - xdiff, self.y - ydiff)

        self.rotated2=pygame.transform.rotozoom(self.img2,
                                               math.degrees(self.theta2),1)
        self.rect2 = self.rotated.get_rect(center=(self.x2,self.y2))

        self.distanceToGoal=((self.x_goal- self.x)**2 + (self.y_goal- self.y)**2)**.5
