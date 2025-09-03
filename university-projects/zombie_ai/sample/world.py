'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from matrix33 import Matrix33
import pyglet
from graphics import COLOUR_NAMES, window
from projectile import Weapon
from astar import a_star

class World(object):

	def __init__(self, cx, cy):
		self.cx = cx
		self.cy = cy
		self.grid = self.create_grid()
		self.hunter = None
		self.targets = []
		self.soldier = []
		self.projectiles = []
		self.game_state = None
		self.paused = True
		self.show_info = True
	def create_grid(self):
		grid_nodes = {}
		for x in range(self.cx):
			for y in range (self.cy):
				position = Vector2D(x, y)
				grid_nodes[(x,y)] = {
					"walkable": True,
					"g_score": float("inf"),
					"came_from": None,
					"safe_spot": False
				}
				if window.safe_spot.is_safe_spot(position):
					grid_nodes[(x,y)]["safe_spot"] = True
		for obstacle in window.obstacles:
			for x in range(self.cx):
				for y in range(self.cy):
					position = Vector2D(x,y)
					if obstacle.is_obstacle(position):
						grid_nodes[(x,y)]["walkable"] = False


		return grid_nodes

	def get_path(self,start, goal):
		return a_star(start, goal, self.grid)



	def is_safe(self, pos):

		if pos not in self.grid:
			return False

		if not self.grid[pos]["walkable"]:
			return False

		pos_vector = Vector2D(pos[0], pos[1])

		for zombie in self.targets:
			if (zombie.pos - pos_vector).length() < 150:
				return False

		return True

	def is_dangerous(self, pos):
		if pos not in self.grid:
			return True

		if not self.grid[pos]["walkable"]:
			return True
		pos_vector = Vector2D(pos[0], pos[1])

		nearby_threats = sum(1 for zombie in self.targets if (zombie.pos - pos_vector).length() < 200)

		if nearby_threats > 2:
			return True

		return False
	def update(self, delta):
		if not self.paused:
			max_projectiles = 20
			while len(self.projectiles) > max_projectiles:
				self.projectiles.pop(0)
			for soldier in self.soldier:
				soldier.update(delta)
			for target in self.targets:
				target.update(delta)

			for projectile in self.projectiles[:]:
				projectile.update(delta)
				if projectile.check_collision():
					if projectile in self.projectiles:
						self.projectiles.remove(projectile)

	def create_explosion(self, pos, radius, damage):
		print(f"🔥 Explosion at {pos} with radius {radius}")

		for object in self.soldier:
			distance = (object.pos - pos).length()
			if distance <= radius:
				object.take_damage(damage)
		for object in self.targets:
			distance = (object.pos - pos).length()
			if distance <= radius:
				object.take_damage(damage)
		for object in self.projectiles:
			distance = (object.pos - pos).length()
			if distance <= radius:
				self.projectiles.remove(object)

	def remove_agent(self, agent):
		if agent in self.soldier:
			self.soldier.remove(agent)
		elif agent in self.targets:
			self.targets.remove(agent)



	def wrap_around(self, pos):
		''' Treat world as a toroidal space. Updates parameter object pos '''
		max_x, max_y = self.cx, self.cy
		if pos.x > max_x:
			pos.x = pos.x - max_x
		elif pos.x < 0:
			pos.x = max_x - pos.x
		if pos.y > max_y:
			pos.y = pos.y - max_y
		elif pos.y < 0:
			pos.y = max_y - pos.y

	def transform_point(self,point,pos, forward, side):
		world_pt = point.copy()

		mat = Matrix33()
		mat.rotate_by_vectors_update(forward,side)
		mat.translate_update(pos.x,pos.y)
		mat.transform_vector2d(world_pt)
		return world_pt


	def transform_points(self, points, pos, forward, side, scale):
		''' Transform the given list of points, using the provided position,
			direction and scale, to object world space. '''
		# make a copy of original points (so we don't trash them)
		wld_pts = [pt.copy() for pt in points]
		# create a transformation matrix to perform the operations
		mat = Matrix33()
		# scale,
		mat.scale_update(scale.x, scale.y)
		# rotate
		mat.rotate_by_vectors_update(forward, side)
		# and translate
		mat.translate_update(pos.x, pos.y)
		# now transform all the points (vertices)
		mat.transform_vector2d_list(wld_pts)
		# done
		return wld_pts

	def input_mouse(self, x, y, button, modifiers):
		if button == 1:  # left
			self.target.x = x
			self.target.y = y

	def input_keyboard(self, symbol, modifiers):
		if symbol == pyglet.window.key.P:
			self.paused = not self.paused

		elif symbol == pyglet.window.key.R:
			for attacker in self.soldier:
				attacker.switch_weapon(Weapon("rifle"))
		elif symbol == pyglet.window.key.G:
			for attacker in self.soldier:
				attacker.switch_weapon(Weapon("handgrenade"))
		elif symbol == pyglet.window.key.H:
			for attacker in self.soldier:
				attacker.switch_weapon(Weapon("handgun"))
		elif symbol == pyglet.window.key.K:
			for attacker in self.soldier:
				attacker.switch_weapon(Weapon("rocket"))