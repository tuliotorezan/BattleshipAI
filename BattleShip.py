# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:56:18 2022

@author: tulio
"""

##Importing general libraries
import numpy as np
import random
#game environment libraries
from gym import Env
from gym.spaces import Box, Discrete






###############     Creating custom reinforced learning environment     ###############
class CustomEnv(Env):
    def __init__(self, enemy_board, grid_size):
        
        #board size
        self.grid_size = grid_size
        
        #cell state (Unknown, hit, miss)
        self.cell = {"~": 0, "X":1, "O": -1}
        
        #setting up the board the coe will see when shooting
        self.board = self.cell["~"]*np.ones((self.grid_size, self.grid_size), dtype="int")
        
        #this is the reference map to where are the enemy ships 0 = water 1=ship, will come from external function
        self.enemy_board = enemy_board
        
        
        self.legal_actions = [] # legal cells available for shooting
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.legal_actions.append((i,j))# this gets updated as an action is performed
        
        #discrete space of where can the user (AI) shoot at
        self.action_space = Discrete(self.grid_size * self.grid_size)
        
        #the state of the board
        self.observation_space = Box(low=-1, high=1, shape=(self.grid_size, self.grid_size),
                                     dtype=np.int)        
        
        
    def step(self, action):
        return 0
    
    def reset(self):
        return 0
    
    def render(self, mode = "human"):
        return 0
    
    #sets the new board state after an action
    def set_state(self, action):
        i,j = action
        if self.enemy_board[i,j] == 1:
            self.board[i,j] = self.cell["X"]
        else:
            self.board[i,j] = self.cell["O"]
        
        