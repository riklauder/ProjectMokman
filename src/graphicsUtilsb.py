# graphicsUtils.py
# ----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import sys
import math
import random
import string
import time
import types
#import tkinter
import pygame as pg
import random
import layout, util
from pygame.locals import *
from pygame import *
from math import sqrt
import shlex
import pygamecam

WIN_WIDTH = 860
WIN_HEIGHT = 800
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30
SCREEN_SIZE = pg.Rect((0, 0, 860, 800))
TILE_SIZE = 32 
GRAVITY = pg.Vector2((0, 0))
WALL_RADIUS = 24
WALL_WIDTH=3
DIR_UP = 0;
DIR_RIGHT = 1;
DIR_DOWN = 2;
DIR_LEFT = 3;
SCRIPT_PATH=sys.path[0]

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
YELLOW=         (255, 255,   0)
PINK=           (255, 105, 180)
LIGHTBLUE=      (135, 206, 250)
RED=            (255,   0,   0)
LIGHTPINK=      (255, 182, 193)

_Windows = sys.platform == 'win32'  # True if on Win95/98/NT

_root_window = None      # The root window for graphics output
screen = None      # The canvas which holds graphics
screen_xs = None      # Size of canvas object
screen_ys = None
screen_x = None      # Current position on canvas
screen_y = None
screen_col = None      # Current colour (set to black below)
screen_tsize = 12
screen_tserifs = 0

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

def colorToVector(color):
    return map(lambda x: int(x, 16) / 256.0, [color[1:3], color[3:5], color[5:7]])

if _Windows:
    screen_tfonts = ['times new roman', 'lucida console']
else:
    screen_tfonts = ['times', 'lucidasans-24']
    pass # XXX need defaults here

def sleep(secs):
    global _root_window
    if _root_window == None:
        time.sleep(secs)
    else:
        _root_window.update_idletasks()
        _root_window.after(int(1000 * secs), _root_window.quit)
        _root_window.mainloop()

def begin_graphics(width=WIN_WIDTH, height=WIN_HEIGHT, color=formatColor(0, 0, 0), title=None):

    global _root_window, screen, screen_x, screen_y, screen_xs, screen_ys, _bg_color

    # Check for duplicate call
    if _root_window is not None:
        # Lose the window.
        # _root_window.destroy()
        _destroy_window()
        
    # Save the canvas size parameters
    screen_xs, screen_ys = width - 1, height - 1
    screen_x, screen_y = 0, screen_ys
    _bg_color = color
    
    # Create the root window
    clock = timer = pg.time.Clock()
    pg.init()
    _root_window = pg.display.set_mode(DISPLAY, FLAGS, DEPTH)
    screen = _root_window
    pg.display.set_caption("Pacman")
    screenp = pg.display.get_surface()

    maplay = 'randomfMap'
    level = layout.getLayout(maplay)
    levelt = level.layoutText
    platforms = pg.sprite.Group()
    playerX = pygamecam.getObjectPos(levelt, 'P', 'x')
    playerY = pygamecam.getObjectPos(levelt, 'P', 'y')
    player = pygamecam.Player(platforms, (playerX, playerY))
    level_width  = level.width*TILE_SIZE
    level_height = level.height*TILE_SIZE
    entities = pygamecam.CameraAwareLayeredUpdates(player, pg.Rect(0, -level_height, level_width, level_height))

    # build the level    
    x = y = 0
    for row in levelt:
        for col in row:
            if col == '%':
                pygamecam.Platform((x, y), platforms, entities)
            if col == 'P':
                player = pygamecam.Player(platforms, (x, y))
            x+=TILE_SIZE
        y+=TILE_SIZE
        x=0

    while 1:

        for e in pg.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pg.display.update()
        timer.tick(60)

    # Bind to key-down and key-up events
    up = down = left = right = running = False

_leftclick_loc = None
_rightclick_loc = None
_ctrl_leftclick_loc = None

def _leftclick(event):
  global _leftclick_loc
  _leftclick_loc = (event.x, event.y)

def _rightclick(event):
  global _rightclick_loc
  _rightclick_loc = (event.x, event.y)

def _ctrl_leftclick(event):
  global _ctrl_leftclick_loc
  _ctrl_leftclick_loc = (event.x, event.y)

def wait_for_click():
  while True:
    global _leftclick_loc
    global _rightclick_loc
    global _ctrl_leftclick_loc
    if _leftclick_loc != None:
      val = _leftclick_loc
      _leftclick_loc = None
      return val, 'left'
    if _rightclick_loc != None:
      val = _rightclick_loc
      _rightclick_loc = None
      return val, 'right'
    if _ctrl_leftclick_loc != None:
      val = _ctrl_leftclick_loc
      _ctrl_leftclick_loc = None
      return val, 'ctrl_left'
    sleep(0.05)  

def draw_background():
    corners = [(0,0), (0, screen_ys), (screen_xs, screen_ys), (screen_xs, 0)]
    polygon(corners, _bg_color, fillColor=_bg_color, filled=True, smoothed=False)
    
def _destroy_window(event=None):
    """Click the close button in the tkinter window."""

    print("DESTROY")
    event.exit(0)

   # global _root_window
   # _root_window.destroy()
   # _root_window = None

def end_graphics():
    global _root_window, screen, _mouse_enabled
    try:
      try:
        sleep(1)
        # if _root_window != None: 
        #   _root_window.destroy()
      except SystemExit as e:
        print('Ending graphic raised an exception:', e)
    finally:
      # _root_window = None
      # screen = None
      # _mouse_enabled = 0
      # _clear_keys()
      pass

def clear_screen(background=None):
    global screen_x, screen_y
    screen.fill((0, 0, 0))
    draw_background()
    screen_x, screen_y = 0, screen_ys

def polygon(coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
  c = []
  for coord in coords:
    c.append(coord[0])
    c.append(coord[1])
  if fillColor == None: fillColor = outlineColor
  if filled == 0: fillColor = ""
  poly = screen.create_polygon(c, outline=outlineColor, fill=fillColor, smooth=smoothed, width=width)
  if behind > 0:    
    screen.tag_lower(poly, behind) # Higher should be more visible
  return poly
  
def square(pos, r, color, filled=1, behind=0):
    x, y = pos
    coords = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
    return polygon(coords, color, color, filled, 0, behind=behind)

def circle(pos, r, outlineColor, fillColor, endpoints=None, style='pieslice', width=2):
    x, y = pos
    x0, x1 = x - r - 1, x + r
    y0, y1 = y - r - 1, y + r
    if endpoints == None:
      e = [0, 359]
    else:
      e = list(endpoints)
    while e[0] > e[1]: e[1] = e[1] + 360

    return screen.create_arc(x0, y0, x1, y1, outline=outlineColor, fill=fillColor,
                              extent=e[1] - e[0], start=e[0], style=style, width=width)

def image(pos, file="../../blueghost.gif"):
    x, y = pos
    # img = PhotoImage(file=file)
    return screen.create_image(x, y, image = pg.image(file=file), anchor = pg.NW)
    
    
def refresh():
    screen.update_idletasks()
                                                    
def moveCircle(id, pos, r, endpoints=None):
    global screen_x, screen_y
    
    x, y = pos
    # x0, x1 = x - r, x + r + 1
    # y0, y1 = y - r, y + r + 1
    x0, x1 = x - r - 1, x + r
    y0, y1 = y - r - 1, y + r
    if endpoints == None:
      e = [0, 359]
    else:
      e = list(endpoints)
    while e[0] > e[1]: e[1] = e[1] + 360

    edit(id, ('start', e[0]), ('extent', e[1] - e[0]))
    move_to(id, x0, y0)

def edit(id, *args):
    screen.itemconfigure(id, **dict(args))
    
def text(pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
    global screen_x, screen_y
    x, y = pos
    font = (font, str(size), style)
    return screen.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)

def changeText(id, newText, font=None, size=12, style='normal'):
  screen.itemconfigure(id, text=newText)
  if font != None:
    screen.itemconfigure(id, font=(font, '-%d' % size, style))

def changeColor(id, newColor):
    screen.itemconfigure(id, fill=newColor)

def line(here, there, color=formatColor(0, 0, 0), width=2):
    x0, y0 = here[0], here[1]
    x1, y1 = there[0], there[1]
    return screen.create_line(x0, y0, x1, y1, fill=color, width=width)

##############################################################################
### Keypress handling ########################################################
##############################################################################

# We bind to key-down and key-up events.

_keysdown = {}
_keyswaiting = {}
# This holds an unprocessed key release.  We delay key releases by up to
# one call to keys_pressed() to get round a problem with auto repeat.
_got_release = None

def _keypress(event):
    global _got_release
    # remap_arrows(event)
    _keysdown[event.keysym] = 1
    _keyswaiting[event.keysym] = 1
    # print(event.char, event.keycode)
    _got_release = None

def _keyrelease(event):
    global _got_release
    # remap_arrows(event)
    try:
      del _keysdown[event.keysym]
    except:
      pass
    _got_release = 1
    
def remap_arrows(event):
    # TURN ARROW PRESSES INTO LETTERS (SHOULD BE IN KEYBOARD AGENT)
    if event.char in ['a', 's', 'd', 'w']:
      return
    if event.keycode in [37, 101]: # LEFT ARROW (win / x)
      event.char = 'a'
    if event.keycode in [38, 99]: # UP ARROW
      event.char = 'w'
    if event.keycode in [39, 102]: # RIGHT ARROW
      event.char = 'd'
    if event.keycode in [40, 104]: # DOWN ARROW
      event.char = 's'

def _clear_keys(event=None):
    global _keysdown, _got_release, _keyswaiting
    _keysdown = {}
    _keyswaiting = {}
    _got_release = None

def keys_pressed(d_o_e=lambda arg: _root_window.dooneevent(arg),
                 d_w=pg.key.get_pressed):
    d_o_e(d_w)
    if _got_release:
      d_o_e(d_w)
    return _keysdown.keys()
  
def keys_waiting():
    global _keyswaiting
    keys = _keyswaiting.keys()
    # print(_keyswaiting, keys)
    _keyswaiting = {}
    return keys

# Block for a list of keys...
def wait_for_keys():
    keys = []
    while keys == []:
        keys = keys_pressed()
        sleep(0.05)
    return keys

def remove_from_screen(x,
                       d_o_e=lambda arg: _root_window.dooneevent(arg),
                       d_w=pg.key.get_pressed):
    screen.delete(x)
    d_o_e(d_w)

def _adjust_coords(coord_list, x, y):
    for i in range(0, len(coord_list), 2):
        coord_list[i] = coord_list[i] + x
        coord_list[i + 1] = coord_list[i + 1] + y
    return coord_list

def move_to(object, x, y=None,
            d_o_e=lambda arg: _root_window.dooneevent(arg),
            d_w=pg.key.get_pressed):
    if y is None:
        try: x, y = x
        except: raise Exception('incomprehensible coordinates')
        
    horiz = True
    newCoords = []
    current_x, current_y = screen.coords(object)[0:2] # first point
    for coord in  screen.coords(object):
      if horiz:  
        inc = x - current_x
      else:      
        inc = y - current_y
      horiz = not horiz
      
      newCoords.append(coord + inc)
    
    screen.coords(object, *newCoords)
    d_o_e(d_w)
    
def move_by(object, x, y=None,
            d_o_e=lambda arg: _root_window.dooneevent(arg),
            d_w=pg.key.get_pressed):
    if y is None:
        try: x, y = x
        except: raise Exception('incomprehensible coordinates')
    
    horiz = True
    newCoords = []
    for coord in  screen.coords(object):
      if horiz:  
        inc = x
      else:      
        inc = y
      horiz = not horiz
      
      newCoords.append(coord + inc)
      
    screen.coords(object, *newCoords)
    d_o_e(d_w)
    
def writePostscript(filename):
    """Writes the current canvas to a postscript file."""
    psfile = open(filename, 'w')
    psfile.write(screen.postscript(pageanchor='sw',
                   y='0.c', 
                   x='0.c'))
    psfile.close()
  
ghost_shape = [                
    (0, - 0.5),
    (0.25, - 0.75),
    (0.5, - 0.5),
    (0.75, - 0.75),
    (0.75, 0.5),
    (0.5, 0.75),
    (- 0.5, 0.75),
    (- 0.75, 0.5),
    (- 0.75, - 0.75),
    (- 0.5, - 0.5),
    (- 0.25, - 0.75)
]

if __name__ == '__main__':
    begin_graphics()
    clear_screen()
    ghost_shape = [(x * 10 + 20, y * 10 + 20) for x, y in ghost_shape]
    g = polygon(ghost_shape, formatColor(1, 1, 1))
    move_to(g, (50, 50))
    circle((150, 150), 20, formatColor(0.7, 0.3, 0.0), endpoints=[15, - 15])
    sleep(2)
