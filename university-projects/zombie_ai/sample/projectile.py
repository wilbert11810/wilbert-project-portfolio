import pyglet
from graphics import window

WEAPON_STATS = {
	"rifle": {"speed": 50, "accuracy": 4.5, "damage": 25},
	"handgrenade": {"speed": 15, "accuracy": 0.5, "damage": 80},
	"rocket": {"speed": 15, "accuracy": 6.0, "damage": 100},
	"handgun": {"speed": 60, "accuracy": 2.0, "damage": 20}
}

class Projectile:
	def __init__(self, attacker, target, direction, world):
		self.world = world
		self.attacker = attacker
		self.target = target
		self.pos = attacker.pos.copy()
		self.speed = attacker.weapon.speed * 10.0
		self.time_needed = (target.pos - attacker.pos).length() / attacker.weapon.speed
		self.vel = direction * self.speed
		self.enemy = target.pos.copy()
		self.hit_threshold = 10
		self.max_speed = self.speed * 2.0
		self.lifetime = 4.0
		self.lifetime = (target.pos - attacker.pos).length() / attacker.weapon.speed
		if self.attacker.weapon.mode == "rifle":
			self.shape = pyglet.shapes.Circle(self.pos.x, self.pos.y,
											  5,color=(255,255,0), batch=window.get_batch("main"))
		elif self.attacker.weapon.mode == "handgun":
			self.shape = pyglet.shapes.Circle(self.pos.x, self.pos.y,
											  5, color=(255, 87, 51), batch=window.get_batch("main"))

	def check_collision(self):

		if (self.pos - self.enemy).length() < self.hit_threshold:
			return True
		return False

	def update(self, delta):
		self.lifetime -= delta
		if self.lifetime <= 0:
			self.world.projectiles.remove(self)
			return
		to_target = (self.enemy - self.pos).normalise()
		desired_vel = to_target * self.speed

		steering_force = (desired_vel - self.vel) * delta
		self.vel += steering_force
		if self.vel.length() > self.max_speed:
			self.vel = self.vel.normalise() * self.max_speed

		self.pos += self.vel * delta
		self.world.wrap_around(self.pos)
		self.shape.x = self.pos.x
		self.shape.y = self.pos.y

		if self.check_collision():
			if self.target and self.target.health > 0:
				self.target.take_damage(self.attacker.weapon.damage)

		if (self.enemy - self.pos).length() < 35:
			self.world.projectiles.remove(self)
			return


class HandGrenade(Projectile):
	def __init__(self,attacker, target, direction, world):
		super().__init__(attacker, target, direction, world)
		self.detonation_timer = 3.0
		self.shape = pyglet.shapes.Circle(self.pos.x, self.pos.y,
											  5, color=(255, 50, 0), batch=window.get_batch("main"))

	def update(self, delta):
		self.detonation_timer -= delta
		if self.detonation_timer <= 0:
			self.explode()
			return False
		self.pos += self.vel * delta
		self.world.wrap_around(self.pos)
		self.shape.x = self.pos.x
		self.shape.y = self.pos.y

	def explode(self):
		print("💥 Grenade exploded!")
		self.world.create_explosion(self.pos, radius = 50, damage=self.attacker.weapon.damage)


class RocketProjectile(Projectile):
	def __init__(self,attacker, target, direction, world):
		super().__init__(attacker, target, direction, world)
		self.homing_strength = 5.0
		self.living_target = target
		self.lifetime = 8.0

		self.shape = pyglet.shapes.Circle(self.pos.x, self.pos.y,
										  5,color=(255,100,0), batch=window.get_batch("main"))


	def update(self, delta):
		self.lifetime -= delta
		if self.lifetime <= 0:
			self.world.projectiles.remove(self)
			return False
		elif self.lifetime <= 1.5:
			self.speed *= 1.5
		to_target = (self.living_target.pos - self.pos).normalise()
		desired_vel = to_target * self.speed

		steering_force = (desired_vel - self.vel) * self.homing_strength
		self.vel += steering_force * delta
		if self.vel.length() > self.max_speed:
			self.vel = self.vel.normalise() * self.max_speed
		self.pos += self.vel * delta

		self.world.wrap_around(self.pos)
		self.shape.x = self.pos.x
		self.shape.y = self.pos.y
		if self.check_collision():
			if self.living_target:
				self.living_target.take_damage(self.attacker.weapon.damage)
			return True
		return False



class Weapon:
	def __init__(self, mode):
		self.mode = mode
		self.speed = WEAPON_STATS[mode]["speed"]
		self.accuracy = WEAPON_STATS[mode]["accuracy"]
		self.damage = WEAPON_STATS[mode]["damage"]

	def switch_weapon(self, new_mode):
		if new_mode in WEAPON_STATS:
			self.mode = new_mode
			self.speed = WEAPON_STATS[new_mode]["speed"]
			self.accuracy = WEAPON_STATS[new_mode]["accuracy"]
			self.damage = WEAPON_STATS[new_mode]["damage"]
