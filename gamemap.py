from bresenham import bresenham

class LoadError(Exception):
	pass

def sanityCheck(cond, data, msg):
	if not cond:
		raise LoadError(msg)

lameRNGPrev = 0
lameRNGInc = 27
def lameRandomPercentage():
	# Generate a very predictable and repetitive pseudorandom number 
	# between 0 and 99. This is for assigning alternate graphical tiles
	# from the map and thus must be predictable.
	global lameRNGPrev
	lameRNGPrev += lameRNGInc
	lameRNGPrev %= 100
	return lameRNGPrev

class Tile(object):
	"""
	A Tile represents a terrain object (grass, tree, etc).
	One or more tiles occupy a map square (see Square object, below).
	"""
	SUPPORTED_ATTRIBUTES = ['transp', 'walk', 'door']

	def __init__(self):
		self.name = None
		self.attributes = {} # Maps attr to True -- +attr if present, -attr if not present.
		self.textchar = '?' # The character used to display the tile on text-based outputs
	
	def checkattr(self, attr):
		return attr in self.attributes

	def load(self, tileinfo):
		sanityCheck(tileinfo.startswith('>tile'), tileinfo, 'expected >tile')
		tilecmd, name, tileextra = tileinfo.split(' ', 2)
		self.name = name

		for word in tileextra.split(' '):
			if not word:
				continue

			if word.startswith('+'):
				self.attrAdd(word[1:])
			elif word.startswith('-'):
				self.attrDel(word[1:])
			elif word.startswith('textchar='):
				word = word[len('textchar='):]
				if word:
					sanityCheck(len(word) == 1, word, "Only one-char textchars supported")
					self.textchar = word
				else:
					self.textchar = " "
			else:
				raise LoadError("Unrecognised tile word")
	
	def attrAdd(self, attr):
		self.attributes[attr] = True
	
	def attrDel(self, attr):
		if attr in self.attributes:
			del self.attributes[attr]

class Square(object):
	"""
	A Square represents a map square.
	It can have one or more stacked map Tiles as well as Characters.
	"""
	VISIBILITY_INVISIBLE = 0
	VISIBILITY_REMEMBERED = 1
	VISIBILITY_BRIGHT = 2

	def __init__(self, tiles):
		# Visibility is one of _INVISIBLE, _REMEMBERED, or _BRIGHT. See updateVisible 
		# for more information.
		self.visible = self.VISIBILITY_INVISIBLE

		# Tiles is the list of tiles shown on this square. Order is important: tiles
		# are drawn from left to right.
		self.tiles = tiles

		# Brightness is a float from 0.0 (black) to 1.0 (maximally bright).
		self.brightness = 1.0
	
	def setVisible(self, isVisible):
		if isVisible:
			self.visible = self.VISIBILITY_BRIGHT
		else:
			if self.visible == self.VISIBILITY_BRIGHT:
				self.visible = self.VISIBILITY_REMEMBERED
	
	def checkattr(self, attr):
		return self.tiles[0].checkattr(attr)

class Tiles(object):
	""" A collection of all supported tiles """
	def __init__(self):
		self._tiles = {}
	
	def load(self, tileinfo):
		tileinfo += ' ' # make parsing easier by ensuring we always have at least two spaces
		sanityCheck(tileinfo.startswith('>tile'), tileinfo, 'expected >tile')
		tilecmd, name, extradata = tileinfo.split(' ', 2)
		sanityCheck(name not in self._tiles, name, 'Tile already exists')

		tile = Tile()
		tile.load(tileinfo)
		self._tiles[name] = tile
	
	def __getitem__(self, key):
		return self._tiles[key]

class Level(object):
	def __init__(self, name, tiles):
		self.name = name
		self.tiles = tiles
		self.themap = []
		self.cmds = {'assign': self.loadCmd_assign}
		self.assigns = {}
	
	def updateVisibles(self, player_x, player_y, left, top, width, height):
		for y in range(height):
			for x in range(width):
				self.updateVisible(player_x, player_y, left + x, top + y)

	def updateVisible(self, player_x, player_y, square_x, square_y):
		"""
		Tiles have three states: invisible, remembered, and bright.
		  Invisible tiles appear as black.
		  Remembered tiles appear as a slightly-darkened image.
		  Lit tiles appear normal, but are darkened proportionately to their brightness.

		Transitions:
		  Invisible -> bright: if visibility criteria are met.
		  Remembered -> bright: if visibility criteria are met.
		  Bright -> remembered: if visibility criteria are not met.
		  No other transitions are possible.

		Visibility: A tile is visible if:
		  It is within range of the player's light, and
		  The player view-casting algorithm (see below) says so.

		Player view-casting:
		  For each tile, calculate the Bresenham line to the player. Walk this line, by
		  examining every tile between the line and the player, not including the target
		  tile but including the tile the player is standing on.

		  If the line intersects any opaque tiles, the target tile is not viewable.

		  A simple optimisation would be to start with the tiles closest to the player and
		  skip view casting for portions of the display if a tile is opaque. For example,
		  the player is surrounded by 8 tiles; if one tile is opaque then (360 / 8) = 45
		  degrees of visual field are obscured.
		"""
		try:
			targetSquare = self[square_y][square_x]
		except IndexError:
			return

		#print "do bres", player_x, player_y, square_x, square_y
		for bres_x, bres_y in bresenham(player_x, player_y, square_x, square_y):
			if (bres_x == player_x and bres_y == player_y) or (bres_x == square_x and bres_y == square_y):
				pass
			else:
				try:
					square = self[bres_y][bres_x]
				except IndexError:
					continue

				if square.checkattr('transp') is False:
					# Blocked!
					targetSquare.setVisible(False)
					break
		else:
			targetSquare.setVisible(True)

		# Calculate the Bresenham line from (player_x, player_y) to (x, y).

	def __getitem__(self, idx):
		return self.themap[idx]

	def loadCmd(self, cmd):
		cmd = cmd[1:]
		exec cmd in self.cmds
	
	def loadCmd_assign(self, mapChar, probabilities):
		# Make the probabilities cumulative
		mungedProbs = []
		probabilities = probabilities[:]
		prevTotal = 0
		while probabilities:
			prob = probabilities.pop(0)
			name = probabilities.pop(0)
			mungedProbs.append( (prevTotal, prevTotal + prob, name) )
			prevTotal += prob

		self.assigns[mapChar] = mungedProbs

	def loadMapLine(self, line):
		mapline = []
		for mapChar in line:
			# Assign a random tile from the probabilities
			tileName = None
			r = lameRandomPercentage()
			for probLow, probHigh, tileName in self.assigns[mapChar]:
				if probLow <= r and probHigh > r:
					break
			else:
				raise LoadError("No probability")

			tile = self.tiles[tileName]
			tiles = [tile] # Feature to add: support multiple tiles

			square = Square(tiles)
			mapline.append(square)

		self.themap.append(mapline)

