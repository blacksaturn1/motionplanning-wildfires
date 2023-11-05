from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
import pygame
from valet.states.state import State

class Robot(ABC):
    
    def draw(self,map:pygame.Surface):
        map.blit(self.rotated,self.rect)
    
    @abstractmethod
    def get_write_info(self):
        pass
    
    @abstractmethod
    def get_neighbors(self,location:Tuple[float,float,float]):
        pass

    @abstractmethod
    def drive(self, nextMove:State):
        pass
