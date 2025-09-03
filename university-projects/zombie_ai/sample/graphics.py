from random import randrange

import pyglet, math
import os

from zombie_ai.sample.vector2d import Vector2D

COLOUR_NAMES = {
	'BLACK':  (000, 000, 000, 255),
	'WHITE':  (255, 255, 255, 255),
	'RED':    (255, 000, 000, 255),
	'GREEN':  (000, 255, 000, 255),
	'BLUE':   (000, 000 ,255, 255),
	'GREY':   (100, 100, 100, 255),
	'PINK':   (255, 175, 175, 255),
	'YELLOW': (255, 255, 000, 255),
	'ORANGE': (255, 175, 000, 255),
	'PURPLE': (200, 000, 175, 200),
	'BROWN':  (125, 125, 100, 255),
	'AQUA':   (100, 230, 255, 255),
	'DARK_GREEN': (000, 100, 000, 255),
	'LIGHT_GREEN':(150, 255, 150, 255),
	'LIGHT_BLUE': (150, 150, 255, 255),
	'LIGHT_GREY': (200, 200, 200, 255),
	'LIGHT_PINK': (255, 230, 230, 255)
}

OBSTACLE_IMAGE = pyglet.image.load(os.path.join("barricade.png"))
FINISH_IMAGE = pyglet.image.load(os.path.join("finish_line.png"))
class ShapeGroup:
	def __init__(self, anchor, batch):
		self._x = anchor.x
		self._y = anchor.y
		self._anchor_x = self._x
		self._anchor_y = self._y
		self._rgba = (255, 255, 255, 255)
		self._visible = True
		self._batch = batch
		self.shapes = []

	def draw(self):
		for shape in self.shapes:
			shape.draw()

	def translate(self, v):
		for shape in self.shapes:
			shape.x += v.x
			shape.y += v.y
		self._anchor_x += v.x
		self._anchor_y += v.y

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self.position = pyglet.math.Vec2(value, self._y)

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self.position = pyglet.math.Vec2(self._x, value)

	@property
	def position(self):
		return pyglet.math.Vec2(self._x, self._y)

	@position.setter
	def position(self, values):
		if type(values) is tuple:
			values = pyglet.math.Vec2(values[0], values[1])
		pos = pyglet.math.Vec2(self.position[0], self.position[1])
		v = values - pos
		self.translate(v)
		self._x = values.x
		self._y = values.y

	@property
	def anchor_x(self):
		return self._anchor_x

	@anchor_x.setter
	def anchor_x(self, value):
		self._anchor_x = value

	@property
	def anchor_y(self):
		return self._anchor_y

	@anchor_y.setter
	def anchor_y(self, value):
		self._anchor_y = value

	@property
	def anchor_position(self):
		return self._anchor_x, self._anchor_y

	@anchor_position.setter
	def anchor_position(self, values):
		if type(values) is tuple:
			values = pyglet.math.Vec2(values[0], values[1])
		self._anchor_x = values.x
		self._anchor_y = values.y

	@property
	def color(self):
		return self._rgba

	@property
	def colour(self):
		return self._rgba

	@colour.setter
	def colour(self, values):
		r, g, b, *a = values

		if a:
			self._rgba = r, g, b, a[0]
		else:
			self._rgba = r, g, b, self._rgba[3]

		for line in self.shapes:
			line.color = self._rgba

	@color.setter
	def color(self, values):
		self.colour = values

	@property
	def opacity(self):
		return self._rgba[3]

	@opacity.setter
	def opacity(self, value):
		self._rgba = (*self._rgba[:3], value)
		for shape in self.shapes:
			shape.color = self._rgba

	@property
	def visible(self):
		return self._visible

	@visible.setter
	def visible(self, value):
		self._visible = value
		for shape in self.shapes:
			shape.visible = value

	@property
	def group(self):
		raise NotImplementedError

	@group.setter
	def group(self, group):
		raise NotImplementedError

	@property
	def batch(self):
		return self._batch

	@batch.setter
	def batch(self, batch):
		if self._batch == batch:
			return

		for line in self.shapes:
			line.batch = batch 

		self._batch = batch
class Obstacle(ShapeGroup):
	def __init__(self, x, y, batch):
		super().__init__(anchor=pyglet.math.Vec2(x,y), batch=batch)
		self.shapes = pyglet.sprite.Sprite(OBSTACLE_IMAGE, x=x, y=y, batch=batch)
		self.shapes.scale = 0.05
		self.pos = Vector2D(x ,y)
		self.shapes.image.anchor_y = 1800
		self.shapes.image.anchor_x = 350
	def is_obstacle(self, point):

		width = self.shapes.width
		height = self.shapes.height
		inside_x = (self.pos.x - width / 2 <= point.x) and (point.x <= self.pos.x + width / 2)
		inside_y = (self.pos.y - height / 2 <= point.y) and (point.y <= self.pos.y + height / 2)

		return inside_x and inside_y
class GoalMaker(ShapeGroup):
	def __init__(self,x,y, batch):
		super().__init__(anchor=pyglet.math.Vec2(x, y), batch=batch)
		self.pos = Vector2D(x,y)
		self.marker = pyglet.sprite.Sprite(FINISH_IMAGE, x=x, y=y, batch=batch)
		self.marker.scale = 0.5
		self.marker.y -= (self.marker.height * self.marker.scale / 2) + 30
		self.marker.x -= (self.marker.width * self.marker.scale / 2) + 45
class SafeSpot(ShapeGroup):
	def __init__(self,x,y, batch,size=60):
		super().__init__(anchor=pyglet.math.Vec2(x, y), batch=batch)
		self.pos = Vector2D(x,y)
		self.size = size
		self.marker = pyglet.shapes.Circle(x, y, self.size/2,color=COLOUR_NAMES["GREEN"], batch=batch)
	def is_safe_spot(self, point ):
		distance = (Vector2D(point.x, point.y) - self.pos).length()
		return distance < self.size / 2

class GameWindow(pyglet.window.Window):
	MIN_UPS = 5
	def __init__(self, **kwargs):
		kwargs['config'] = pyglet.gl.Config(double_buffer=True, sample_buffers=1, samples=8)
		super(GameWindow, self).__init__(**kwargs)
		self.fps_display = pyglet.window.FPSDisplay(self)
		self.cfg = {
			'INFO': False,
			"WINNING": True
		}
		self.batches = {
			"main": pyglet.graphics.Batch(),
			"info": pyglet.graphics.Batch(),
			"winning": pyglet.graphics.Batch()
		}
		self.labels = {
			'mode':	pyglet.text.Label('', x=200, y=self.height-20, color=COLOUR_NAMES['WHITE']),
			'status':	pyglet.text.Label('', x=400, y=self.height-20, color=COLOUR_NAMES['WHITE']) 
		}
		self.add_handlers()
		self.background = pyglet.sprite.Sprite(pyglet.image.load(os.path.join('background.png')))
		self.obstacles = [ Obstacle(200, 200, self.get_batch("main")),
							Obstacle(400, 400, self.get_batch("main")),
							Obstacle(600, 130, self.get_batch("main")),
							Obstacle(20, 550, self.get_batch("main")),
							Obstacle(350, 600, self.get_batch("main"))]
		self.goal_maker = GoalMaker(800,600, self.get_batch("main"))
		self.safe_spot = SafeSpot(50,300,self.get_batch("main"))

	def _update_label(self, label, text='---'):
		if label in self.labels:
			self.labels[label].text = text
		

	def add_handlers(self):
		@self.event
		#didn't test this... whoops
		def on_resize(cx, cy):
			from game import game
			game.world.cx = cx
			game.world.cy = cy

		@self.event
		def on_mouse_press(x, y, button, modifiers):
			from game import game
			game.input_mouse(x, y, button, modifiers)


		@self.event
		def on_key_press(symbol, modifiers):
			if symbol == pyglet.window.key.I:
				self.cfg['INFO'] = not self.cfg['INFO']
			from game import game
			game.input_keyboard(symbol, modifiers)

		@self.event
		def on_draw():
			self.clear()
			self.background.draw()
			for obstacle in self.obstacles:
				obstacle.shapes.draw()
			self.batches["main"].draw()
			if self.cfg['INFO']:
				self.batches["info"].draw()
			self.fps_display.draw()
			for label in self.labels.values():
				label.draw()
			if self.cfg['WINNING']:
				self.batches["winning"].draw()

		
	def get_batch(self, batch_name="main"):
		return self.batches[batch_name]

settings = {
		'width': 900,
		'height': 650,
		'vsync': True,
		'resizable': False,
		'caption': "Zombie Smart Survival",
	}
	
window = GameWindow(**settings)