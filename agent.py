import torch
import random
import numpy as np
from Battleship2 import BattleshipGameAI
from collections import deque #will be used to store our memory
from model import Linear_QNet, QTrainer
from plotStuff import plot
from settings import *

class Agent:
    def __init__(self,stateShape):
        self.nGames = 0
        self.epsilon = 0 #will be usedd to controll randomness
        self.gamma = 0.9 #discount rate needs to be <1
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(stateShape,256,1)  #inputSize, denselayerSize, how many choices it can make at the end
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma) 
        
        #model and trainer still needed
    
    def getState(self, game):
        return game.board_state
    
    def getAction(self, state):
        #begins with wandom moves -> explores the environment and then exploits it
        self.epsilon = 80- self.nGames
        fire = 0
        if random.randint(0,200) < self.epsilon:
            fire = random.randint(0,99)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) #this executes the forward function on our model
            fire = torch.argmax(prediction).item()
            
        return fire
    
    def remember(self, state, action, reward, nextState, done):
        #automatically will do a popleft if we reach MAX_MEMORY
        self.memory.append((state, action, reward, nextState, done)) #the extra set of parenthesis is fo appending the whole thing as a single element
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #random list of tuples from the memory
        else:
            mini_sample = self.memory
        
        #this magic line extracts data from mini_sample and puts all states toghether, all actions togheter and so on
        states, actions, rewards, nextStates, dones = zip(*mini_sample) #could just do a for loop to do this
        
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)
    
    def train_short_memory(self, state, action, reward, nextState, done):
        self.trainer.trainStep(state, action, reward, nextState, done) #will train for a single step
    
    
def train():
    trackScores = []
    meanScores = []
    totalScore = 0
    bestScore = 0
    game = BattleshipGameAI()
    agent = Agent(game.board_state)#game.board_state.shape or .size or just board_state
    while True:
        oldState = agent.getState(game)
        oldState = oldState.reshape(1,10,10)
        action = agent.getAction(oldState)
        
        #perform move and get new state
        reward, done, score = game.fire(action)
        newState = agent.getState(game)
        newState = newState.reshape(1,10,10)
        
        #train short memory
        #sees how the game was, what was its last action, how the game is now and what reward it got for it's last action
        #and should be able to learn something from it
        agent.train_short_memory(oldState, action, reward, newState, done)
        
        #remember
        agent.remember(oldState, action, reward, newState, done)
        
        if done:
            #train long memory
            game.reset()
            agent.nGames += 1
            #agent.train_long_memory()
            
            if score > bestScore:
                bestScore = score
                agent.model.save()
                
            print("Game", agent.nGames, "Score", score, "Best score", bestScore)
            
            #recording scores and plotting stuff
            trackScores.append(score)
            totalScore +=score
            meanScores.append(totalScore/agent.nGames)
            plot(trackScores, meanScores)


train()