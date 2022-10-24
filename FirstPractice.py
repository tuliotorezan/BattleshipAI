# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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



###############     Creating custom reinforced learning environment     ###############
class CustomEnv(Env):
    def __init__(self):
        self.action_space = Discrete(3)  #for battleship will probably make this a set of 2 coordinates, each, from 0-10
        self.observation_space = Box(low=np.array([0]), high=np.array([100])) #will probably hold the battlefield here
        self.state = 38 + random.randint(-3, 3)
        self.shower_length = 60  #for battleship this will probably hold the max ammount of turns, in case no one wins
        
        
    #the step function defines what should be done after taking an action in our game
    def step(self, action):
        self.state = self.state + action -1
        self.shower_length -= 1
        
        #Calculating reward
        if self.state >= 37 and self.state <=39:
            reward = 1
        else:
            reward = -1
            
        #Checking if shower is done
        if self.shower_length <=0:
            done = True
        else:
            done = False
            
        #Setting placeholder for info
        info = {}
        
        return self.state, reward, done, info
    
    def render(self):
        #this is where you should write the visualiozation code
        return 0
        
    def reset(self):
        self.state = 38 + random.randint(-3, 3)
        self.shower_length = 60
        return self.state
    
    
env = CustomEnv()

episodes = 20
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0
    
    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print("Episode:{} Score:{}".format(episode, score))
        
        
        
        
###############     Creating simple Deep Learning model     ###############

states = env.observation_space.shape
actions = env.action_space.n

def build_model(states, actions):
    model = Sequential()
    model.add(Dense(24,activation="relu", input_shape=states))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(actions, activation="linear"))
    return model


model = build_model(states, actions)

model.summary()

        
        
        
###############     Creating the agent with Keras-ReinforcementLearning     ###############












        
        
        
        
        
        
        
        
        