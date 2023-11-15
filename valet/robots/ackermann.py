import pygame
import math
from math import pi
from valet.states.ackermannState import AckermannState
from valet.robots.robot import Robot
from typing import List, Optional, Tuple


class RobotAckermann(Robot):
    def __init__(self,startpos, robotImg,width,goalPositionAndOrientation) -> None:
        self.m2p=35#3779.52
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.x_goal=goalPositionAndOrientation[0]
        self.y_goal=goalPositionAndOrientation[1]
        self.orientation=goalPositionAndOrientation[2]
        self.theta=0
        self.v=0.00 * self.m2p
        self.psi = 0
        self.psi_max=60
        self.maxspeed=45#0.02 * self.m2p
        self.minspeed=0.01 * self.m2p
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.l=2.8 *25#* 15#* 35
        self.dt = 0.75
        self.distanceToGoal=0.0
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
 

    def get_write_info(self):
        txt = f"V = {int(self.v)} PSI={int(self.psi)} THETA={int(self.theta)} DTG: {float(self.distanceToGoal)}"
        return txt
    
    def get_neighbors(self,location:Tuple[float,float,float]):
        neighbors:List[AckermannState]=[]
        psi_increment = 5
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
        self.theta =nextMove.theta
        self.x=nextMove.x
        self.y=nextMove.y
        
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
        self.distanceToGoal=((self.x_goal- self.x)**2 + (self.y_goal- self.y)**2)**.5

    # def move(self,event=None):
    #     if event is not None:
    #         if event.type==pygame.KEYDOWN:
    #             if event.key==pygame.K_UP:
    #                 self.v+=0.001*self.m2p
    #             elif event.key == pygame.K_DOWN:
    #                 self.v-=0.001*self.m2p
    #             elif event.key == pygame.K_RIGHT:
    #                 self.psi-=10
    #                 if self.psi<=-50:
    #                     self.psi=-50

    #             elif event.key == pygame.K_LEFT:
                    
    #                 self.psi+=10
    #                 if self.psi>=50:
    #                     self.psi=50    
    #             elif event.key == pygame.K_KP5:
    #                 self.v=0                    
    #     self.x+=self.v*math.cos(self.theta)*self.dt
    #     # y is opposite direction of screen
    #     self.y-=self.v*math.sin(self.theta)*self.dt
        
    #     thetadelta=((self.v/self.l)*math.tan(math.radians(self.psi)))*self.dt #%(360)
    #     # if self.psi != 0:
            
    #     # else:
    #     #     thetadelta=0
    #     #thetadelta = thetadelta % (2*pi)
    #     if thetadelta > math.pi:
    #             thetadelta = (2*math.pi) - thetadelta
    #             thetadelta = -1 * thetadelta
        

    #     self.theta += thetadelta

    #     if self.theta>2*pi:
    #         self.theta-=2*pi
    #     if self.theta<(-2*pi):
    #         self.theta+=2*pi
            
        
            
    #     #self.rotated=self.img
    #     self.rotated=pygame.transform.rotozoom(self.img,
    #                                            math.degrees(self.theta),1)
    #     self.rect = self.rotated.get_rect(center=(self.x,self.y))
