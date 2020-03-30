#! /usr/bin/python
# Main game loop and core fuctions
from settings import *
import random, ctypes, math, heapq, itertools, time, collections, cProfile, re, cython
import pygame as pg
import layout, pacmanrules, game, ghosts, roundrects
import pygame.rect as rect
from pygame.compat import geterror
from pygame import mixer
import pygame.display as display
from pygame import *
import pygame.surface as surface
from math import sqrt, ceil, floor
from pacmanrules import PacmanRules, GhostRules
from util import nearestPoint
from util import manhattanDistance
from ghosts import *
import threading, multiprocessing
from multiprocessing import Process, Pool, current_process
from collections import defaultdict
from roundrects import aa_round_rect


file = open("hiscore.t", "r")
hiscore = file.read()
file.close()

# Must come before pygame.init()
pg.mixer.pre_init(22050, 16, 2, 512)
pg.mixer.init()

pg.init()
#screen = pg.display.set_mode(SCREEN_SIZE.size)
clock = pg.time.Clock()
pg.display.init()
if DEBUG:
    info = pg.display.Info()
    print(info)
screen = pg.display.set_mode(DISPLAY, FLAGS, DEPTH)
pg.display.set_caption("Mokman! Use arrows or Controller Stick to move!")
screenp = pg.display.get_surface()
timer = pg.time.Clock()

seconds = 0

up = down = left = right = running = False
maplay = 'randomfMap'
level = layout.getLayout(maplay)
global levelt
levelt = level.layoutText


snd_pellet = {0: pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", 
    "pellet1.wav")),1: pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res",
    "sounds", "pellet2.wav"))}
snd_powerpellet = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds",
    "PowerPill.wav"))
snd_eatgh = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatghost.wav"))
snd_eatg2 = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatgh2.wav"))
snd_fruitbounce = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds",
    "fruitbounce.wav"))
snd_eatfruit = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatfruit.wav"))
snd_extralife = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","extralife.wav"))
snd_die = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","die.wav"))
snd_begin = pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "begin.wav"))
snd_chomp = pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "chomp.wav"))
snd_combo = pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "combo.wav"))
snd_wakka = pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "wakawakam.wav"))
snd_shep = pg.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "Sheptone.ogg"))
snd_wakka.set_volume(.9)
snd_shep.set_volume(.8)


font_name = pg.font.match_font('roboto', bold=True)
score = SCORE

def CheckInputs():
    if js!=None and js.get_axis(JS_XAXIS)>0.5:
        return DIR_RIGHT
    elif js!=None and js.get_axis(JS_XAXIS)<-0.5:
        return DIR_LEFT
    elif js!=None and js.get_axis(JS_YAXIS)>0.5:
        return DIR_DOWN
    elif js!=None and js.get_axis(JS_YAXIS)<-0.5:
        return DIR_UP

# initialise the joystick
if pg.joystick.get_count()>0:
    if JS_DEVNUM<pg.joystick.get_count(): js=pg.joystick.Joystick(JS_DEVNUM)
    else: js=pg.joystick.Joystick(0)
    js.init()
else: js=None

class Entity(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
#DIR_UP = 0  #DIR_RIGHT = 1 #DIR_DOWN = 2  #DIR_LEFT = 3 #STOPPED = 4

#-----------------------------------------------------------------------------#
#----------O---O-----This is the main game loop-----O--------O----------------#
def main():
    snd_begin.play()
    hscore = hiscore
    platforms = pg.sprite.Group()
    foods = pg.sprite.Group()
    teleports = pg.sprite.Group()
    powerups = pg.sprite.Group()
    playerX = getObjectPos(levelt, 'P', 'x')
    playerY = getObjectPos(levelt, 'P', 'y')
    ghosts = pg.sprite.Group()
    hscore = hiscore
    player = Player(platforms, (playerX, playerY), foods, teleports, powerups,
        ghosts, hscore)
    #all_sprites = pg.sprite.Group(platforms, player, ghosts, foods, teleports, powerups)
    level_width  = level.width*TILE_SIZE
    level_height = 999*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pg.Rect(0, -level_height, level_width,
        level_height))
    frame_count = 0
    frame_rate = 20
    start_time = 0
    pg.display.flip()


    # build the level and spawn ghosts
    x = y = 0
    for row in levelt:
        for col in row:
            if col == '%':
                Platform((x, y), platforms, entities)
            if col == 'T':
                Teleport((x, y), teleports, entities)
            if col == '.':
                Pacfood((x+15, y+15), foods, entities)
            if col == 'o':
                Pacpower((x+13, y+13), powerups, entities)
            if col == 'B':
                BlinkyGhosts(platforms, (x, y), ghosts, entities)
            if col == 'S':
                SlyderGhosts(platforms, (x, y), ghosts, entities)
            if col == 'W':
                WelchGhosts(platforms, (x, y), ghosts, entities)
            if col == 'C':
                ClydeGhosts(platforms, (x, y), ghosts, entities)
            if col == 'P':
                player = Player(platforms, (x, y), foods, teleports, powerups, ghosts, hscore)
                PinkyGhosts(platforms, (x-TILE_SIZE, y-(27*TILE_SIZE)), ghosts,  entities)
                InkyGhosts(platforms, (x-TILE_SIZE, y-(27*2*TILE_SIZE)), ghosts,  entities)
            x+=TILE_SIZE
        y+=TILE_SIZE
        x=0

    
    

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                exit(entities.target.hscore)
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit(entities.target.hscore)
            elif e.type == pg.JOYBUTTONDOWN:
                if e.button == 6:
                        f = open("hiscore.t", "w")
                        f.write(entities.target.hscore)
                        f.close()
                        return False

        CheckInputs()

        entities.update()
        screen.fill((0, 0, 0))
        total_seconds = frame_count // frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        entities.draw(screen)
        draw_text(screen, "Time: {0:02}:{1:02}".format(minutes, seconds), 22, 128, 10)
        draw_text(screen, "Score: " + str(entities.target.score), 24, HALF_WIDTH, 10)
        draw_text(screen, "HISCORE: " + entities.target.hscore, 26, WIN_WIDTH-128, 10)

        # Calculate total seconds
        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
        pg.display.update()
        frame_count += 1
        timedelta = timer.tick(60)
        timedelta /= 1000
#-------------------------------------------------#
#--0--0---0--end loop------O--O----O----------------#
#----core functions----------------------------#
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def getDir(self):
    if (self.vel.x>=1): return DIR_RIGHT
    if (self.vel.x<=-1): return DIR_LEFT
    if (self.vel.y<=-1): return DIR_UP
    if (self.vel.y>=1): return DIR_DOWN
    if (self.vel.y == 0 and self.vel.x == 0): return STOPPED

def getlayoutActions(self):
    x = self.laycoods.x
    y = self.laycoods.y
    #if self.currDir == DIR_DOWN or DIR_RIGHT:
    #    x -= 1
    #    y -= 1
    legals = []
    #check L
    if not isWall(x-1, y):
        legals.append(DIR_LEFT)
    #check R
    if not isWall(x+1, y):
        legals.append(DIR_RIGHT)
    #check D
    if not isWall(x, y+1):
        legals.append(DIR_DOWN)
    #check U
    if not isWall(x, y-1):
        legals.append(DIR_UP)
    
    return legals


def teleport(self, teleports):
    for t in teleports:
        if pg.sprite.collide_rect(self, t):
            if self.rect.left > 2*TILE_SIZE:
                self.rect.left = TILE_SIZE
            elif self.rect.left < 2*TILE_SIZE:
                self.rect.left = WIN_WIDTH-TILE_SIZE

def isWall(x, y):
    if levelt[int(y)][int(x)] == '%':
        return True
    else: return False

def getillegalActions(self):
    """
    Returns the illegal actions for the agent specified.
    """
    # GameState.explored.add(self)
    #if self.isWin() or self.isLose(): return []
    illegal = []
    plats = self.platforms
    velUL = -1
    velDR = 1
    copys = self
    currDir = self.dir
    if currDir == 4:
        velUL = velDR = 0
    #check LEFT
    if currDir != DIR_RIGHT:
        copys.rect.left += velUL
        legalColl(plats, copys, velUL, 0, illegal)
    #check RIGHT
    if currDir != DIR_LEFT:
        copys.rect.left += velDR
        legalColl(plats, copys, velDR, 0, illegal)
    #check DOWN
    if currDir != DIR_UP:
        copys.rect.top += velDR
        legalColl(plats, copys, 0, velDR, illegal)
    #check UP
    if currDir != DIR_DOWN:
        copys.rect.top += velUL
        legalColl(plats, copys, 0, velUL, illegal)

    return illegal

def legalColl(plts, cpys, xvel, yvel, legal):
    for p in plts:
        if pg.sprite.collide_rect(cpys, p):
            if xvel > 0:
                cpys.rect.right = p.rect.left
                legal.append(DIR_RIGHT)
            if xvel < 0:
                cpys.rect.left = p.rect.right
                legal.append(DIR_LEFT)
            if yvel > 0:
                cpys.rect.bottom = p.rect.top
                legal.append(DIR_DOWN)
            if yvel < 0:
                cpys.rect.top = p.rect.bottom
                legal.append(DIR_UP)
#DIR_UP = 0   #DIR_RIGHT = 1
#DIR_DOWN = 2 #DIR_LEFT = 3 #STOPPED=4


def getObjectPos(level, char ,coord):
    '''
    returns x or y pos based on 
    coord: of 'x' or 'y' 
    x or y * TILE_SIZE
    '''
    x = y = 0
    for row in level:
        for col in row:
            if col == char:
                if coord == 'x':
                    return x
                if coord == 'y':
                    return y
            x+=TILE_SIZE
        y+=TILE_SIZE
        x=0


def getObjectCoord(self, char):
    '''
    returns x or y pos based on rect pos
    char: of 'x' or 'y' for return
    '''
    if char == 'x':
        if self.currDir == DIR_RIGHT:
            return floor(self.rect.left/TILE_SIZE)
        else:
            return ceil(self.rect.left / TILE_SIZE)
    if char == 'y':
        if self.currDir == DIR_DOWN:
            return floor(self.rect.top/TILE_SIZE)
        else:
            return ceil(self.rect.top / TILE_SIZE)

#-----------Main Game Helper Classes-------------#
class CameraAwareLayeredUpdates(pg.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pg.Vector2(int(0), int(0))
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width/2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height/2
            self.cam += (pg.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move((int(self.cam.x), int(self.cam.y))))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty

#--------PPPPPPPLAAAAAYERRRR----------------------------#
class Player(Entity):
    '''
    Player class - initialize with player sprite and all other game
    elements
    
    Player(mapsprite,*(startX, startY), food, etc.)

    *mapsprite - master sprite object representing game world

    *startX - x coordinate for staring position

    *startY - y coordinate for staring position

    '''
    def __init__(self, platforms, pos, foods, teleports, powerups, ghosts, hscore, *groups):
        super().__init__(Color("#ebef00"), pos)
        self.dir = 4
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = True
        self.currDir = 3
        self.lastDir = 4
        self.platforms = platforms
        self.foods = foods
        self.teleports = teleports
        self.powerups = powerups
        self.ghosts = ghosts
        self.speed = PAC_SPEED*TURNBOOST
        self.turning = None
        self.change_x=0
        self.change_y=0
        self.ghostLimit=7
        self.ghostCount=0
        self.score=1
        self.combobegin= False
        self.hscore = hscore
        self.ghostState = 0
        self.ghostTimer = 0



    def update(self):
        pressed = pg.key.get_pressed()
        up = pressed[K_UP]
        down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        joyp = CheckInputs() 
        #== DIR_UP or DIR_DOWN or DIR_LEFT or DIR_RIGHT:
        #    joyp = CheckInputs
        if joyp==DIR_UP:
            up = True
            #self.dir=joyp
        if joyp==DIR_DOWN:
            down=True
            #self.dir=joyp
        if joyp==DIR_LEFT:
            left=True
            #self.dir=joyp
        if joyp==DIR_RIGHT:
            right=True
            #self.dir=joyp


        self.ghostCount=0
        for gh in self.ghosts:
            self.ghostCount+=1
        
        if self.combobegin > 100:
            snd_shep.play()

        if self.ghostCount < self.ghostLimit:
            self.spawnRandomGhost()

        self.currDir = getDir(self)
        #if getDir(self) != self.dir:
        #    self.isTurning()
        self.laycoods.x = getObjectCoord(self, 'x')
        self.laycoods.y = getObjectCoord(self, 'y')
        legals = getlayoutActions(self)
        if self.stopped == True:
            legals.append(STOPPED)
        if self.lastDir != STOPPED and DEBUG == True:
            print("currVselfVLastDir:", self.currDir, self.dir, self.lastDir)
            print("legals, l.x l.y", legals, self.laycoods.x, self.laycoods.y)
        self.lastDir = self.currDir
        if self.stopped:
            self.dir = 4
            if self.dir in legals:
                self.vel.x = 0
                self.vel.y = 0
        if right or self.dir == 1:
            self.dir = 1
            if self.dir in legals:
                self.vel.x = self.speed
                self.change_x += self.vel.x
                self.vel.y = 0
                self.stopped = False
        if left or self.dir == 3:
            self.dir = 3
            if self.dir in legals:
                self.vel.x = -self.speed
                self.change_x += self.vel.x
                self.vel.y = 0
                self.stopped = False
        if up or self.dir == 0:
            self.dir = 0
            if self.dir in legals:
                self.vel.y = -self.speed
                self.change_y += self.vel.y
                self.vel.x = 0  
                self.stopped = False
        if down or self.dir == 2:
            self.dir = 2
            if self.dir in legals:
                self.vel.y = self.speed
                self.change_y += self.vel.y
                self.vel.x = 0
                self.stopped = False
        # increment in x direction
        self.rect.left += int(self.vel.x)
        if self.vel.x != 0:
            if self.turning and abs(self.vel.x) < PAC_SPEED*TURNBOOST:
                self.vel.x *= TURNBOOST
            self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += int(self.vel.y)
        if self.vel.y != 0:
            if self.turning and abs(self.vel.y) < PAC_SPEED*TURNBOOST:
                self.vel.y *= TURNBOOST
            self.collide(0, self.vel.y, self.platforms)
        #self.foodCollide(self.foods)
        #self.teleport(self.teleports)
        #self.powerup(self.powerups)
        ghostsMove(self.ghosts, self.teleports)
        if self.ghostState == 3:
            tb = sTimer(self.ghosts, self.ghostTimer)
            if tb:
                self.ghostState = 0
                self.ghostTimer = 0
            else: 
                self.ghostTimer += 1
        score = self.score
        if DEBUG == True:
            print("v.x new.x v.y", self.vel.x, self.rect.left, self.vel.y)        
        #DIR_UP = 0  #DIR_RIGHT = 1 #DIR_DOWN = 2  #DIR_LEFT = 3
        #STOPPED = 4
        if self.score > int(self.hscore):
            self.hscore = str(self.score)

    #collide function for Mokman main player
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                curDir = getDir(self)
                if isinstance(p, ExitBlock):
                    pg.event.post(pg.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    if curDir == 1:
                        self.stopped = True
                elif xvel < 0:
                    if DEBUG == True:
                        print("s.lf p.rt", self.rect.left, p.rect.right)
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    if curDir == 3:
                        self.stopped = True
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                    if curDir == 2:
                        self.stopped = True
                elif yvel < 0:
                    self.yvel = 0
                    self.rect.top = p.rect.bottom
                    if curDir == 0:
                        self.stopped = True
        #DIR_UP = 0  #DIR_RIGHT = 1  #DIR_DOWN = 2  #DIR_LEFT = 3
        #STOPPED = 4
        self.foodCollide()
        teleport(self, self.teleports)
        self.powerup()


    def spawnRandomGhost(self):
        newghosts = pg.sprite.Group()
        SlyderGhosts(self.platforms, (18*TILE_SIZE, self.rect.top-(22*TILE_SIZE)), self.ghosts)
        BlinkyGhosts(self.platforms, (6*TILE_SIZE, self.rect.top-(24*TILE_SIZE)), self.ghosts)


    def isTurning(self):
        if getDir(self) != self.dir:
            self.turning = True
            self.speed = PAC_SPEED*TURNBOOST
        else:
            self.speed = PAC_SPEED*TURNBOOST
            self.turning = False

    def foodCollide(self):
        for f in self.foods:
            if pg.sprite.collide_rect(self, f):
                f.kill()
                self.score += 1
                snd_wakka.play()
                #snd_pellet[self.score%2].play()


    def powerup(self):
        for p in self.powerups:
            if pg.sprite.collide_rect(self, p):
                p.kill()
                gstate = 3
                self.score += 100
                ghosts.chgGhostState(self.ghosts, gstate)
                self.ghostState = gstate
                snd_powerpellet.play()

    def a(self):
        #axis of motion
        if self.dir.x != 0:
            return 'x'
        else:
            return 'y'

    def b(self):
        #axis perpinidicual to motion
        if self.dir.x != 0:
            return 'y'
        else:
            return 'x'


randomMapColours = []
randomMapColours.append("#8A2BE2")
randomMapColours.append("#FF69B4")
randomMapColours.append("#FF00FF")
randomMapColours.append("#228B22")
randomMapColours.append("#191970")
randomMapColours.append("#7FFFD4")
randomMapColours.append("#FF1493")
randomMapColours.append("#DC143C")
randomMapColours.append("#FF69B4")
randomMapColours.append("#000080")
randomMapColours.append("#B22222")
randomMapColours.append("#DA70D6")
pickint = random.randint(0, 11)

class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color(randomMapColours[pickint]), pos, *groups)

class Teleport(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("black"), pos, *groups)

class FoodEntity(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((2, 2))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Pacfood(FoodEntity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#ebef00"), pos, *groups)

class PowerEntity(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((6, 6))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Pacpower(PowerEntity):
    def __init__(self, pos, *groups):
        super().__init__(Color("white"), pos, *groups)


class ExitBlock(Platform):
    def __init__(self, pos, *groups):
        super().__init__(Color("#ebef00"), pos, *groups)

def exit(hscore):
    f = open("hiscore.t", "w")
    f.write(hscore)
    f.close()
    pg.quit()
    sys.exit(0)
    

if __name__ == "__main__":
    main()