
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
import pygame
import math

class State:
    
    def __init__(
        self,
        xy: Tuple[float, float],
        theta: float,
        img
       
    ):
        self.xy=(round(xy[0],2),round(xy[1],2))
        self.x = round(xy[0],2)
        self.y = round(xy[1],2)
        self.theta = round(theta,1)
        self.img = img
        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
        self.rect.width*=1.3
        self.rect.height*=1.3
        self.cost_to_come=0
        self.cost_to_go=0


    def get_location(self):
        return (self.x,self.y,self.theta)


    def get_cost(self,goal):
        x,y,theta = goal
        euclideanCost = ((x- self.x)**2 + (y- self.y)**2)**.5
        # thetaCost = abs(theta-self.theta)
        return euclideanCost  

   
    def __hash__(self):
        return hash((self.x, self.y,self.theta))
    
    @abstractmethod
    def __eq__(self, other):
        return (self.x, self.y,self.theta) == (other.x, other.y,other.theta)
    
    @abstractmethod
    def __lt__(self, other):
        return (self.cost_to_come+self.cost_to_go)  < (other.cost_to_come+other.cost_to_go)