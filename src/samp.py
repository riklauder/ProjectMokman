#!/usr/bin/python
#My super cool block game.
import pygame, random, math, operator, time
from pygame.locals import *
#Constant variables or something like that...
BGCOLOR =[50,100,200] 
GRAVITY = 1
##Special functions
#Holds the informations for powerups and returns it based on number sent.
#returns pointlist, color, rect.
def iteminfo(typeno,center):
    if typeno==1:
        return  [[center[0]-10,center[1]-10],[center[0]+10,center[1]-10],[center[0]+10,center[1]+10],[center[0]-10,center[1]+10]],\
               [128,128,128],\
               pygame.Rect(center[0]-10,center[1]-10,20,20)
##People and polygons
class polygon:
    def __init__(self,color,pointlist,width=0,state=1):
        self.color = color
        self.pointlist  = pointlist
        self.width = width
        self.rect = pygame.Rect(20,20,30,30) #TODO fix!
        self.oldrect = self.rect
        self.vel = [0,0]
        self.state = state #Is it solid? yes
        self.age = 0
    def draw(self,screen):
        self.rect = pygame.draw.polygon(screen,self.color,self.pointlist,self.width)

    def moverel(self,x,y): #Move it an amount relative to it's position
        self.oldpointlist = self.pointlist
        self.rect = self.rect.move(x,y)
        for i in range(len(self.pointlist)):
                       self.pointlist[i][0] += x
                       self.pointlist[i][1] += y
        self.rect = self.rect.move(x,y)
                       
    def movevel(self): #Move it an amount equal to ir's velocity
        self.oldpointlist = self.pointlist
        
        for i in range(len(self.pointlist)):
                       self.pointlist[i][0] += self.vel[0]
                       self.pointlist[i][1] += self.vel[1]
        self.vel[0] *= 0.95
        self.vel[1] *= 0.95
        self.rect = self.rect.move(self.vel[0],self.vel[1])

    def update(self):
        self.oldrect = self.rect
#------------------------------------------------------------------------------------------------
class person(polygon):
    def __init__(self,color,pointlist,width,state=1):
        
        self.color = color
        self.pointlist = pointlist
        #self.oldpointlist = pointlist
        self.width = width
        self. vel = [0,0]
        self.rect = pygame.Rect(20,20,30,30) #TODO fix!!!
        #self.oldrect = self.rect
        self.age =0
        self.state = state
        self.items = [0,0,0]
        

    def inputs(self,inputs): #Send in all the keys being pressed
        if inputs.count(K_UP) >0:
            self.vel[1] += -1.5
        if inputs.count(K_DOWN) >0:
            self.vel[1] += 1 + 0.5 
        if inputs.count(K_LEFT) >0:
            self.vel[0] += -1 -  0.5 * self.items[1]
        if inputs.count(K_RIGHT) >0:
            self.vel[0] += 1 + 0.5 * self.items[1]

            


    def collidey(self,world): #Fall down or up
        y = 0
        for i in range(len(world[1])):
            #This makes a rectangle that is really just a side of the border.
            if  self.rect.colliderect(pygame.Rect(world[1][i].rect.left + 2,world[1][i].rect.top,(world[1][i].rect.right - world[1][i].rect.left - 4),1)) :
                if world[1][i].state == 1:
                    self.vel[0] *= 0.95
                    self.vel[1] = 0 
                    y = world[1][i].rect.top  - self.rect.bottom
                if world[1][i].state == 0:
                    self.items[world[1][i].typeno] += 1
                    world[1][i].age = 100
                    
            if  self.rect.colliderect(pygame.Rect(world[1][i].rect.left + 2,world[1][i].rect.bottom,(world[1][i].rect.right - world[1][i].rect.left - 4),1)) :
                if world[1][i].state == 1:
                    self.vel[0] *= 0.95
                    self.vel[1] = 0
                    y = world[1][i].rect.bottom  - self.rect.top
                if world[1][i].state == 0:
                    pass
        return y
    def collidex(self,world): #check for collisions. Needs polish.
        x = 0
        for i in range(len(world[1])):
            if  self.rect.colliderect(pygame.Rect(world[1][i].rect.left,world[1][i].rect.top + 2,1,(world[1][i].rect.bottom - world[1][i].rect.top - 4))) :
                if world[1][i].state == 1:
                    self.vel[0] = 0 
                    x = world[1][i].rect.left  - self.rect.right
                if world[1][i].state == 0:
                    pass
            if self.rect.colliderect(pygame.Rect(world[1][i].rect.right,world[1][i].rect.top + 2,1,(world[1][i].rect.bottom - world[1][i].rect.top - 4))):
                if world[1][i].state == 1:
                    self.vel[0] = 0 
                    x = world[1][i].rect.right  - self.rect.left
                if world[1][i].state == 0:
                    pass
        return x
#----------------------------------------------------------------------------------------
class powerup(polygon):
    def __init__(self,center,width=0,typeno=1,state=0):
        self.pointlist,self.color,self.rect = iteminfo(typeno,center)
        #self.oldpointlist = pointlist
        self.width = width
        self. vel = [0,0]
        self.typeno = typeno 
        #self.oldrect = self.rect
        self.age =0
        self.state = state
##########################   
#Particles or as close as I can get#
##########################    

class Particle:
    def __init__(self,center,brightness=230,radius=2, width=0):
        self.center = [center[0] + random.randint(-1,1), center[1] + random.randint(-1,1)]
        self.brightness = brightness + random.randint(-5,15)
        self.radius = radius
        self.color = [brightness,brightness,brightness]
        self.width = width
        self.age = 0
        self.rect = pygame.Rect(self.center[0] - radius, self.center[1] - radius,2 * radius, 2 * radius)
        self.oldrect = self.rect

    def draw(self,screen):
        
        self. rect = \
              pygame.draw.circle\
              (screen,
               [int(self.color[0]) ,int( self.color[1]) ,int( self.color[2])],
               [int(self.center[0]),int(self.center[1])],
                 self.radius,
                 self.width)

    def moverel(self,x,y):
        self.center[0] += x
        self.center[1] += y
        self.rect = self.rect.move(x,y)

    def update(self):
        if self.brightness > 2:
            self.brightness  -= 2
        self.color = [
            (self.color[0] + 0.06 * (BGCOLOR[0] - self.color[0])),
                      (self.color[1] + 0.06 * (BGCOLOR[1] - self.color[1])),
                      (self.color[2] + 0.06 * (BGCOLOR[2] - self.color[2])),
                      ]
        self.radius += 1
        self.age += 1
        self.oldrect = self.rect
        
        
        
        

############################
#This where all the magic happens!#
############################
def main():
    #Screen setup
    pygame.init()
    
    screen = pygame.display.set_mode([640, 480])
    screen.fill(BGCOLOR)
    pygame.display.update()
    #Clock init
    clock = pygame.time.Clock()
    #Keylists init.
    downlist = []
    uplist = []
    pressedlist = []
    #Player and world init
    player = person([100,200,200],
                     [[100,200],[130,200],[130,230],[100,230]],
                     0)
    world = [
        [],
        [polygon( [255,255,255],[[-10,400],[620,400],[600,420],[0,420]],1),
        polygon( [255,255,255],[[-810,390],[-10,390],[-10,420],[-810,420]],1),
        polygon( [255,255,255],[[-10,300],[620,300],[600,320],[0,320]],1),
        powerup([50,200]),
        powerup([0,420]),
        powerup([150,380]),
        powerup([-160,360])

         ],
        
        []
         ]
    #other stuff
    delay = 0
    #delayb = 0
    
    #The actual loop.
    while 1:
        #Wiping variables, ticking clock, clearing screen
        clock.tick(30)
        screen.fill(BGCOLOR)
        delay += 1
        #delayb += 1
        downlist = []
        uplist = []

        #What a brave new WORLD.
        if delay > 2:
            delay = 0
            if  abs(player.vel[1]) > 1 or abs(player.vel[0]) > 3:
                world[0].append(Particle(player.rect.center))
                 
                
        for listy in world:
            for i in range(len(listy)):
                listy[i].update()
                listy[i].draw(screen)
        for i in range(len(world)):
            if len(world[i]) > 0:
                for j in range(len(world[i])):
                    if world[i][-j].age > 90:
                        del world[i][-j]
                    
                

        
        
        #Now why would you want to quit?    
        for key in pygame.event.get(QUIT):
             pygame.display.quit()
             return
        #Add key presses to respective lists.
        for key in pygame.event.get(KEYUP):
            uplist.append(key.key)
            pressedlist = [item for item in pressedlist if  item != key.key]            
        for key in pygame.event.get(KEYDOWN):
            downlist.append(key.key)
            pressedlist.append(key.key)

        
            
        for key in pressedlist:
            if key == K_ESCAPE:
                pygame.display.quit()
                return
        ###################
        #player and world stuff.#
        ###################
        player.update()
        player.inputs(pressedlist)
        
        player.vel[1] += GRAVITY
        player.vel[0]  *= 0.9
        player.movevel()       
        player.color = [200,200,100]
        player.moverel(0,player.collidey(world))
        player.moverel(player.collidex(world),0)

        
        #Scrollin' on the river...
        if player.rect.right > 600:
            distance =  round(600 - player.rect.right,0)
            for listy in world:
                for thingy in listy:
                    thingy.moverel(distance,0)
            player.moverel(distance,0)

        if player.rect.left <= 40:
            distance = round(40 - player.rect.left ,0)
            for listy in world:
                for thingy in listy:
                    thingy.moverel(distance,0)
            player.moverel(distance,0)
        
        player.draw(screen)
        #if delayb > 7:
         #   pygame.image.save(screen, time.strftime("%S.bmp") )
          #  delayb = 0
        pygame.display.flip()

    
    
    

if __name__ == '__main__': main()