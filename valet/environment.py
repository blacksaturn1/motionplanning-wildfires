import pygame
import random
import math
from valet.robots.robot import Robot
from typing import List

class Envir:
    def __init__(self,dimensions,robot:Robot, goal):
        #colors
        self.robot=robot
        self.black=(0,0,0)
        self.white=(255,255,255)
        self.green=(0,255,0)
        self.blue=(0,0,255)
        self.red=(255,0,0)
        self.yel=(255,255,0)
        # map dim
        self.height = dimensions[0]
        self.width = dimensions[1]
        # window settings
        pygame.display.set_caption("Robot")
        self.map=pygame.display.set_mode((self.width,self.height))
        self.font=pygame.font.Font('freesansbold.ttf',25)
        self.text = self.font.render('default',True,self.white,self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center=(dimensions[1]-600,dimensions[0]-100)

        self.goal = goal
        # obstacles
        self.obstacles:list[pygame.Rect] = [
            # pygame.Rect(100, 100, 50, 50),
            # pygame.Rect(400, 400, 100, 100),
            # pygame.Rect(400, 600, 50, 50),
            pygame.Rect(300, 200, 200, 200),  
            pygame.Rect(200, 600, 340, 40),
            pygame.Rect(650, 600, 150, 40),
            pygame.Rect(0, 650, 800, 160),
        ]
        self.obstacleGrid=[]
        # Initialize the grid attribute
        self.grid_size = 20
        self.grid_width = dimensions[1] // self.grid_size
        self.grid_height = dimensions[0] // self.grid_size
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def write_info(self):
        txt = self.robot.get_write_info()
        self.text=self.font.render(txt,True,self.white,self.black)
        self.map.blit(self.text,self.textRect)

    def write_text_info(self,text):
        self.text=self.font.render(text,True,self.yel,self.black)
        self.map.blit(self.text,self.textRect)



    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.map, self.red, obstacle)

    def draw_goal(self):
        pygame.draw.circle(self.map, self.green,[self.goal[0],self.goal[1]],15,1)

    def getrandom_obstacles(self,coveragePer=.10):
        percentageObstacle = 0
        obstacleAmount_goal=250*5*250*5*coveragePer
        obstacleAmount_current=0
        self.obstacles=[]
        while  obstacleAmount_current<=obstacleAmount_goal*.96:
            obstacleAmount=math.floor(math.sqrt((obstacleAmount_goal-obstacleAmount_current)/16))
            getRandomLocationX = 200+random.randrange(0,5*250-200,1)
            getRandomLocationY = 200+random.randrange(0,5*250-200,1)
            self.obstacles.append(pygame.Rect(getRandomLocationX, getRandomLocationY, obstacleAmount, obstacleAmount))
            obstacleAmount_current+=obstacleAmount*obstacleAmount
            percentageObstacle=obstacleAmount_current / obstacleAmount_goal
         
         
    def getrandom_goal(self):
         return (random.randrange(0,5*250,1), random.randrange(0,5*250,1),0)