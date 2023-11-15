from valet.states.state import State
from typing import List, Optional, Tuple
import pygame
import math
from queue import PriorityQueue
from valet.prm import ProbabilisticRoadmap
from valet.search import AStar

class PRM:

    def __init__(self,location:Tuple[float,float,float],goal:Tuple[float,float,float],
                 obstacleGrid,robot,display, write_info:callable) -> None:
        self.currentLocation=location
        self.goal:Tuple[float,float,float]=goal
        self.neighbors:List[State]=[]
        self.path: dict[State,State]={}
        self.network_path: dict[State,List[State]]={}
        self.cost: dict[State,float]={}
        self.obstacles:list[pygame.Rect] = obstacleGrid
        self.queue:PriorityQueue[State] = PriorityQueue()
        self.robot = robot
        x,y,theta=self.currentLocation
        self.firstState = State((x,y),theta,self.robot.img)
        self.firstState.cost_to_come = 0
        self.firstState.cost_to_go=self.firstState.get_cost(self.goal)
        self.currentState = self.firstState
        self.lastState=None
        self.display = display
        self.write_info=write_info
        self.robot.maxspeed=45
        
        self.map_size=(250*3,250*3)
        self.start_radius=20
        self.goal_pose=(self.goal[0],self.goal[1])
        self.goal_radius=20
        self.start_pose=(self.currentLocation[0],self.currentLocation[1])
        self.node_radius=20
        self.neighbours=12
        self.planner = ProbabilisticRoadmap(self.map_size, self.start_pose, self.start_radius, self.goal_pose,
                                                self.goal_radius, self.obstacles,
                                                self.neighbours)
        self.search = AStar(self.planner.nodes)

    def sample(self):
        self.planner.sample(1000)

    def create_network(self):
        self.planner.create_network(self.display, self.node_radius, self.neighbours)
        self.search = AStar(self.planner.nodes)

    def get_path(self,start_pose,goal_pose):
        self.planner.start_pose=start_pose
        self.planner.goal_pose=goal_pose
        self.search.solve(self.planner.nodes,self.planner.get_start_node(),self.planner.get_end_node())
        # self.search.search(self.planner.get_start_node(),self.planner.get_end_node())
        

    def add_neighbors(self, neighbors):
        self.neighbors=[]
        for neighbor in neighbors:
            if self.isCollision(neighbor):
                continue
            self.neighbors.append(neighbor)

    def create_roadmap(self):
        pass

    def search(self):
        cost = 9999
        x,y,theta=self.currentLocation
        previousLocation=self.currentLocation
        startState = self.firstState
        lowestCostState=startState
        self.queue.put(startState)
        state=startState
        counter=0
        while not self.goalCheck(state) and self.queue.not_empty:
            counter+=1
            self.write_info("Planner iteration: {}".format(counter))
            state = self.queue.get()
            cost = state.cost_to_go
            
            # if state.cost_to_go<lowestCostState.cost_to_go:
            #     lowestCostState=state
            #     if state.cost_to_go>500:
            #         self.robot.maxspeed=45
            #     elif state.cost_to_go>200:
            #         self.robot.maxspeed=45
            #         self.robot.dt=.5
            #     elif state.cost_to_go>50:
            #         self.robot.maxspeed=45
            #         self.robot.dt=.5
            #     elif state.cost_to_go>15:
            #         self.robot.maxspeed=10
            #         self.robot.dt=.5

            state_location = state.get_location()
            neighbors = self.robot.get_neighbors(state_location)
            for nextState in neighbors:
                reward = 4
                nextState.cost_to_come = (state.cost_to_come+
                                          nextState.get_cost(state_location))
                nextState.cost_to_go=nextState.get_cost(self.goal)*reward
                if self.isCollision(nextState):
                    continue
                if nextState not in self.path:
                    self.path[nextState]=state
                    self.queue.put(nextState)
                    position = nextState.xy
                    self.display.fill((255, 0, 0), (position, (2, 2)))
                    pygame.event.get()
                    pygame.display.update()
            if counter >1 and counter%1000==0:
                break
        self.lastState = state
        return state
        

    def goalCheck(self,state:State):
        distanceToGoal = self.calculateCostToGoal(state)
        thetaDiff = abs(self.goal[2]-state.theta)
        return distanceToGoal<=5 and thetaDiff<=(math.pi/8)


    def plan(self):
        for neighbor in self.neighbors:
            self.cost[neighbor]=self.calculateCost(neighbor)

    def isCollision(self,state:State):
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
            return None
        
        currentState = self.lastState
        previousState = currentState

        while previousState!=self.currentState:
            currentState=previousState
            previousState=self.path[currentState]
            
        self.currentState=currentState
   
        return currentState
    
    def calculateCostToGoal(self,state:State):
        euclideanCost = ((self.goal[0]- state.x)**2 + (self.goal[1]- state.y)**2)**.5
        thetaCost = abs(self.goal[2]-state.theta)
        return euclideanCost*1.1 + thetaCost*.1



