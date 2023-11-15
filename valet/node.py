import math
import valet.helper as helper
import pygame

class Node:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.parent = None
        self.search = None
        self.adj = {}
        self.edge = {}

    def get_coords(self):
        return self.x, self.y

    def add_neighbour(self, neighbour):
        self.adj[neighbour] = self.__euclidean_dist(neighbour)
        self.edge[neighbour] = NodeEdge(self, neighbour)

    def __euclidean_dist(self, neighbour):
        return math.hypot((self.x - neighbour.x), (self.y - neighbour.y))

    def get_connections(self):
        return self.adj.keys()

    def get_weight(self, neighbour):
        return self.adj[neighbour]

    def draw(self, surf, node_radius, width):
        for neighbour in self.edge:
            color = helper.Color.GREY
            if neighbour.search == "Dijkstra":
                color = helper.Color.BLUE
            if neighbour.search == "AStar":
                color = helper.Color.RED
            if neighbour.search == "GreedyBFS":
                color = helper.Color.LIGHT_BLUE
            pygame.draw.line(surf, color, self.edge[neighbour].nfrom.get_coords(),
                             self.edge[neighbour].nto.get_coords(), width=width)
        pygame.draw.circle(surf, helper.Color.LIGHTGREY, self.get_coords(), node_radius, width=0)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.id}"


# Used to visualize pathfinding
class NodeEdge:
    def __init__(self, node_from: Node, node_to: Node):
        self.nfrom = node_from
        self.nto = node_to
