import pygame
import random
import math
from valet.robots.robot import Robot
from typing import List
import numpy as np
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
        self.pixels_per_meter=3
        # window settings
        pygame.display.set_caption("Robot")
        self.window_width = self.width*self.pixels_per_meter
        self.window_height = self.height*self.pixels_per_meter
        self.map=pygame.display.set_mode((self.window_width ,self.window_height))
        self.font=pygame.font.Font('freesansbold.ttf',25)
        self.text = self.font.render('default',True,self.white,self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center=(dimensions[1]*self.pixels_per_meter-600,dimensions[0]*self.pixels_per_meter-100)
        self.random_number_generator = np.random.default_rng(seed=42)
        self.text2 = self.font.render('default',True,self.white,self.black)
        self.textRect2 = self.text.get_rect()
        self.textRect2.center=(dimensions[1]*self.pixels_per_meter-600,dimensions[0]*self.pixels_per_meter-200)

        self.goal = goal
        # obstacles
        self.obstacles:list[pygame.Rect] = [
            # pygame.Rect(100, 100, 50, 50),
            # pygame.Rect(400, 400, 100, 100),
            # pygame.Rect(400, 600, 50, 50),
            pygame.Rect(300, 200, 200, 200),  
            pygame.Rect(200, 600, 340, 40),
            pygame.Rect(650, 600, 150, 40),
            # pygame.Rect(0, 650, 800, 160),
        ]
        self.obstacle_state={}
        for idx,obstacle in enumerate(self.obstacles):
            self.obstacle_state[idx] = self.green

        #self.burning_obstacles=[]
        #self.extinguished_obstacles=[]

        # self.obstacleGrid=[]
        # # Initialize the grid attributes for Wumpus
        # self.grid_size = 20
        # self.grid_width = dimensions[1] // self.grid_size
        # self.grid_height = dimensions[0] // self.grid_size
        # self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def write_info(self):
        txt = self.robot.get_write_info()
        self.text=self.font.render(txt,True,self.white,self.black)
        self.map.blit(self.text,self.textRect)

    def write_text_info(self,text):
        self.text=self.font.render(text,True,self.yel,self.black)
        self.map.blit(self.text,self.textRect)

    def write_text_info2(self,text):
        self.text2=self.font.render(text,True,self.yel,self.black)
        self.map.blit(self.text2,self.textRect2)

    def draw_obstacles(self):
        for index,obstacle in enumerate(self.obstacles):
            color = self.obstacle_state[index]
            pygame.draw.rect(self.map, color, obstacle)

    def draw_goal(self,goal=(0,0),color=(0,255,0)):
        pygame.draw.circle(self.map, color,[goal[0],goal[1]],30,3)

    def getrandom_obstacles(self,coveragePer=.10):
        percentageObstacle = 0
        obstacleAmount_goal=self.height*self.pixels_per_meter*self.width*self.pixels_per_meter*coveragePer
        obstacleAmount_current=0
        self.obstacles=[]
        minObstacle_amount=self.pixels_per_meter*5
        while  obstacleAmount_current<=obstacleAmount_goal*.99:
            #obstacleAmount=math.floor(math.sqrt((obstacleAmount_goal-obstacleAmount_current)/16))
            obstacleAmountCount = self.random_number_generator.choice(range(1,5,1))
            obstacleAmount = minObstacle_amount * obstacleAmountCount
            obstacleAmountCount = self.random_number_generator.choice(range(1,5,1))
            obstacleAmount2 = minObstacle_amount * obstacleAmountCount
            getRandomLocationX = 20+random.randrange(0,self.pixels_per_meter*250-obstacleAmount,1)
            getRandomLocationY = 20+random.randrange(0,self.pixels_per_meter*250-obstacleAmount,1)



            rect = pygame.Rect(getRandomLocationX, getRandomLocationY, obstacleAmount, obstacleAmount2)
            if self.isCollision(rect):
                continue
            self.obstacles.append(rect)
            obstacleAmount_current+=obstacleAmount*obstacleAmount
            percentageObstacle=obstacleAmount_current / obstacleAmount_goal
        
        self.obstacle_state={}
        for idx,obstacle in enumerate(self.obstacles):
            self.obstacle_state[idx] = self.green
         
         
    def getrandom_goal(self):
         return (random.randrange(0,5*250,1), random.randrange(0,5*250,1),0)
    
    def getrandom_obstacle(self):
         obstacle_index = self.random_number_generator.choice(range(0,len(self.obstacles),1))
         obstacle = self.obstacles[obstacle_index]
         return (obstacle.x,obstacle.y,obstacle_index)
         
    
    def isCollision(self,rect):
        for obstacle in self.obstacles:
            if obstacle.colliderect(rect):
                return True
        return False
    
    def drawGrid(self):
        blockSize = self.pixels_per_meter * 5 #Set the size of the grid block
        for x in range(0, self.window_width, blockSize):
            for y in range(0, self.window_height, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize,)
                pygame.draw.rect(self.map, self.white, rect, 1)


    def draw_environment(self):
        self.map.fill(self.black)
        self.drawGrid()
        self.draw_obstacles()
        # self.draw_goal()
        
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