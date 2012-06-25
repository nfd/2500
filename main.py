import leveldata
import tiledata
import gamemap
import ttyview
import player

class Game(object):
	def __init__(self):
		self.tiles = None
		self.level = None
		self.player = player.Player(30, 10)
		self.objects = [self.player]
		self.view = ttyview.TTYView()
	
	def playLevel(self):
		self._loadLevel()
		self.view.setTiles(self.tiles)
		self.view.setLevel(self.level)
		self.view.setObjects(self.objects)
		self._mainLoop()
	
	def _loadLevel(self):
		if self.tiles is None:
			self._loadTiles()

		self.level = gamemap.Level('Overground', self.tiles)

		mapMode = False

		for line in leveldata.LEVEL_OVERGROUND.split('\n'):
			if line.strip():
				if not mapMode:
					if line.startswith('>map'):
						mapMode = True
					else:
						self.level.loadCmd(line)
				else:
					self.level.loadMapLine(line)
	
	def _loadTiles(self):
		self.tiles = gamemap.Tiles()
		for line in tiledata.TILES.split('\n'):
			line = line.strip()
			if line and line.startswith('>tile'):
				self.tiles.load(line)
	
	def _mainLoop(self):
		while True:
			# FIXME: Should only updateVisibles when player moves?
			# Possibly other things too, such as lighting lamps...
			self.level.updateVisibles(self.player.x, self.player.y,
					self.view.portal_left(), self.view.portal_top(),
					self.view.portal_width, self.view.portal_height)

			# Redraw
			self.view.draw()

			# Wait for the next command, which is always executed by the
			# player object.
			action = self.view.get_action()
			if action == 'invalid':
				self.view.report_invalid()
			else:
				self.player.act(action)
	
if __name__ == '__main__':
	game = Game()
	game.playLevel()

