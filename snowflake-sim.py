# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:35:16 2023

@author: filon
"""

# Random walk
import random
import numpy as np
import pygame

class App:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self.startX, self.startY = round(self.width/2), round(self.height/2)
        self.X, self.Y = self.startX, self.startY
        self.prob = 50
        
        self.minX, self.minY = self.X, self.Y
        self.maxX, self.maxY = self.X, self.Y
        self.padSize = 20
        
        self.domainMinX = self.startX - self.padSize
        self.domainMaxX = self.startX + self.padSize
        self.domainMinY = self.startY - self.padSize
        self.domainMaxY = self.startY + self.padSize
        
        self.crystalColor = 0x808080
        
        self.displaySurface = None
        self.pixelArray = None
        self.updateFlag = False

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Diffusion Limited Aggregation')
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.isRunning = True
        
        # Set seed point
        self.pixelArray[self.startX, self.startY + 10] = self.crystalColor
        pygame.display.update()
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False
    
    def on_loop(self):
        # Choose a random direction to move
        newD = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)))
        newProb = random.randrange(0,100)
        # Extract dX and dY
        dX, dY = newD
        
        # Apply to X and Y coords
        newX = self.X + dX
        newY = self.Y + dY
        
        if (newX < self.domainMinX):
            newX = self.domainMaxX
            
        if (newX > self.domainMaxX):
            newX = self.domainMinX
        
        if (newY < self.domainMinY):
            newY = self.domainMaxY
            
        if (newY > self.domainMaxY):
            newY = self.domainMinY
        
        # Check if pixel has already been filled
        if (self.pixelArray[newX, newY] == self.crystalColor):
            if newProb <= self.prob:
                self.updateFlag = True
            
            # Modify extent of simulation domain when neccessary
            if (self.X < self.minX):
                self.minX = self.X
            
            if (self.X > self.maxX):
                self.maxX = self.X
                
            if (self.Y < self.minY):
                self.minY = self.Y
                
            if (self.Y > self.maxY):
                self.maxY = self.Y
                
            # Modify the domain
            self.domainMinX = max([self.minX - self.padSize, 1])
            self.domainMaxX = min([self.maxX + self.padSize, self.width - 1])
            self.domainMinY = max([self.minY - self.padSize, 1])
            self.domainMaxY = min([self.maxY + self.padSize, self.height - 1])
            
        else:
            self.updateFlag = False
            self.X, self.Y = newX, newY
    
    def on_render(self):
        if self.updateFlag:
            # Update the pixel array
            self.pixelArray[self.X, self.Y] = self.crystalColor
            pygame.display.update()
            
            # Reset update flag
            self.updateFlag = False
            
            # Select one of the four sides of the domain
            newSide = random.choice((1, 2, 3, 4))
            if (newSide == 1):
                self.X = self.domainMinX
                self.Y = int(random.uniform(self.domainMinY, self.domainMaxY))
            elif (newSide == 2):
                self.X = int(random.uniform(self.domainMinX, self.domainMaxX))
                self.Y = self.domainMinY
            elif (newSide == 3):
                self.X = self.domainMaxX
                self.Y = int(random.uniform(self.domainMinY, self.domainMaxY))
            else:
                self.X = int(random.uniform(self.domainMinX, self.domainMaxX))
                self.Y = self.domainMaxY
    
    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False
        
        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)
            
            self.on_loop()
            self.on_render()
        
        pygame.quit()

if __name__ == "__main__":
    t = App()
    t.on_execute()