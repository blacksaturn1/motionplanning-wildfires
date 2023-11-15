from typing import List, Optional, Tuple
from valet.node import Node
import random
import valet.helper as helper

class ProbabilisticRoadmap:
    nodes: List[Node]

    def __init__(self, map_dim, start_pose, start_radius, goal_pose, goal_radius, obstacles, k):
        self.map_dim = self.mapx, self.mapy = map_dim
        self.start_pose = self.sx, self.sy = start_pose
        self.start_radius = start_radius
        self.goal_pose = self.gx, self.gy = goal_pose
        self.goal_radius = goal_radius
        self.obstacles = obstacles
        self.k = k
        self.nodes = []
        self.network_created = False

    def sample(self, sample_size):
        self.network_created = False
        self.nodes = []
        self.add_node(0, *self.start_pose)
        for i in range(sample_size):
            n = len(self.nodes)
            collision = True
            x, y = (-1, -1)
            while collision:
                x, y = self.sample_envir()
                collision = self.on_obstacle((x, y))
            self.add_node(n, x, y)
        return self.nodes

    def sample_envir(self):
        x = int(random.uniform(0, self.mapx))
        y = int(random.uniform(0, self.mapy))
        return x, y

    def on_obstacle(self, point):
        for obs in self.obstacles:
            if obs.collidepoint(point):
                return True
        return False

    def add_node(self, n, x, y):
        self.nodes.insert(n, Node(x, y, n))

    def remove_node(self, n):
        self.nodes.pop(n)

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles

    def cross_obstacle(self, start_pos, end_pos):
        sx, sy = start_pos[0], start_pos[1]
        ex, ey = end_pos[0], end_pos[1]

        for obs in self.obstacles:
            for i in range(100):
                u = i / 100
                x = sx * u + ex * (1 - u)
                y = sy * u + ey * (1 - u)
                if obs.collidepoint(x, y):
                    return True
        return False

    def find_k_nearest(self, n, k):
        k_dists = {}
        for i in range(k + 1):
            d = helper.dist_to_node(self.nodes[i], n)
            k_dists[d] = self.nodes[i]

        for i in range(len(self.nodes)):
            nn = self.nodes[i]
            d = helper.dist_to_node(nn, n)
            if d not in k_dists.keys():
                max_dist = max(k_dists.keys())
                if d < max_dist:
                    k_dists.pop(max_dist)
                    k_dists[d] = nn

        return k_dists.values()

    def connect(self, n1, n2):
        if self.cross_obstacle(n1.get_coords(), n2.get_coords()):
            return False
        else:
            helper.add_edge(n1, n2)

    def add_edges(self, n):
        k_nearest = self.find_k_nearest(n, self.k)
        for node in k_nearest:
            self.connect(n, node)
        return n

    def update_edges_gt(self, n):
        k_nearest = self.find_k_nearest(n, self.k)
        for node in k_nearest:
            if node in n.adj:
                continue
            self.connect(n, node)
        return n

    def update_edges_lt(self, n):
        k_nearest = self.find_k_nearest(n, self.k)
        adj = n.adj.copy()
        for node in adj:
            if node in k_nearest:
                continue
            else:
                del n.adj[node]
                del n.edge[node]
        return n

    def find_node_in_radius(self, p, r):
        x = p[0]
        y = p[1]
        if len(self.nodes) == 0:
            return None
        max_dist = r
        closest_node = None
        for node in self.nodes:
            d = helper.dist_to_point(node, p)
            if d <= max_dist:
                max_dist = d
                xx, yy = node.get_coords()
                if (x - xx) ** 2 + (y - yy) ** 2 <= r ** 2:
                    closest_node = node
        return closest_node

    def get_start_node(self):
        return self.find_node_in_radius(self.start_pose, self.start_radius)

    def get_end_node(self):
        return self.find_node_in_radius(self.goal_pose, self.goal_radius)

    def create_network(self, surf, nr, neighbours):
        if (self.network_created):
            return
        self.k = neighbours
        for node in self.nodes:
            node.adj = {}
            node.edge = {}
            self.add_edges(node)
            node.draw(surf, nr, 1)
        self.network_created = True

    def update_network_gt(self):
        for node in self.nodes:
            self.update_edges_gt(node)

    def update_network_lt(self):
        for node in self.nodes:
            self.update_edges_lt(node)

    def update_k(self, k):
        for node in self.nodes:
            node.search = None
            node.parent = None
        if k > self.k:
            self.k = k
            self.update_network_gt()
        elif k < self.k:
            self.k = k
            self.update_network_lt()

    def update_pose(self, sp, gp):
        self.start_pose = sp
        self.goal_pose = gp

