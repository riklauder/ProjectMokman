#not /usr/bin/python
import sys
import random
import math

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

# get direction enum from a direction vector
def getEnumFromDir (dir) :
    if (dir.x==-1): return DIR_LEFT
    if (dir.x==1): return DIR_RIGHT
    if (dir.y==-1): return DIR_UP
    if (dir.y==1): return DIR_DOWN


# set direction vector from a direction enum
def setDirFromEnum (dir,dirEnum):
    if dirEnum == DIR_UP: 
        dir.x = 0 
        dir.y = -1 
    elif dirEnum == DIR_RIGHT: 
        dir.x =1 
        dir.y = 0 
    elif dirEnum == DIR_DOWN: 
        dir.x = 0 
        dir.y = 1 
    elif dirEnum == DIR_LEFT: 
        dir.x = -1 
        dir.y = 0 


# size of a square tile in pixels
tileSize = 8


# constructor
class Map:
    def __init__ (self, numCols, numRows, tiles=None):

        self.numCols = numCols
        self.numRows = numRows
        self.numTiles = numCols*numRows
        self.widthPixels = numCols*tileSize
        self.heightPixels = numRows*tileSize

        # ascii map
        self.tiles = mapgen()

        self.resetCurrent()
        self.parseWalls()


    # reset current tiles
    def resetCurrent (self) :
        self.currentTiles = ""

    # self is a procedural way to generate original-looking maps from a simple ascii tile
    # map without a spritesheet.
    def parseWalls(self) :

        # creates a list of drawable canvas paths to render the map walls
        self.paths = []

        # a map of wall tiles self already belong to a built path
        visited = []

# we extend the x range to suggest the continuation of the tunnels
    def toIndex (self, x,y) :
        if (x>=-2 and x<self.numCols+2) and (y>=0 and y<self.numRows):
            return (x+2)+y*(self.numCols+4)
            

    # a map of which wall tiles self are not completely surrounded by other wall tiles
    def edges(self):    
        for y in self.numRows:
            for x in self.umCols+2 :
                if (self.getTile(x,y) == '|' and 
                    self.getTile(x-1,y) != '|' or
                    self.getTile(x+1,y) != '|' or
                    self.getTile(x,y-1) != '|' or
                    self.getTile(x,y+1) != '|' or
                    self.getTile(x-1,y-1) != '|' or
                    self.getTile(x-1,y+1) != '|' or
                    self.getTile(x+1,y-1) != '|' or
                    self.getTile(x+1,y+1) != '|'):
                    edges[i] = True
            
        
    

    # walks along edge wall tiles starting at the given index to build a canvas path
    def makePath (self, tx,ty) :

        # get initial direction
        dir
        dirEnum = []
        if (toIndex(tx+1,ty) in edges):
            dirEnum = DIR_RIGHT
        elif (toIndex(tx, ty+1) in edges):
            dirEnum = DIR_DOWN
        else:
            setDirFromEnum(dir,dirEnum)
        # increment to next tile
        tx += dir.x
        ty += dir.y
        # backup initial location and direction
        init_tx = tx
        init_ty = ty
        init_dirEnum = dirEnum
        path = []
        pad = []
        # (persists for each call to getStartPoint)
        point = []
        lastPoint = []
        turn = []
        turnAround = []
        while (True) :
            visited = visited[toIndex(tx,ty)] = True
            # determine start point
            point = getStartPoint(tx,ty,dirEnum)
            if (turn) :
                # if we're turning into self tile, create a control point for the curve
                #
                # >---+  <- control point
                #     |
                #     V
                lastPoint = path[path.length-1]
                if (dir.x == 0) :
                    point.cx = point.x
                    point.cy = lastPoint.y
                
                else :
                    point.cx = lastPoint.x
                    point.cy = point.y
                
            
            # update direction
            turn = False
            turnAround = False
            if (toIndex(tx+dir.y, ty-dir.x) in edges) : # turn left
                dirEnum = (dirEnum+3)%4
                turn = True
            
            elif (toIndex(tx+dir.x, ty+dir.y) in edges) : # continue straight
                dirEnum = dirEnum
            elif (toIndex(tx-dir.y, ty+dir.x) in edges) : # turn right
                dirEnum = (dirEnum+1)%4
                turn = True
            
            else : # turn around
                dirEnum = (dirEnum+2)%4
                turnAround = True
            
            setDirFromEnum(dir,dirEnum)
            # commit path point
            path.push(point)
            # special case for turning around (have to connect more dots manually)
            if (turnAround) :
                path.push(getStartPoint(tx-dir.x, ty-dir.y, (dirEnum+2)%4))
                path.push(getStartPoint(tx, ty, dirEnum))
            
            # advance to the next wall
            tx += dir.x
            ty += dir.y
            # exit at full cycle
            if (tx==init_tx and ty==init_ty and dirEnum == init_dirEnum) :
                self.paths.push(path)
                break
            
            # iterate through all edges, making a new path after hitting an unvisited wall edge
            i = 0
            for y in self.numRowsy:
                for x in self.numCls+2:
                    if x in edges and i not in visited :
                        visited[x] = True
                        makePath(x,y)
                        i+=2
            

        def getStartPoint (tx,ty,dirEnum) :
            dir = []
            setDirFromEnum(dir, dirEnum)
            if (not(toIndex(tx+dir.y,ty-dir.x) in edges)):
                if self.pad == self.isFloorTile(tx+dir.y,ty-dir.x):
                    self.pad = 5 
                else: self.pad = 0
                px = -tileSize/2+pad
                py = tileSize/2
                a = dirEnum*math.PI/2
                c = math.cos(a)
                s = math.sin(a)
            return{
                # the first expression is the rotated point centered at origin
                # the second expression is to translate it to the tile
                (px*c - py*s) + (tx+0.5)*tileSize,
                (px*s + py*c) + (ty+0.5)*tileSize
            }
            
        

    def posToIndex (self,x,y) :
        if (x>=0 and x<self.numCols and y>=0 and y<self.numRows):
            return x+y*self.numCols

    # retrieves tile character at given coordinate
    # extended to include offscreen tunnel space
    def getTile (self,x,y) :
        if (x>=0 and x<self.numCols and y>=0 and y<self.numRows):
            return self.currentTiles[self.posToIndex(x,y)]
        # extend walls and paths outward for entrances and exits
        if ((x==-1           and self.getTile(x+1,y)=='|' and (self.isFloorTile(x+1,y+1) or self.isFloorTile(x+1,y-1))) or
            (x==self.numCols and self.getTile(x-1,y)=='|' and (self.isFloorTile(x-1,y+1) or self.isFloorTile(x-1,y-1)))):
            return '%'
        if ((x==-1           and self.isFloorTile(x+1,y)) or
            (x==self.numCols and self.isFloorTile(x-1,y))):
            return ' '


    # determines if the given character is a walkable floor tile
    def isFloorTileChar (self, tile) :
        return tile==' ' or tile=='.' or tile=='o'


    # determines if the given tile coordinate has a walkable floor tile
    def isFloorTile (self,x,y) :
        return self.isFloorTileChar(self.getTile(x,y))


    def mapgen(self):
        def getRandomInt (min,max) :
            return math.floor(math.random() * (max-min+1)) + min
        

        def shuffle (list) :
            len = list.length
            for i in len :
                j = getRandomInt(0,len-1)
                temp = list[i]
                list[i] = list[j]
                list[j] = temp
            
        
        def randomElement (list) :
            len = list.length
            if (len > 0) :
                return list[getRandomInt(0,len-1)]
            
        

        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

        cells = []
        tallRows = []
        narrowCols = []

        rows = 9
        cols = 5

        def reset () :
            # initialize cells
            for i in rows*cols :
                cells[i] = {
                    i%cols,
                    math.floor(i/cols),
                    False,
                    [False, False, False, False],
                    [],
                    None,
                    None
                }
                
            
            # allow each cell to refer to surround cells by direction
            for i in rows*cols:
                c = cells[i]
                if (c.x > 0):
                    c.next[LEFT] = cells[i-1]
                if (c.x < cols - 1):
                    c.next[RIGHT] = cells[i+1]
                if (c.y > 0):
                    c.next[UP] = cells[i-cols]
                if (c.y < rows - 1):
                    c.next[DOWN] = cells[i+cols]
            
            # define the ghost home square
            i = 3*cols
            c = cells[i]
            c.filled=True
            c.connect[LEFT] = c.connect[RIGHT] = c.connect[DOWN] = True
            i+=1
            c = cells[i]
            c.filled=True
            c.connect[LEFT] = c.connect[DOWN] = True
            i+=cols-1
            c = cells[i]
            c.filled=True
            c.connect[LEFT] = c.connect[UP] = c.connect[RIGHT] = True
            i+=1
            c = cells[i]
            c.filled=True
            c.connect[UP] = c.connect[LEFT] = True
        
        def genRandom () :
            def getLeftMostEmptyCells () :
                leftCells = []
                for x in cols :
                    for y in rows :
                        c = cells[x+y*cols]
                        if not(c.filled) :
                            leftCells.push(c)
                        
                    
                    if (leftCells.length > 0) :
                        break
                    
                
                return leftCells
            
            def isOpenCell (cell,i,prevDir,size) :
                # prevent wall from going through starting position
                if (cell.y == 6 and cell.x == 0 and i == DOWN or 
                    cell.y == 7 and cell.x == 0 and i == UP) :
                    return False
                
                # prevent long straight pieces of length 3
                if (size == 2 and (i==prevDir or  (i+2)%4==prevDir)) :
                    return False
                
                # examine an adjacent empty cell
                if (cell.next[i] and cell.next[i].filled) :
                    
                    # only open if the cell to the left of it is filled
                    if (cell.next[i].next[LEFT] and not cell.next[i].next[LEFT].filled) :
                        return
                    else :
                        return True
                    
                
                return False
            def getOpenCells (cell,prevDir,size) :
                openCells = []
                numOpenCells = 0
                for i in 4 :
                    if (isOpenCell(cell,i,prevDir,size)) :
                        openCells.push(i)
                        numOpenCells += 1
                    
                
                return {openCells: openCells, numOpenCells: numOpenCells}
            
            def connectCell (cell,dir) :
                cell.connect[dir] = True
                cell.next[dir].connect[(dir+2)%4] = True
                if (cell.x == 0 and dir == RIGHT) :
                    cell.connect[LEFT] = True
                
            
            def gen () :
            
                cell = []     # cell at the center of growth (open cells are chosen around this cell)
                newCell = []  # most recent cell filled
                firstCell = []# the starting cell of the current group
                openCells = []   # list of open cells around the center cell
                numOpenCells = [] # size of openCells
                dir = []# the most recent direction of growth relative to the center cell
                numFilled = 0  # current count of total cells filled
                size = []          # current number of cells in the current group
                probStopGrowingAtSize = [ # probability of stopping growth at sizes...
                        0,     # size 0
                        0,     # size 1
                        0.10,  # size 2
                        0.5,   # size 3
                        0.75,  # size 4
                        1]    # size 5
                # A single cell group of size 1 is allowed at each row at y=0 and y=rows-1,
                # so keep count of those created.
                singleCount = []
                singleCount[0] = singleCount[rows-1] = 0
                probTopAndBotSingleCellJoin = 0.35
                # A count and limit of the number long pieces (i.e. an "L" of size 4 or "T" of size 5)
                longPieces = 0
                maxLongPieces = 1
                probExtendAtSize2 = 1
                probExtendAtSize3or4 = 0.5
                def fillCell (cell) :
                    cell.filled = True
                    cell.no = self.numFilled+1
                    cell.group = numGroups
                
                for numGroups in numGroups :
                    # find all the leftmost empty cells
                    openCells = getLeftMostEmptyCells()
                    # stop add pieces if there are no more empty cells.
                    numOpenCells = openCells.length
                    if (numOpenCells == 0) :
                        break
                    
                    # choose the center cell to be a random open cell, and fill it.
                    firstCell = cell = openCells[getRandomInt(0,numOpenCells-1)]
                    fillCell(cell)
                    # randomly allow one single-cell piece on the top or bottom of the map.
                    if (cell.x < cols-1 and (cell.y in singleCount) and math.random() <= probTopAndBotSingleCellJoin) :
                        if (singleCount[cell.y] == 0) :
                            if cell.connect[cell.y] == 0 :
                                cell.connect[cell.y] = UP
                            else: cell.connect[cell.y] = DOWN
                            singleCount[cell.y]+=1
                            continue
                        
                    
                    # number of cells in this contiguous group
                    size = 1
                    if (cell.x == cols-1) :
                        # if the first cell is at the right edge, then don't grow it.
                        cell.connect[RIGHT] = True
                        cell.isRaiseHeightCandidate = True
                    
                    else :
                        # only allow the piece to grow to 5 cells at most.
                        while (size < 5) :
                            stop = False
                            if (size == 2) :
                                # With a horizontal 2-cell group, try to turn it into a 4-cell "L" group.
                                # This is done here because this case cannot be reached when a piece has already grown to size 3.
                                c = firstCell
                                if (c.x > 0 and c.connect[RIGHT] and c.next[RIGHT] and c.next[RIGHT].next[RIGHT]) :
                                    if (longPieces < maxLongPieces and math.random() <= probExtendAtSize2) :
                                        c = c.next[RIGHT].next[RIGHT]
                                        dirs = []
                                        if (isOpenCell(c,UP)) :
                                            dirs[UP] = True
                                        
                                        if (isOpenCell(c,DOWN)) :
                                            dirs[DOWN] = True
                                        
                                        if (dirs[UP] and dirs[DOWN]) :
                                            i = [UP,DOWN][getRandomInt(0,1)]
                                        
                                        elif (dirs[UP]) :
                                            i = UP
                                        
                                        elif (dirs[DOWN]) :
                                            i = DOWN
                                        
                                        else :
                                            i = None
                                        
                                        if i != None:
                                            connectCell(c,LEFT)
                                            fillCell(c)
                                            connectCell(c,i)
                                            fillCell(c.next[i])
                                            longPieces+=1
                                            size+=2
                                            stop = True
                                        
                                    
                                
                            
                            if not(stop) :
                                # find available open adjacent cells.
                                result = getOpenCells(cell,dir,size)
                                openCells = result['openCells']
                                numOpenCells = result['numOpenCells']
                                # if no open cells found from center point, then use the last cell as the new center
                                # but only do this if we are of length 2 to prevent numerous short pieces.
                                # then recalculate the open adjacent cells.
                                if (numOpenCells == 0 and size == 2) :
                                    cell = newCell
                                    result = getOpenCells(cell,dir,size)
                                    openCells = result['openCells']
                                    numOpenCells = result['numOpenCells']
                                
                                # no more adjacent cells, so stop growing this piece.
                                if (numOpenCells == 0) :
                                    stop = True
                                
                                else :
                                    # choose a random valid direction to grow.
                                    dir = openCells[getRandomInt(0,numOpenCells-1)]
                                    newCell = cell.next[dir]
                                    # connect the cell to the new cell.
                                    connectCell(cell,dir)
                                    # fill the cell
                                    fillCell(newCell)
                                    # increase the size count of this piece.
                                    size+=1
                                    # don't let center pieces grow past 3 cells
                                    if (firstCell.x == 0 and size == 3) :
                                        stop = True
                                    
                                    # Use a probability to determine when to stop growing the piece.
                                    if (math.random() <= probStopGrowingAtSize[size]) :
                                        stop = True
                                    
                                
                            
                            # Close the piece.
                            if (stop) :
                                if (size == 1) :
                                    # This is provably impossible because this loop is never entered with size==1.
                                    {}
                                elif (size == 2) :
                                    # With a vertical 2-cell group, attach to the right wall if adjacent.
                                    c = firstCell
                                    if (c.x == cols-1) :
                                        # select the top cell
                                        if (c.connect[UP]) :
                                            c = c.next[UP]
                                        
                                        c.connect[RIGHT] = c.next[DOWN].connect[RIGHT] = True
                                    
                                    
                                
                                elif (size == 3 or  size == 4) :
                                    # Try to extend group to have a long leg
                                    if (longPieces < maxLongPieces and firstCell.x > 0 and math.random() <= probExtendAtSize3or4) :
                                        dirs = []
                                        dirsLength = 0
                                        for i in 4 :
                                            if (cell.connect[i] and isOpenCell(cell.next[i],i)) :
                                                dirs.push(i)
                                                dirsLength+=1
                                            
                                        
                                        if (dirsLength > 0) :
                                            i = dirs[getRandomInt(0,dirsLength-1)]
                                            c = cell.next[i]
                                            connectCell(c,i)
                                            fillCell(c.next[i])
                                            longPieces+=1
                                        
                                    
                                
                                break
                            
                        
                    
                
                setResizeCandidates()
            
            def setResizeCandidates () :
                c = []
                q = []
                c2 = []
                q2 = []
                x = []
                y = []
                for i in rows*cols :
                    c = cells[i]
                    x = i % cols
                    y = math.floor(i/cols)
                    # determine if it has flexible height
                    #
                    # |_|
                    #
                    # or
                    #  _
                    # | |
                    #
                    q = c.connect
                    if ((c.x == 0 or  not q[LEFT]) and
                        (c.x == cols-1 or  not q[RIGHT]) and q[UP] != q[DOWN]) :
                        c.isRaiseHeightCandidate = True
                    
                    #  _ _
                    # |_ _|
                    #
                    c2 = c.next[RIGHT]
                    if (c2 != None) :
                        q2 = c2.connect
                        if (((c.x == 0 or  not q[LEFT]) and not q[UP] and not q[DOWN]) and
                            ((c2.x == cols-1 or  not q2[RIGHT]) and not q2[UP] and not q2[DOWN])) :
                            c.isRaiseHeightCandidate = c2.isRaiseHeightCandidate = True
                        
                    
                    # determine if it has flexible width
                    # if cell is on the right edge with an opening to the right
                    if (c.x == cols-1 and q[RIGHT]) :
                        c.isShrinkWidthCandidate = True
                    
                    #  _
                    # |_
                    # 
                    # or
                    #  _
                    #  _|
                    #
                    if ((c.y == 0 or  not q[UP]) and
                        (c.y == rows-1 or  not q[DOWN]) and q[LEFT] != q[RIGHT]) :
                        c.isShrinkWidthCandidate = True
                    
                
            
            # Identify if a cell is the center of a cross.
            def cellIsCrossCenter (c) :
                return c.connect[UP] and c.connect[RIGHT] and c.connect[DOWN] and c.connect[LEFT]
            
            def chooseNarrowCols () :
                def canShrinkWidth (x,y) :
                    # Can cause no more tight turns.
                    if (y==rows-1) :
                        return True
                    
                    # get the right-hand-side bound
                    c=[]
                    c2 =[]
                    for x0 in cols:
                        c = cells[x0+y*cols]
                        c2 = c.next[DOWN]
                        if ((not c.connect[RIGHT] or  cellIsCrossCenter(c)) and
                            (not c2.connect[RIGHT] or  cellIsCrossCenter(c2))) :
                            break
                        
                    
                    # build candidate list
                    candidates = []
                    numCandidates = 0
                    for ci in c2.next[LEFT] :
                        if (c2.isShrinkWidthCandidate) :
                            candidates.push(c2)
                            numCandidates+=1
                        
                        # cannot proceed further without causing irreconcilable tight turns
                        if ((not c2.connect[LEFT] or  cellIsCrossCenter(c2)) and
                            (not c2.next[UP].connect[LEFT] or  cellIsCrossCenter(c2.next[UP]))) :
                            break
                        
                    
                    shuffle(candidates)
                    for i in numCandidates :
                        c2 = candidates[i]
                        if (canShrinkWidth(c2.x,c2.y)) :
                            c2.shrinkWidth = True
                            narrowCols[c2.y] = c2.x
                            return True
                        
                    
                    return False
                
                c =[]
                for x in cols-1:
                    c = cells[x]
                    if (c.isShrinkWidthCandidate and canShrinkWidth(x,0)) :
                        c.shrinkWidth = True
                        narrowCols[c.y] = c.x
                        return True
                    
                
                return False
            
            def chooseTallRows () :
                def canRaiseHeight (x,y) :
                    # Can cause no more tight turns.
                    if (x==cols-1) :
                        return True
                    
                    # find the first cell below that will create too tight a turn on the 
                    c =[]
                    c2=[]
                    for y0 in y:
                        c = cells[x+y0*cols]
                        c2 = c.next[RIGHT]
                        if ((not c.connect[UP] or  cellIsCrossCenter(c)) and 
                            (not c2.connect[UP] or  cellIsCrossCenter(c2))) :
                            break
                        
                    
                    # Proceed from the right cell upwards, looking for a cell that can be raised.
                    candidates = []
                    numCandidates = 0
                    for c2 in c2 :
                        if (c2.isRaiseHeightCandidate) :
                            candidates.push(c2)
                            numCandidates+=1
                        
                        # cannot proceed further without causing irreconcilable tight turns
                        if ((not c2.connect[DOWN] or  cellIsCrossCenter(c2)) and
                            (not c2.next[LEFT].connect[DOWN] or  cellIsCrossCenter(c2.next[LEFT]))) :
                            break
                        
                    
                    shuffle(candidates)
                    for i in numCandidates:
                        c2 = candidates[i]
                        if (canRaiseHeight(c2.x,c2.y)) :
                            c2.raiseHeight = True
                            tallRows[c2.x] = c2.y
                            return True
                        
                    
                    return False
                
                # From the top left, examine cells below until hitting top of ghost house.
                # A raisable cell must be found before the ghost house.
                c=[]
                for y in 3:
                    c = cells[y*cols]
                    if (c.isRaiseHeightCandidate and canRaiseHeight(0,y)) :
                        c.raiseHeight = True
                        tallRows[c.x] = c.y
                        return True
                    
                
                return False
            
            # This is a function to detect impurities in the map that have no heuristic implemented to avoid it yet in gen().
            def isDesirable () :
                # ensure a solid top right corner
                c = cells[4]
                if (c.connect[UP] or  c.connect[RIGHT]) :
                    return False
                
                # ensure a solid bottom right corner
                c = cells[rows*cols-1]
                if (c.connect[DOWN] or  c.connect[RIGHT]) :
                    return False
                
                # ensure there are no two stacked/side-by-side 2-cell pieces.
                def isHori (x,y) :
                    q1 = cells[x+y*cols].connect
                    q2 = cells[x+1+y*cols].connect
                    return not q1[UP] and not q1[DOWN] and (x==0 or  not q1[LEFT]) and q1[RIGHT] and not q2[UP] and not q2[DOWN] and q2[LEFT] and not q2[RIGHT]
                
                def isVert (x,y) :
                    q1 = cells[x+y*cols].connect
                    q2 = cells[x+(y+1)*cols].connect
                    if (x==cols-1) :
                        # special case (we can consider two single cells as vertical at the right edge)
                        return not q1[LEFT] and not q1[UP] and not q1[DOWN] and not q2[LEFT] and not q2[UP] and not q2[DOWN]
                    
                    return not q1[LEFT] and not q1[RIGHT] and not q1[UP] and q1[DOWN] and not q2[LEFT] and not q2[RIGHT] and q2[UP] and not q2[DOWN]
                
                g = []
                for y in rows :
                    for x in cols :
                        if (isHori(x,y) and isHori(x,y+1) or 
                            isVert(x,y) and isVert(x+1,y)) :
                            # don't allow them in the middle because they'll be two large when reflected.
                            if (x==0) :
                                return False
                            
                            # Join the four cells to create a square.
                            cells[x+y*cols].connect[DOWN] = True
                            cells[x+y*cols].connect[RIGHT] = True
                            g = cells[x+y*cols].group
                            cells[x+1+y*cols].connect[DOWN] = True
                            cells[x+1+y*cols].connect[LEFT] = True
                            cells[x+1+y*cols].group = g
                            cells[x+(y+1)*cols].connect[UP] = True
                            cells[x+(y+1)*cols].connect[RIGHT] = True
                            cells[x+(y+1)*cols].group = g
                            cells[x+1+(y+1)*cols].connect[UP] = True
                            cells[x+1+(y+1)*cols].connect[LEFT] = True
                            cells[x+1+(y+1)*cols].group = g
                        
                    
                
                if (not chooseTallRows()) :
                    return False
                
                if (not chooseNarrowCols()) :
                    return False
                
                return True
            
            # set the final position and size of each cell when upscaling the simple model to actual size
            def setUpScaleCoords () :
                c=[]
                for i in rows*cols :
                    c = cells[i]
                    c.final_x = c.x*3
                    if (narrowCols[c.y] < c.x) :
                        c.final_x-=1
                    
                    c.final_y = c.y*3
                    if (tallRows[c.x] < c.y) :
                        c.final_y+=1
                    
                    if c.final_w == c.shrinkWidth:
                        c.final_w = 2 
                    else: c.final_w = 3
                    if c.final_h == c.raiseHeight:
                        c.final_h = 4 
                    else: c.final_h = 3
                
            
            def reassignGroup (oldg,newg) :
                c=[]
                for i in rows*cols :
                    c = cells[i]
                    if (c.group == oldg) :
                        c.group = newg
                    
                
            
            def createTunnels () :
                # declare candidates
                singleDeadEndCells = []
                topSingleDeadEndCells = []
                botSingleDeadEndCells = []
                voidTunnelCells = []
                topVoidTunnelCells = []
                botVoidTunnelCells = []
                edgeTunnelCells = []
                topEdgeTunnelCells = []
                botEdgeTunnelCells = []
                doubleDeadEndCells = []
                numTunnelsCreated = 0
                # prepare candidates
                c=[]
                upDead=[]
                downDead=[]
                for y in rows :
                    c = cells[cols-1+y*cols]
                    if (c.connect[UP]) :
                        continue
                    
                    if (c.y > 1 and c.y < rows-2) :
                        c.isEdgeTunnelCandidate = True
                        edgeTunnelCells.push(c)
                        if (c.y <= 2) :
                            topEdgeTunnelCells.push(c)
                        elif (c.y >= 5) :
                            botEdgeTunnelCells.push(c)
                        
                    
                    upDead = (not c.next[UP] or  c.next[UP].connect[RIGHT])
                    downDead = (not c.next[DOWN] or  c.next[DOWN].connect[RIGHT])
                    if (c.connect[RIGHT]) :
                        if (upDead) :
                            c.isVoidTunnelCandidate = True
                            voidTunnelCells.push(c)
                            if (c.y <= 2) :
                                topVoidTunnelCells.push(c)
                            
                            elif (c.y >= 6) :
                                botVoidTunnelCells.push(c)
                            
                        
                    
                    else :
                        if (c.connect[DOWN]) :
                            continue
                        
                        if (upDead != downDead) :
                            if (not c.raiseHeight and y < rows-1 and not c.next[LEFT].connect[LEFT]) :
                                singleDeadEndCells.push(c)
                                c.isSingleDeadEndCandidate = True
                                if c.singleDeadEndDir == upDead:
                                    c.singleDeadEndDir = UP
                                else:c.singleDeadEndDir = DOWN
                                if upDead == 1 :
                                    offset = 0
                                else: offset = 1
                                    
                                if (c.y <= 1+offset) :
                                    topSingleDeadEndCells.push(c)
                                
                                elif (c.y >= 5+offset) :
                                    botSingleDeadEndCells.push(c)
                                
                            
                        
                        elif (upDead and downDead) :
                            if (y > 0 and y < rows-1) :
                                if (c.next[LEFT].connect[UP] and c.next[LEFT].connect[DOWN]) :
                                    c.isDoubleDeadEndCandidate = True
                                    if (c.y >= 2 and c.y <= 5) :
                                        doubleDeadEndCells.push(c)
                                    
                                
                            
                        
                    
                
                # choose tunnels from candidates
                numTunnelsDesired = math.random()
                if numTunnelsDesired <= 0.45:
                    numTunnelsDesired = 2
                else: numTunnelsDesired = 1
                c=[]
                def selectSingleDeadEnd (c) :
                    c.connect[RIGHT] = True
                    if (c.singleDeadEndDir == UP) :
                        c.topTunnel = True
                    
                    else :
                        c.next[DOWN].topTunnel = True
                    
                
                if (numTunnelsDesired == 1) :
                    if (c == randomElement(voidTunnelCells)) :
                        c.topTunnel = True
                    elif (c == randomElement(singleDeadEndCells)) :
                        selectSingleDeadEnd(c)
                    elif (c == randomElement(edgeTunnelCells)) :
                        c.topTunnel = True
                    else :
                        return False
                    
                
                elif (numTunnelsDesired == 2) :
                    if (c == randomElement(doubleDeadEndCells)) :
                        c.connect[RIGHT] = True
                        c.topTunnel = True
                        c.next[DOWN].topTunnel = True
                    
                    else :
                        numTunnelsCreated = 1
                        if (c == randomElement(topVoidTunnelCells)) :
                            c.topTunnel = True
                        
                        elif (c == randomElement(topSingleDeadEndCells)) :
                            selectSingleDeadEnd(c)
                        
                        elif (c == randomElement(topEdgeTunnelCells)) :
                            c.topTunnel = True
                        
                        else :
                            # could not find a top tunnel opening
                            numTunnelsCreated = 0
                        
                        if (c == randomElement(botVoidTunnelCells)) :
                            c.topTunnel = True
                        
                        elif (c == randomElement(botSingleDeadEndCells)) :
                            selectSingleDeadEnd(c)
                        
                        elif (c == randomElement(botEdgeTunnelCells)) :
                            c.topTunnel = True
                        
                        else :
                            # could not find a bottom tunnel opening
                            if (numTunnelsCreated == 0) :
                                return False
                            
                        
                    
                
                # don't allow a horizontal path to cut straight through a map (through tunnels)
                exit=None
                topy=[]
                for y in rows :
                    c = cells[cols-1+y*cols]
                    if (c.topTunnel) :
                        exit = True
                        topy = c.final_y
                        while (c.next[LEFT]) :
                            c = c.next[LEFT]
                            if (not c.connect[UP] and c.final_y == topy) :
                                continue
                            
                            else :
                                exit = False
                                break
                            
                        
                        if (exit) :
                            return False
                        
                    
                
                # clear unused void tunnels (dead ends)
                len = voidTunnelCells.length
                def replaceGroup (oldg,newg) :
                    c=[]
                    for i in rows*cols :
                        c = cells[i]
                        if (c.group == oldg) :
                            c.group = newg
                        
                    
                
                for i in len:
                    c = voidTunnelCells[i]
                    if (not c.topTunnel) :
                        replaceGroup(c.group, c.next[UP].group)
                        c.connect[UP] = True
                        c.next[UP].connect[DOWN] = True
                    
                
                return True
            
            def joinWalls () :
                # randomly join wall pieces to the boundary to increase difficulty
                c=[]
                # join cells to the top boundary
                for x in cols :
                    c = cells[x]
                    if (not c.connect[LEFT] and not c.connect[RIGHT] and not c.connect[UP] and
                        (not c.connect[DOWN] or  not c.next[DOWN].connect[DOWN])) :
                        # ensure it will not create a dead-end
                        if ((not c.next[LEFT] or  not c.next[LEFT].connect[UP]) and
                            (c.next[RIGHT] and not c.next[RIGHT].connect[UP])) :
                            # prevent connecting very large piece
                            if (not (c.next[DOWN] and c.next[DOWN].connect[RIGHT] and c.next[DOWN].next[RIGHT].connect[RIGHT])) :
                                c.isJoinCandidate = True
                                if (math.random() <= 0.25) :
                                    c.connect[UP] = True
                                
                            
                        
                    
                
                # join cells to the bottom boundary
                for x in cols:
                    c = cells[x+(rows-1)*cols]
                    if (not c.connect[LEFT] and not c.connect[RIGHT] and not c.connect[DOWN] and
                        (not c.connect[UP] or  not c.next[UP].connect[UP])) :
                        # ensure it will not creat a dead-end
                        if ((not c.next[LEFT] or  not c.next[LEFT].connect[DOWN]) and
                            (c.next[RIGHT] and not c.next[RIGHT].connect[DOWN])) :
                            # prevent connecting very large piece
                            if (not (c.next[UP] and c.next[UP].connect[RIGHT] and c.next[UP].next[RIGHT].connect[RIGHT])) :
                                c.isJoinCandidate = True
                                if (math.random() <= 0.25) :
                                    c.connect[DOWN] = True
                                
                            
                        
                    
                
                # join cells to the right boundary
                c2=[]
                for y in rows :
                    c = cells[cols-1+y*cols]
                    if (c.raiseHeight) :
                        continue
                    
                    if (not c.connect[RIGHT] and not c.connect[UP] and not c.connect[DOWN] and
                        not c.next[UP].connect[RIGHT] and not c.next[DOWN].connect[RIGHT]) :
                        if (c.connect[LEFT]) :
                            c2 = c.next[LEFT]
                            if (not c2.connect[UP] and not c2.connect[DOWN] and not c2.connect[LEFT]) :
                                c.isJoinCandidate = True
                                if (math.random() <= 0.5) :
                                    c.connect[RIGHT] = True
                                
                            
                        
                    
                
            
            # try to generate a valid map, and keep count of tries.
            genCount = 0
            while (True) :
                reset()
                gen()
                genCount+=1
                if (not isDesirable()) :
                    continue
                
                setUpScaleCoords()
                joinWalls()
                if (not createTunnels()) :
                    continue
                
                break
            
        
    # Transform the simple cells to a tile array used for creating the map.
    def getTiles (self) :
        tiles = [] # each is a character indicating a wall(|), path(.), or blank(_).
        tileCells = [] # maps each tile to a specific cell of our simple map
        subrows = rows*3+1+3
        subcols = cols*3-1+2
        midcols = subcols-2
        fullcols = (subcols-2)*2
        # getter and setter for tiles (ensures vertical symmetry axis)
        def setTile (x,y,v) :
            if (x<0 or  x>subcols-1 or  y<0 or  y>subrows-1) :
                return
            
            x -= 2
            tiles[midcols+x+y*fullcols] = v
            tiles[midcols-1-x+y*fullcols] = v
        
        def getTile (x,y) :
            if (x<0 or  x>subcols-1 or  y<0 or  y>subrows-1) :
                return None
            
            x -= 2
            return tiles[midcols+x+y*fullcols]
        
        # getter and setter for tile cells
        def setTileCell (x,y,cell) :
            if (x<0 or  x>subcols-1 or  y<0 or  y>subrows-1) :
                return
            
            x -= 2
            tileCells[x+y*subcols] = cell
        
        def getTileCell (x,y) :
            if (x<0 or  x>subcols-1 or  y<0 or  y>subrows-1) :
                return None
            
            x -= 2
            return tileCells[x+y*subcols]
        
        # initialize tiles
        for i in subrows*fullcols:
            tiles.push('_')
        
        for i in subrows*subcols :
            tileCells.push(None)
        
        # set tile cells
        c=[]
        for i in rows*cols:
            c = cells[i]
            for x0 in c.final_w :
                for y0 in c.final_h :
                    setTileCell(c.final_x+x0,c.final_y+1+y0,c)
                
            
        
        # set path tiles
        cl=[]
        cu=[]
        for y in subrows:
            for x in subcols:
                c = getTileCell(x,y) # cell
                cl = getTileCell(x-1,y) # left cell
                cu = getTileCell(x,y-1) # up cell
                if (c) :
                    # inside map
                    if (cl and c.group != cl.group or  # at vertical boundary
                        cu and c.group != cu.group or  # at horizontal boundary
                        not cu and not c.connect[UP]) : # at top boundary
                        setTile(x,y,'.')
                    
                
                else :
                    # outside map
                    if (cl and (not cl.connect[RIGHT] or  getTile(x-1,y) == '.') or  # at right boundary
                        cu and (not cu.connect[DOWN] or  getTile(x,y-1) == '.')) : # at bottom boundary
                        setTile(x,y,'.')
                    
                
                # at corner connecting two paths
                if (getTile(x-1,y) == '.' and getTile(x,y-1) == '.' and getTile(x-1,y-1) == '_') :
                    setTile(x,y,'.')
                
            
        
        # extend tunnels
        y=[]
        for c in cells[cols-1]:
            if (c.topTunnel) :
                y = c.final_y+1
                setTile(subcols-1, y,'.')
                setTile(subcols-2, y,'.')
            
        
        # fill in walls
        for y in subrows :
            for x in subcols :
                # any blank tile that shares a vertex with a path tile should be a wall tile
                if (getTile(x,y) != '.' and (getTile(x-1,y) == '.' or  getTile(x,y-1) == '.' or  getTile(x+1,y) == '.' or  getTile(x,y+1) == '.' or 
                    getTile(x-1,y-1) == '.' or  getTile(x+1,y-1) == '.' or  getTile(x+1,y+1) == '.' or  getTile(x-1,y+1) == '.')) :
                    setTile(x,y,'|')
                
            
        
        # create the ghost door
        setTile(2,12,'-')
        # set energizers
        def getTopEnergizerRange () :
            maxy = subrows/2
            x = subcols-2
            for y in maxy:
                if (getTile(x,y) == '.' and getTile(x,y+1) == '.') :
                    miny = y+1
                    break
                
            
            maxy = math.min(maxy,miny+7)
            for y in miny:
                if (getTile(x-1,y) == '.') :
                    maxy = y-1
                    break
                
            
            return {miny:miny, maxy:maxy}
        
        def getBotEnergizerRange () :
            miny = subrows/2
            x = subcols-2
            for y in subrows :
                if (getTile(x,y) == '.' and getTile(x,y+1) == '.') :
                    maxy = y
                    break
                
            
            miny = math.max(miny,maxy-7)
            for y in miny :
                if (getTile(x-1,y) == '.') :
                    miny = y+1
                    break
                
            
            return {miny:miny, maxy:maxy}
        
        x = subcols-2
        range
        if (range == getTopEnergizerRange()) :
            y = getRandomInt(range.miny, range.maxy)
            setTile(x,y,'o')
        
        if (range == getBotEnergizerRange()) :
            y = getRandomInt(range.miny, range.maxy)
            setTile(x,y,'o')
        
        # erase pellets in the tunnels
        def eraseUntilIntersection (x,y) :
            adj=[]
            while (True) :
                adj = []
                if (getTile(x-1,y) == '.') :
                    adj.push({x:x-1,y:y})
                
                if (getTile(x+1,y) == '.') :
                    adj.push({x:x+1,y:y})
                
                if (getTile(x,y-1) == '.') :
                    adj.push({x:x,y:y-1})
                
                if (getTile(x,y+1) == '.') :
                    adj.push({x:x,y:y+1})
                
                if (adj.length == 1) :
                    setTile(x,y,' ')
                    x = adj[0].x
                    y = adj[0].y
                
                else :
                    break
                
            
        
        x = subcols-1
        for y in subrows:
            if (getTile(x,y) == '.') :
                eraseUntilIntersection(x,y)
            
        
        # erase pellets on starting position
        setTile(1,subrows-8,' ')
        # erase pellets around the ghost house
        for i in 7 :
            # erase pellets from bottom of the ghost house proceeding down until
            # reaching a pellet tile that isn't surround by walls
            # on the left and right
            y = subrows-14
            setTile(i, y, ' ')
            j = 1
            while (getTile(i,y+j) == '.' and
                    getTile(i-1,y+j) == '|' and
                    getTile(i+1,y+j) == '|') :
                setTile(i,y+j,' ')
                j+=1
            
            # erase pellets from top of the ghost house proceeding up until
            # reaching a pellet tile that isn't surround by walls
            # on the left and right
            y = subrows-20
            setTile(i, y, ' ')
            j = 1
            while (getTile(i,y-j) == '.' and
                    getTile(i-1,y-j) == '|' and
                    getTile(i+1,y-j) == '|') :
                setTile(i,y-j,' ')
                j+=1
            
        
        # erase pellets on the side of the ghost house
        for i in 7 :
            # erase pellets from side of the ghost house proceeding right until
            # reaching a pellet tile that isn't surround by walls
            # on the top and bottom.
            x = 6
            y = subrows-14-i
            setTile(x, y, ' ')
            j = 1
            while (getTile(x+j,y) == '.' and
                    getTile(x+j,y-1) == '|' and
                    getTile(x+j,y+1) == '|') :
                setTile(x+j,y,' ')
                j+=1
            
        
        # return a tile string (3 empty lines on top and 2 on bottom)
        print (
            "____________________________" +
            "____________________________" +
            "____________________________" +
            tiles.join("") +
            "____________________________" +
            "____________________________")
    


mastermap = Map(36,28, mastermap.getTiles)

print(mastermap)

