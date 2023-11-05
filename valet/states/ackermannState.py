from typing import List, Optional, Tuple
import pygame
import math
from valet.states.state import State

class AckermannState(State):

    def __init__(
        self,
        xy: Tuple[float, float],
        theta: float,
        psi: float,
        v: float,
        img
    ):
        super().__init__(xy,theta,img)
        self.psi = round(psi,1)
        self.v=v
        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
        self.rect.width*=1.3
        self.rect.height*=1.3
        self.cost_to_come=0
        self.cost_to_go = 0
    
    