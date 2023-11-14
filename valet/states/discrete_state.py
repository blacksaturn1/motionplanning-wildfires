
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
import pygame
import math
from valet.states.state import State

class DiscreteState(State):
    
    def __init__(
        self,
        xy: Tuple[float, float],
        img
       
    ):
        self.xy=(round(xy[0],2),round(xy[1],2))
        self.c = round(xy[0],2)
        self.r = round(xy[1],2)
        # self.theta = round(theta,1)
        self.img = img
        self.rotated = pygame.transform.rotozoom(self.img,0,1)
        self.xx = self.convert_column_to_x(self.c)
        self.yy = self.convert_column_to_x(self.r)
        
        self.rect = self.rotated.get_rect(center=(self.xx,self.yy))
        self.rect.width*=1
        self.rect.height*=1
        self.cost_to_come=0
        self.cost_to_go=0


    def get_location(self):
        return (self.c,self.r)


    def get_cost(self,goal):
        x,y = goal
        euclideanCost = ((x- self.r)**2 + (y- self.c)**2)**.5
        return euclideanCost  

   
    def __hash__(self):
        return hash((self.c, self.r))
    
    @abstractmethod
    def __eq__(self, other):
        return (self.c, self.r) == (other.c, other.r)
    
    @abstractmethod
    def __lt__(self, other):
        return (self.cost_to_come+self.cost_to_go)  < (other.cost_to_come+other.cost_to_go)
    

    def convert_column_to_x(self,column, square_width=15):
        x = 1 * (square_width/2.0 ) + square_width * column
        return x

    def convert_row_to_y(self,row, square_height=15):
        y = 1 * (square_height/2.0) + square_height * row 
        return y
    
    def convert_x_to_column(self,x, square_width=15):
        
        column = int(x /square_width)

        return column

    def convert_y_to_row(self,y, square_height=15):
        row = int(y /(square_height))
        return row