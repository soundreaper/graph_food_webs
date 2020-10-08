from collections import deque
from random import choice
import pandas as pd
import numpy as np

class Vertex(object):
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.id = vertex_id
        self.neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (number): The weight of this edge.
        """
        if vertex_obj.get_id() in self.neighbors_dict.keys():
            return

        self.neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return [neighbor for (neighbor, weight) in self.neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex."""
        return list(self.neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'

class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {}
        self.is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        if vertex_id in self.vertex_dict.keys():
            return False
        vertex_obj = Vertex(vertex_id)
        self.vertex_dict[vertex_id] = vertex_obj
        return True

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.vertex_dict.keys():
            return None
        vertex_obj = self.vertex_dict[vertex_id]
        return vertex_obj
    
    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        weight (number): The edge weight.
        """
        all_ids = self.vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)

    def get_vertices(self):
        """Return all the vertices in the graph"""
        return list(self.vertex_dict.values())

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax:
        for vertex in graph"""
        return iter(self.vertex_dict.values())

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root

    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if(parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def shortest_prey_to_predator(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to find the shortest path from a given prey
        to a target predator (could be the next one could be the apex predator).
        """
        vertex_to_distance = {x:float('inf') for x in self.get_vertices()}
        start_vertex = self.get_vertex(start_id)
        vertex_to_distance[start_vertex] = 0
    
        while vertex_to_distance:
            min_weighted_vertex = min(vertex_to_distance.items(), key=lambda x: x[1])
            vertex_to_distance.pop(min_weighted_vertex[0])

            if min_weighted_vertex[0].get_id() == target_id:
                return min_weighted_vertex[1]

            try:
                for neighbor in min_weighted_vertex[0].get_neighbors_with_weights():
                    vertex, weight = neighbor
                    if vertex in vertex_to_distance and weight + min_weighted_vertex[1] < vertex_to_distance[vertex]:
                        vertex_to_distance[vertex] = weight + min_weighted_vertex[1]
            except KeyError:
                continue
    
        return None

    def popular_species(self):
        """
        Use Floyd-Warshall's Algorithm to look at one animal in a food web
        and figure out how long it would take to get to every other animal.
        This can tell us which animals in a given food web are the most
        "popular" meaning they are consumed a lot. In most ecosystems,
        there tend to be many more prey than predators. Using this algorithm,
        if we find that a predator is very "popular" it might show that
        a certain species is overpopulated.
        """
        dist = {}
        all_vertex_ids = self.vertex_dict.keys()

        for vertex1 in all_vertex_ids:
            dist[vertex1] = {}
            for vertex2 in all_vertex_ids:
                dist[vertex1][vertex2] = float('inf')
            dist[vertex1][vertex1] = 0

        all_vertex_objs = self.get_vertices()
        for vertex in all_vertex_objs:
            neighbors_with_weights = vertex.get_neighbors_with_weights()
            for neighbor, weight in neighbors_with_weights:
                dist[vertex.get_id()][neighbor.get_id()] = weight

        for i in all_vertex_ids:
            for j in all_vertex_ids:
                for k in all_vertex_ids:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist
    
    def most_common_prey(self):
        """
        This uses the popular_species function we wrote to pick out the most
        common animal. This is useful for figuring out what species of animals
        is the MOST common in a given ecosystem.
        """
        animal_dictionary = self.popular_species()
        df = pd.DataFrame.from_dict(animal_dictionary)
        df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
        return(df.columns[0])
            

    # def food_chains(self):
    #     edges = []
    #     for vertex in self.get_vertices():
    #         for neighbor, weight in vertex.get_neighbors_with_weights():
    #             edges.append((vertex.get_id(), neighbor.get_id(), weight))
    #     edges = sorted(edges, key=lambda x: x[2])
    
    #     parent_map = {x[0]:x[0] for x in edges}
    
    #     spanning_tree = []
    
    #     while len(spanning_tree) <= len(edges)-1:
    #         current = edges.pop(0)
    #         (vertex1, vertex2, weight) = current
    
    #         if self.find(parent_map, vertex1) != self.find(parent_map, vertex2):
    #             spanning_tree.append(current)
    #             self.union(parent_map, vertex1, vertex2)
    #         else:
    #             continue
    
    #     return spanning_tree