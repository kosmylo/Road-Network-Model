from random import sample, randrange
from itertools import product
import math
from constants import MAXIMUM_ROAD_CAPACITY, MAXIMUM_TRAVEL_DISTANCE, AVERAGE_VELOCITY, AVERAGE_CONSUMPTION, CHARGER_CAPACITY, CHARGER_SPEED, CHARGER_TIME
import numpy as np

class RoadNetwork():
    """
    Class for creating the road network model
    """

    def __init__(self, n, m):
        """
        :param `int` n: The number of nodes
        :param `int` m: The number of edges
        """

        if n <= 0:
            raise ValueError('Node number must be positive')
        if m <= 0:
            raise ValueError('Edge number must be positive')
        if m > n**2:
            raise ValueError('Edge number must be no greater than the square of node number')

        self.n = n
        self.m = m

    def create_random_graph(self):
        """
        Create a random directed graph with n nodes and m edges and return the adjacency list

        :return `list` road_adj_list: The list containing the neighbours of each node
        """
        
        nodes = range(self.n)
        adj_list = [[] for i in nodes]
        possible_edges = product(nodes, repeat=2)
        
        for u, v in sample(list(possible_edges), self.m):
            if u != v:
                adj_list[u].append(v)
        
        road_adj_list = [sorted(item) for item in adj_list]
        
        return road_adj_list

    def create_capacity_matrix(self, road_adj_list):
        """
        Create a capacity matrix with the maximum amount of vehicles per unit time of the i-j link

        :param `list` road_adj_list: The list containing the neighbours of each node

        :return `numpy.ndarray` road_capacity_matrix: The matrix containing the capacity of each road link
        """
        
        road_adj_dict = dict(enumerate(road_adj_list))
        road_capacity_matrix = np.zeros((self.n, self.n))

        for i, j in road_adj_dict.items():

            road_capacity_matrix[i, i] = np.inf

            for k in j:

                road_capacity_matrix[i, k] = randrange(MAXIMUM_ROAD_CAPACITY+1)

        return road_capacity_matrix

    def create_travel_distance_matrix(self, road_adj_list):
        """
        Create a matrix with the travel distance along the i-j link

        :param `list` road_adj_list: The list containing the neighbours of each node

        :return `numpy.ndarray` road_travel_distance_matrix: The matrix containing the travel distance for each road link
        """
        
        road_adj_dict = dict(enumerate(road_adj_list))
        road_travel_distance_matrix = np.zeros((self.n, self.n))

        for i, j in road_adj_dict.items():

            for k in j:

                road_travel_distance_matrix[i, k] = randrange(MAXIMUM_TRAVEL_DISTANCE+1)

        return road_travel_distance_matrix   

    def create_travel_time_matrix(self, road_adj_list, road_travel_distance_matrix):
        """
        Create a matrix with the travel time along the i-j link

        :param `list` road_adj_list: The list containing the neighbours of each node
        :param `numpy.ndarray` road_travel_distance_matrix: The matrix containing the travel distance for each road link

        :return `numpy.ndarray` road_travel_time_matrix: The matrix containing the travel time for each road link
        """
        
        road_adj_dict = dict(enumerate(road_adj_list))
        road_travel_time_matrix = np.zeros((self.n, self.n))

        for i, j in road_adj_dict.items():

            road_travel_time_matrix[i, i] = 1

            for k in j:

                road_travel_time_matrix[i, k] = math.ceil(road_travel_distance_matrix[i, k] / AVERAGE_VELOCITY)

        return road_travel_time_matrix 

    def create_charge_to_traverse_matrix(self, road_adj_list, road_travel_distance_matrix):
        """
        Create a matrix with the amount of units of charge required to travel from i to j

        :param `list` road_adj_list: The list containing the neighbours of each node
        :param `numpy.ndarray` road_travel_distance_matrix: The matrix containing the travel distance for each road link

        :return `numpy.ndarray` road_charge_to_traverse_matrix: The matrix containing the amount of units of charge required for each road link
        """
        
        road_adj_dict = dict(enumerate(road_adj_list))
        road_charge_to_traverse_matrix = np.zeros((self.n, self.n))

        for i, j in road_adj_dict.items():

            for k in j:

                road_charge_to_traverse_matrix[i, k] = math.ceil(road_travel_distance_matrix[i, k] * AVERAGE_CONSUMPTION)

        return road_charge_to_traverse_matrix 

    def create_charger_list(self):
        """
        Create a random list with the location of the node in road_adj_list corresponding to the l-th charging station

        :return `list` charger_list: The list containing the locations of the charging stations
        """
        
        charger_list_bool = []
        charger_list = []
        nodes = range(self.n)
        
        for i in nodes:
            charger_list_bool.append(np.random.choice([0,1]))
            charger_list = [i for i, x in enumerate(charger_list_bool) if x == 1]

        return charger_list   

    def create_charger_capacity_list(self, charger_list):
        """
        Create a list with the number of vehicles that can charge concurrently in charging station l

        :param `list` charger_list: The list containing the locations of the charging stations

        :return `list` charger_capacity_list: The list containing the capacity of the charging stations
        """
        
        charger_capacity_list = []
        charging_stations = range(len(charger_list))

        for i in charging_stations:
            charger_capacity_list.append(CHARGER_CAPACITY)

        return charger_capacity_list   

    def create_charger_speed_list(self, charger_list):
        """
        Create a list with the amount of charge gained by a vehicle crossing charging station l

        :param `list` charger_list: The list containing the locations of the charging stations

        :return `list` charger_speed_list: The list containing the charging rate from/to the charging stations
        """
        
        charger_speed_list = []
        charging_stations = range(len(charger_list))

        for i in charging_stations:
            charger_speed_list.append(CHARGER_SPEED)

        return charger_speed_list

    def create_charger_time_list(self, charger_list):
        """
        Create a list with time required to charge charger_speed_list(l) units of charge at charging station l

        :param `list` charger_list: The list containing the locations of the charging stations

        :return `list` charger_time_list: The list containing the time that it takes to charge/discharge with the charging rate at charging stations
        """
        
        charger_time_list = []
        charging_stations = range(len(charger_list))

        for i in charging_stations:
            charger_time_list.append(CHARGER_TIME)

        return charger_time_list