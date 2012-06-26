PORTAL_WIDTH = 20
PORTAL_HEIGHT = 16

class TTYView(object):
	def __init__(self):
		self.level = None
		self.tiles = None
		self.objects = None
		self.player = None
		self.portal_width = PORTAL_WIDTH
		self.portal_height = PORTAL_HEIGHT
		self.keys = {
				'h': 'player_left',
				'j': 'player_down',
				'k': 'player_up',
				'l': 'player_right',
				'y': 'player_left_up',
				'u': 'player_right_up',
				'b': 'player_left_down',
				'n': 'player_right_down',
		}

	@property
	def portal_left(self):
		return self.player.x - (PORTAL_WIDTH / 2)

	@property
	def portal_top(self):
		return self.player.y - (PORTAL_HEIGHT / 2)

	def setLevel(self, level):
		self.level = level
	
	def setTiles(self, tiles):
		self.tiles = tiles
	
	def setObjects(self, objects):
		self.objects = objects
		self.player = objects[0]
	
	def draw(self):
		min_x = self.portal_left
		min_y = self.portal_top

		text_lines = []

		# Add the map
		for y in range(PORTAL_HEIGHT):
			map_y = min_y + y
			text_line = []
			for x in range(PORTAL_WIDTH):
				map_x = min_x + x
				try:
					square = self.level[map_y][map_x]
					if square.visible == square.VISIBILITY_BRIGHT:
						textchar = square.tiles[0].textchar
					else:
						textchar = ' '
				except IndexError:
					textchar = ' '
				text_line.append(textchar)
			text_lines.append(text_line)

		# Add the PC and NPCs. This is hella optimisable by using a better data structure
		# for the objects (set of buckets would be pretty reasonable)
		for gameobject in self.objects:
			if gameobject.x >= min_x and gameobject.x < (min_x + PORTAL_WIDTH) \
					and gameobject.y >= min_y and gameobject.y < (min_y + PORTAL_HEIGHT):
				text_lines[gameobject.y - min_y][gameobject.x - min_x] = gameobject.textchar

		print '\n'.join([''.join(text_line) for text_line in text_lines])
	
	def get_action(self):
		pressed = raw_input()
		if pressed:
			key = pressed[0]
			return self.keys.get(key, 'invalid')
		else:
			return 'invalid'

	def report_invalid(self):
		print "Input invalid."


