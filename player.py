#Player actions
#player_left, player_right, _up, _down, _left_up, _right_up, _left_down, _right_down

class GameObject(object):
	def __init__(self):
		self.textchar = '?'

class Player(GameObject):
	def __init__(self, x, y):
		GameObject.__init__(self)

		self.textchar = '@'

		# Player X and Y grid position.
		self.x = x
		self.y = y
	
	def act(self, action):
		getattr(self, 'action_' + action)()
	
	def action_player_left(self):
		self.x -= 1
	
	def action_player_right(self):
		self.x += 1
	
	def action_player_up(self):
		self.y -= 1
	
	def action_player_down(self):
		self.y += 1
	
	def action_player_left_up(self):
		self.x -= 1
		self.y -= 1
	
	def action_player_left_down(self):
		self.x -= 1
		self.y += 1
	
	def action_player_right_up(self):
		self.x += 1
		self.y -= 1

	def action_player_right_down(self):
		self.x += 1
		self.y += 1
	

