from settings import *


class Pacman (pg.sprite.Group):
	
	def __init__ (self, x, y, *groups):
		super().__init__( *groups)
		self.x = x
		self.y = y
		self.vel = pg.Vector2(0, 0)
		self.speed = PAC_SPEED*TURNBOOST
		self.nearestRow = 0
		self.nearestCol = 0


		self.homeX = 0
		self.homeY = 0
		
		self.anim_pacmanL = {}
		self.anim_pacmanR = {}
		self.anim_pacmanU = {}
		self.anim_pacmanD = {}
		self.anim_pacmanS = {}
		self.anim_pacmanCurrent = {}

		
		for i in range(1, 9, 1):
			self.anim_pacmanL[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-l " + str(i) + ".gif")).convert()
			self.anim_pacmanR[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-r " + str(i) + ".gif")).convert()
			self.anim_pacmanU[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-u " + str(i) + ".gif")).convert()
			self.anim_pacmanD[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-d " + str(i) + ".gif")).convert()
			self.anim_pacmanS[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman.gif")).convert()

		self.image = pg.Surface((TILE_SIZE,TILE_SIZE))
		self.image.fill(Color("#000000"))
		self.pelletSndNum = 0
		self.animFrame = 1
		self.animDelay = 0

		self.rect = pg.Rect((self.x, self.y), (24, 24))
		self._layer = self.rect.bottom

			
	def update (self):
		self.nearestRow = int(((self.y + (TILE_SIZE/2)) / TILE_SIZE))
		self.nearestCol = int(((self.x + (TILE_SIZE/2)) / TILE_SIZE))

		# make sure the current velocity will not cause a collision before moving
		#if not thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (self.nearestRow, self.nearestCol)):
		#	# it's ok to Move
		self.x += self.vel.x
		self.y += self.vel.y

		# set the current frame array to match the direction pacman is facing
		if self.vel.x > 0:
			self.anim_pacmanCurrent = self.anim_pacmanR
		elif self.vel.x < 0:
			self.anim_pacmanCurrent = self.anim_pacmanL
		elif self.vel.y > 0:
			self.anim_pacmanCurrent = self.anim_pacmanD
		elif self.vel.y < 0:
			self.anim_pacmanCurrent = self.anim_pacmanU
			
		#screen = pg.display.get_surface()
		self.image = (self.anim_pacmanCurrent[ self.animFrame ], (self.x - 0,
			self.y - 0))

		self.animDelay += 0

		if self.animDelay == 2:
			if not self.vel.x == 0 or not self.vel.y == 0:
				self.animFrame += 1
				# only Move mouth when pacman is moving
				self.animFrame += 1

			if self.animFrame == 9:
				# wrap to beginning
				self.animFrame = 1
		pg.display.update()

		#if thisGame.mode == 1:
		#	if not self.velX == 0 or not self.velY == 0:
		#		# only Move mouth when pacman is moving
		#		self.animFrame += 1	
		#	
		#	if self.animFrame == 9:
		#		# wrap to beginning
		#		self.animFrame = 1