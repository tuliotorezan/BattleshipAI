#Created on Mon Oct 24 21:29:31 2022
#@author: tulio


##Importing general libraries
import numpy as np
import pygame
import random
from enum import Enum
from collections import namedtuple
import sys
from settings import *
from sprites import *


class BattleshipGame:
    def __init__(self):
        # init display
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)
        self._load_data()
        
        self.shotsFired = []        
        #this is the reference map to where are the enemy ships 0 = water 1=ship, will come from external function
        self.enemy_board = self.InitializeBoard()
        #board size
        self.grid_size = self.enemy_board.shape[0]
        #cell state (Unknown, hit, miss)
        self.cell = {"~": 0, "X":1, "O": -1}
        #setting up the board you will see when shooting
        self.board_state = self.cell["~"]*np.ones((self.grid_size, self.grid_size), dtype="int")
        #counting the total number of hits before winning
        self.shotsToWin = sum(sum(self.enemy_board))
        self.done = False
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.reset()
        self.all_sprites = pg.sprite.Group()
        self.target = Target(self, 2, 4)
        
    def _load_data(self):
        pass
        
            
    def fire(self, action):
        i = action%10
        j = action//10
        if self.enemy_board[i,j] == 1:
            self.board_state[i,j] = self.cell["X"]
            self.enemy_board[i,j] = -1
            self.shotsToWin -= 1
            self.shotsFired.append(Shot(self, i, j, True))
            if self.shotsToWin == 0:
                self.done = True
                self.playing = False
            reward = 1
        elif self.enemy_board[i][j] == -1:
            reward = -5
        else:
            self.board_state[i,j] = self.cell["O"]
            reward = -1  
            self.shotsFired.append(Shot(self, i, j, False))          
        return self.board_state, reward, self.done
    
    def run (self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self._events()
            self._update()
            self._draw()
            
    def _quit(self):
        pygame.quit()
        sys.exit()
    
    def _update(self):
        self.all_sprites.update()
        
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
    
    def _events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._quit()
                if event.key == pg.K_LEFT:
                    self.target.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.target.move(dx=1)
                if event.key == pg.K_UP:
                    self.target.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.target.move(dy=1)
                if event.key == pg.K_RETURN:
                    self.fire(self.target.x+self.target.y*10)
                    

    
        
    def draw_grid(self):
        for x in range(int(WIDTH/4), int(3*WIDTH/4)+1, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (x,int(HEIGHT/4)), (x,int(3*HEIGHT/4)))
        for y in range(int(HEIGHT/4), int(3*HEIGHT/4)+1, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (int(WIDTH/4),y), (int(3*WIDTH/4),y))
    
    def _draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
        
    def reset(self):
        self.enemy_board = self.InitializeBoard(self.grid_size)
        self.board_state = self.cell["~"]*np.ones((self.grid_size, self.grid_size), dtype="int")
        self.shotsToWin = sum(sum(self.enemy_board))
        self.done = False
        return 0
        
    def InitializeBoard(self, boardSize=10):
        board = np.zeros((boardSize,boardSize))
        shipList = [5,4,3,3,2]
        for shipSize in shipList:    
            answ = False
            while answ == False:
                direction = np.random.randint(0,2)
                x = np.random.randint(0, boardSize)
                y = np.random.randint(0,boardSize)
                answ = self.PlaceShip(board, direction, x, y, shipSize)
        return board

    def PlaceShip(self, board, direction, x, y, shipSize):
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
        

g = BattleshipGame()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()