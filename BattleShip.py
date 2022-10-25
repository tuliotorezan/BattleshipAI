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
#deep larning libraries
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
#libraries for reinforced learning
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


def InitializeBoard(boardSize=10):
    board = np.zeros((boardSize,boardSize))
    shipList = [5,4,3,3,2]
    for shipSize in shipList:    
        answ = False
        while answ == False:
            direction = np.random.randint(0,2)
            x = np.random.randint(0, boardSize)
            y = np.random.randint(0,boardSize)
            answ = PlaceShip(board, direction, x, y, shipSize)
    return board

def PlaceShip(board, direction, x, y, shipSize):
    lenX, lenY = board.shape
    
    if direction == "h" or direction == 0:
        #check if a ship of this size can fit in the board beginning on position x
        if x+shipSize > lenX:
            return False
        
        #check if there is something in that position already
        for i in range(0,shipSize):
            if board[x+i][y] != 0:
                return False
        #if the space is available, then we put the ship in it
        for i in range(0, shipSize):
            board[x+i][y] = 1
        return True
            
    if direction == "v" or direction == 1:
        #check if a ship of this size can fit in the board beginning on position y
        if y+shipSize > lenY:
            return False
        
        #check if there is something in that position already
        for i in range(0,shipSize):
            if board[x][y+i] != 0:
                return False
        #if the space is available, then we put the ship in it
        for i in range(0, shipSize):
            board[x][y+i] = 1
        return True
    
            



###############     Creating custom reinforced learning environment     ###############
class BattleshipEnv(Env):
    def __init__(self):
        
        #this is the reference map to where are the enemy ships 0 = water 1=ship, will come from external function
        self.enemy_board = InitializeBoard()
        
        #board size
        self.grid_size = self.enemy_board.shape[0]
        
        #cell state (Unknown, hit, miss)
        self.cell = {"~": 0, "X":1, "O": -1}
        
        #setting up the board you will see when shooting
        self.board_state = self.cell["~"]*np.ones((self.grid_size, self.grid_size), dtype="int")
        
        #counting the total number of hits before winning
        self.shotsToWin = sum(sum(self.enemy_board))
        
        self.done = False
        
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
        i = action%10
        j = action//10
        if self.enemy_board[i,j] == 1:
            self.board_state[i,j] = self.cell["X"]
            self.enemy_board[i,j] = -1
            self.shotsToWin -= 1
            if self.shotsToWin == 0:
                self.done = True
            reward = 1
        elif self.enemy_board[i][j] == -1:
            reward = -5
        else:
            self.board_state[i,j] = self.cell["O"]
            reward = -1
            
        return self.board_state, reward, self.done
    
    
    
    def reset(self):
        self.enemy_board = InitializeBoard(self.grid_size)
        self.board_state = self.cell["~"]*np.ones((self.grid_size, self.grid_size), dtype="int")
        self.shotsToWin = sum(sum(self.enemy_board))
        self.done = False
        return 0
    
    
    
    def render(self, mode = "human"):
        return 0
    
        
        
#this is simulating its playing randomly
env = BattleshipEnv()
episodes = 20
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0
    shots = 0
    
    while not done:
        action = env.action_space.sample()
        board_state, reward, done = env.step(action)
        shots +=1
        score += reward
        print("{}".format(board_state))
    print("Episode:{} Score:{} Shots:{}".format(episode, score, shots))
    
        
        
       
###############     Creating simple Deep Learning model     ###############

states = env.observation_space.shape
actions = env.action_space.n

def build_model(states, actions):
    model = Sequential()
    model.add(Dense(256,activation="relu", input_shape=states))
    model.add(Dense(512, activation="relu"))
    model.add(Flatten())
    model.add(Dense(actions, activation="linear"))
    return model


model = build_model(states, actions)

model.summary()

        
        
        
###############     Creating the agent with Keras-ReinforcementLearning     ###############

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit = 50000, window_length=2, ignore_episode_boundaries=True)
    dqn = DQNAgent(model=model, memory = memory, policy=policy,
                   nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn


dqn = build_agent(model, actions)
dqn.compile(Adam(lr=1e-3), metrics=["mae"])
dqn.fit(env, nb_steps=60000, visualize=False, verbose = 1)


results = dqn.test(env, nb_episodes=150, visualize=False)
print(np.mean(results.history["episode_reward"]))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        