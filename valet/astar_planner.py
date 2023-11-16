from valet.states.discrete_state import DiscreteState
from typing import List, Optional, Tuple
import pygame
import math
from queue import PriorityQueue
class AStar:

    def __init__(self,location:Tuple[float,float],goal:Tuple[float,float],
                 obstacleGrid,robot:DiscreteState,display, write_info:callable) -> None:
        self.currentLocation=location
        self.goal:Tuple[float,float]=goal
        self.neighbors:List[DiscreteState]=[]
        self.path: dict[DiscreteState,DiscreteState]={}
        self.network_path: dict[DiscreteState,List[DiscreteState]]={}
        self.cost: dict[DiscreteState,float]={}
        self.obstacles:list[pygame.Rect] = obstacleGrid
        self.queue:PriorityQueue[DiscreteState] = PriorityQueue()
        self.robot = robot
        x,y=self.currentLocation
        self.firstState = DiscreteState((x,y),self.robot.img)
        self.firstState.cost_to_come = 0
        self.firstState.cost_to_go=self.firstState.get_cost(self.goal)
        self.currentState = self.firstState
        self.lastState=None
        self.display = display
        self.write_info=write_info
        self.robot.maxspeed=30
        

    def add_neighbors(self, neighbors):
        self.neighbors=[]
        for neighbor in neighbors:
            if self.isCollision(neighbor):
                continue
            self.neighbors.append(neighbor)

    def search(self):
        # cost = 9999
        x,y=self.currentLocation
        # previousLocation=self.currentLocation
        startState = self.firstState
        # lowestCostState=startState
        self.queue.put(startState)
        state=startState
        counter=0
        while not self.goalCheck(state) and self.queue.not_empty:
            counter+=1
            self.write_info("Planner iteration: {}".format(counter))
            state = self.queue.get()
            # cost = state.cost_to_go
            
            state_location = state.get_location()
            neighbors = self.robot.get_neighbors(state_location)
            for nextState in neighbors:
                reward = 1
                nextState.cost_to_come = (state.cost_to_come+
                                          nextState.get_cost(state_location))
                nextState.cost_to_go=nextState.get_cost(self.goal)*reward
                if self.isCollision(nextState):
                    continue
                if nextState not in self.path:
                    self.path[nextState]=state
                    self.queue.put(nextState)
                    position = nextState.xx,nextState.yy
                    self.display.fill((255, 0, 0), (position, (2, 2)))
                    pygame.event.get()
                    pygame.display.update()
                # else:
                #     print("Duplicate")
            # if counter >1 and counter%500==0:
            #     break

        self.lastState = state
        return state
        

    def goalCheck(self,state:DiscreteState):
        distanceToGoal = self.calculateCostToGoal(state)
        # thetaDiff = abs(self.goal[2]-state.theta)
        #return distanceToGoal<=0 #and thetaDiff<=(math.pi/8)
        if self.goal[0]==state.c and self.goal[1]==state.r:
            return True
        return False


    def plan(self):
        for neighbor in self.neighbors:
            self.cost[neighbor]=self.calculateCost(neighbor)

    def isCollision(self,state:DiscreteState):
        for obstacle in self.obstacles:
            if obstacle.colliderect(state.rect):
                return True
            
        return False
    
    def step(self):
        lowestCost=9999
        lowestCostNeighbor=None
        for state,value in self.cost.items():
            if value<lowestCost:
                if not self.isCollision(state):
                    lowestCost=value 
                    lowestCostNeighbor=state
        self.cost={}
        self.neigbors={}
        return lowestCostNeighbor

    def step2(self):
        if self.currentState is None:
            return None
        if self.currentState==self.lastState:
            return self.currentState
        
        currentState = self.lastState
        previousState = currentState

        while previousState!=self.currentState:
            currentState=previousState
            previousState=self.path[currentState]
            
        self.currentState=currentState
   
        # previousState=self.path[self.currentState]
        # self.currentState=previousState

        return previousState
    
    def calculateCostToGoal(self,state:DiscreteState):
        euclideanCost = ((self.goal[0]- state.c)**2 + (self.goal[1]- state.r)**2)**.5
        # thetaCost = abs(self.goal[2]-state.theta)
        return euclideanCost #*1.1 + thetaCost*.1



