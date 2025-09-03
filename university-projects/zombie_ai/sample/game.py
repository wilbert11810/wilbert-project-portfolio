game = None

from enum import Enum
import pyglet
from world import World
from graphics import window
from agent import SoldierAgent, Target # Agent with seek, arrive, flee and pursuit
from projectile import Weapon

class Game():
	def __init__(self):
		self.world = World(window.size[0], window.size[1])
		self.world.soldier.append(SoldierAgent(self.world, Weapon("rifle")))
		for _ in range(5):
			self.world.targets.append(Target(self.world))
		self.world.paused = False

	def input_mouse(self, x, y, button, modifiers):
		self.world.input_mouse(x, y, button, modifiers)

	def input_keyboard(self, symbol, modifiers):
		if symbol == pyglet.window.key.A:
			self.world.targets.append(Target(self.world))
		self.world.input_keyboard(symbol, modifiers)

	def update(self, delta):
		self.world.update(delta)