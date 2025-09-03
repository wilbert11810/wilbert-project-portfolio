'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by
	Clinton Woodward <cwoodward@swin.edu.au>
	James Bonner <jbonner@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

import pyglet
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window
from math import sin, cos, radians, sqrt
from random import random, randrange, uniform
from path import Path
from projectile import Projectile,RocketProjectile,HandGrenade
import time
from behaivoural import Cohesion, Separation, Alignment
import os

WEAPON_STATS = {
	"rifle": {"speed": 50, "accuracy": 4.5},
	"handgrenade": {"speed": 15, "accuracy": 0.5},
	"rocket": {"speed": 15, "accuracy": 6.0},
	"handgun": {"speed": 60, "accuracy": 2.0}
}
ZOMBIE_IMAGE = pyglet.image.load(os.path.join("Idle.png"))
SPRITE_SHEET = pyglet.image.load(os.path.join("Walk.png"))
frame_width = 64
frame_height = 64
PLAYER_FRAME = []
for i in range(8):
	PLAYER_FRAME.append(SPRITE_SHEET.get_region(i * frame_width, 0, frame_width, frame_height))
PLAYER_ANIMATION = pyglet.image.Animation.from_image_sequence(PLAYER_FRAME, duration=0.1, loop=True)

class Agent(object):

	def __init__(self, world=None,scale=30.0, mass=1.0, mode='follow_path'):

		self.world = world
		self.mode = mode
		dir = radians(random()*360)
		self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
		self.vel = Vector2D()
		self.heading = Vector2D(sin(dir), cos(dir))
		self.side = self.heading.perp()
		self.scale = Vector2D(scale, scale)
		self.force = Vector2D()
		self.accel = Vector2D()
		self.mass = mass
		self.waypoint_threshold = 10
		self.wander_target = Vector2D(1, 0)
		self.wander_dist = 1.0 * scale
		self.wander_radius = 1.0 * scale
		self.wander_jitter = 10.0 * scale
		self.bRadius = scale
		self.max_speed = 20.0 * scale
		self.max_force = 1200.0
		self.health = 200

	def take_damage(self, amount):
		self.health -= amount
		if self.health <= 0:
			self.execute()

	def execute(self):
		if self.world:
			self.world.remove_agent(self)

	def update(self, delta):
		force = self.force
		force.truncate(self.max_force)
		self.accel = force / self.mass
		self.vel += self.accel * delta
		self.vel.truncate(self.max_speed)
		self.pos += self.vel * delta
		if self.vel.lengthSq() > 0.00000001:
			self.heading = self.vel.get_normalised()
			self.side = self.heading.perp()
		self.world.wrap_around(self.pos)


	def seek(self, target_pos):
		future_offset = (self.vel * 0.5)
		future_target = target_pos + future_offset
		desired_vel = (future_target - self.pos).normalise() * self.max_speed
		return (desired_vel - self.vel)

	def flee(self, hunter_pos):
		panic_distance = 100
		if (self.pos - hunter_pos).length() > panic_distance:
			return Vector2D()

		desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
		return (desired_vel - self.vel)


	def wander(self, delta):
		wander_target = self.wander_target
		jitter = self.wander_jitter * delta
		wander_target += Vector2D(uniform(-1, 1) * jitter, uniform(-1, 1) * jitter)
		wander_target.normalise()
		wander_target *= self.wander_radius
		wander_dist_vector = Vector2D(self.wander_dist, 0)
		target = wander_target + Vector2D(self.wander_dist, 0)
		world_target = self.world.transform_point(target, self.pos, self.heading, self.side)
		return self.seek(world_target)

class Target(Agent):
	def __init__(self, world):
		super().__init__(world)
		self.vehicle = pyglet.sprite.Sprite(ZOMBIE_IMAGE, x=self.pos.x , y=self.pos.y  , batch=window.get_batch("main"))
		self.vehicle.scale = 0.2
		self.vehicle.image.anchor_y = 150
		self.vehicle.image.anchor_x = 120
		self.state = "patrol"
		self.max_speed = 200
		self.current_path = None
		self.attack_range = 80
		self.attack_damage = 20
		self.attack_cooldown = 1
		self.attack_timer = 0
		self.BRadius = 50
		self.waypoints = self.generate_patrol_points(count=3)
		self.current_index = 0
		self.cohesion = Cohesion(self)
		self.alignment = Alignment(self)
		self.separation = Separation(self)
		self.weights = {
			"alignment": 1.0,
			"cohesion": 0.5,
			"separation": 2.0
		}

	def generate_patrol_points(self, count=3, min_distance=200):
		patrol_points = []
		while len(patrol_points) < count:
			x = randrange(50, self.world.cx - 50)
			y = randrange(50, self.world.cy - 50)
			new_point = Vector2D(x, y)

			if not self.world.grid[(int(x), int(y))]["walkable"] or self.world.grid[(int(x), int(y))]["safe_spot"]:
				continue

			if all((new_point - existing_point).length() > min_distance for existing_point in patrol_points):
				patrol_points.append(new_point)

		return patrol_points

	def is_player_visible(self, player):
		direction_to_player = (player.pos - self.pos).normalise()
		dot_product = self.heading.dot(direction_to_player)
		distance = (player.pos - self.pos).length()

		if dot_product <= 0.7 or distance > 150:
			return False

		for step in range(0, int(distance), 10):
			check_pos = self.pos + direction_to_player * step
			if check_pos.x > 899 or check_pos.y > 649:
				return False
			check_tuple = (int(check_pos.x), int(check_pos.y))
			if not self.world.grid[check_tuple]["walkable"] or self.world.grid[check_tuple]["safe_spot"]:
				return False

		return True

	def TagNeighbours(self, bots, radius):
		for bot in bots:
			bot.tagged = False
			to = self.pos - bot.pos

			gap = radius + bot.BRadius
			if to.lengthSq() < gap**2:
				bot.tagged = True

	def find_nearest_open_point(self, x, y):
		search_radius = 10
		vision_angles = [-45, -30, -15, 0, 15, 30, 45]

		for offset in range(0, 100, search_radius):
			for angle in vision_angles:
				direction = Vector2D(cos(radians(angle)), sin(radians(angle)))
				adjusted_x = int(x + direction.x * offset)
				adjusted_y = int(y + direction.y * offset)
				adjusted_tuple = (adjusted_x, adjusted_y)

				if adjusted_tuple not in self.world.grid:
					return x, y

				if self.world.grid[adjusted_tuple]["walkable"] or not self.world.grid[(int(x), int(y))]["safe_spot"]:
					return adjusted_x, adjusted_y

		return x, y

	def is_path_clear(self, start_x, start_y, end_x, end_y, step_size=10):
		direction = Vector2D(end_x - start_x, end_y - start_y).normalise()
		distance = sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)

		for step in range(0, int(distance), step_size):
			check_x = int(start_x + direction.x * step)
			check_y = int(start_y + direction.y * step)
			check_tuple = (check_x, check_y)

			if check_tuple not in self.world.grid:
				return False

			if not self.world.grid[check_tuple]["walkable"] or self.world.grid[check_tuple]["safe_spot"]:
				return False

		return True

	def draw_vision_cone(self):
		left_angle = self.heading.copy().rotate(-45)
		right_angle = self.heading.copy().rotate(45)

		left_x = self.pos.x + (left_angle.x * 100)
		left_y = self.pos.y + (left_angle.y * 100)
		right_x = self.pos.x + (right_angle.x * 100)
		right_y = self.pos.y + (right_angle.y * 100)

		if not self.is_path_clear(self.pos.x, self.pos.y, left_x, left_y):
			left_x, left_y = self.find_nearest_open_point(left_x, left_y)
		if not self.is_path_clear(self.pos.x, self.pos.y, right_x, right_y):
			right_x, right_y = self.find_nearest_open_point(right_x, right_y)

		self.vision_cone = pyglet.shapes.Polygon(
			(self.pos.x, self.pos.y),
			(left_x, left_y),
			(right_x, right_y),
			color=(255, 255, 0, 100), batch=window.get_batch("main")
		)

	def rotate_towards(self, target_pos, max_turn_speed):
		desired_direction = (target_pos - self.pos).normalise()
		angle_diff = self.heading.angle_between(desired_direction)

		rotation_step = min(abs(angle_diff), max_turn_speed) * (1 if angle_diff > 0 else -1)
		self.heading.rotate(rotation_step)
	def handle_state_transitions(self):
		nearest_enemy = min(self.world.soldier, key=lambda attacker: (self.pos - attacker.pos).length())

		if self.is_player_visible(nearest_enemy) and self.state == "patrol":
			self.current_path = self.world.get_path(self.pos, nearest_enemy.pos)
			if self.current_path:
				for zombie in self.world.targets:
					zombie.state = "chase"
					zombie.current_path = self.current_path.copy()
			return
		elif self.state == "chase" and (self.pos - nearest_enemy.pos).length() < self.attack_range:

			self.state = "attack"
			print(f"Changing to {self.state} state")
			return
		else:
			self.state = "patrol"
			self.current_path = None
			self.max_speed = 100
			return

	def attack(self, target):
		target.health -= self.attack_damage
		print(f"Remaining Player Health: {target.health}")
		if target.health <= 0:
			target.draw_game_over_message()


	def handle_attack_behavior(self, delta):
		nearest_enemy = min(self.world.soldier, key=lambda attacker: (self.pos - attacker.pos).length())

		self.vel = Vector2D(0, 0)

		if self.attack_timer <= 0:
			self.attack(nearest_enemy)
			self.attack_timer = self.attack_cooldown

		self.attack_timer -= delta

		if (self.pos - nearest_enemy.pos).length() > self.attack_range:
			self.state = "chase"

	def handle_chase_behavior(self, delta):
		self.max_speed = 300

		if self.current_path and len(self.current_path) > 0:
			next_waypoint = Vector2D(self.current_path[0][0], self.current_path[0][1])

			if (self.pos - next_waypoint).length() < 100.0:
				self.current_path.pop(0)
				if self.current_path:
					next_waypoint = Vector2D(self.current_path[0][0], self.current_path[0][1])

			next_pos_tuple = (int(next_waypoint.x), int(next_waypoint.y))

			if next_pos_tuple in self.world.grid and not self.world.grid[next_pos_tuple]["walkable"]:
				self.current_path = self.world.get_path(self.pos, next_waypoint)

			self.force = self.seek(next_waypoint)
			group = [bot for bot in self.world.targets if bot.tagged]
			self.alignment_force = self.alignment.compute(group) * self.weights["alignment"]
			self.cohesion_force = self.cohesion.compute(group) * self.weights["cohesion"]
			self.separation_force = self.separation.compute(group, delta) * self.weights["separation"]
			self.force += self.alignment_force + self.cohesion_force + self.separation_force
		else:
			self.state = "patrol"
			self.max_speed = 200

	def apply_movement(self, delta):
		self.avoid_obstacle(delta)
		super().update(delta)

	def avoid_obstacle(self, delta):
		next_pos = self.pos + self.vel * delta
		next_pos_tuple = (int(next_pos.x), int(next_pos.y))
		if next_pos_tuple in self.world.grid and not self.world.grid[next_pos_tuple]["walkable"]:
			original_heading = Vector2D(self.heading.x, self.heading.y)
			rotation_angles = [30, -30, 45, -45, 60, -60, 90, -90, 135, -135, 180]

			for angle in rotation_angles:
				test_heading = Vector2D(original_heading.x, original_heading.y)
				test_heading.rotate(angle)
				adjusted_pos = self.pos + (test_heading.normalise() * max(self.vel.length(),50) * delta)
				self.world.wrap_around(adjusted_pos)
				adjusted_tuple = (int(adjusted_pos.x), int(adjusted_pos.y))

				if self.world.grid[adjusted_tuple]["walkable"]:
					self.heading.rotate(angle)
					self.vel = self.heading.normalise() * self.max_speed
					return
			self.heading.rotate(90)

	def handle_patrol_behavior(self, delta):
		current_target = self.waypoints[self.current_index]
		to_target = current_target - self.pos
		distance = to_target.length()
		if distance < 10:
			self.current_index = (self.current_index + 1) % len(self.waypoints)
		direction = to_target.normalise() if distance > 0 else Vector2D()

		self.force = self.seek(current_target)

	def update(self, delta):
		self.draw_vision_cone()
		self.TagNeighbours(self.world.targets, radius=50)

		if self.health <= 0:
			self.execute()
			return
		self.handle_state_transitions()
		if self.state == "chase":
			self.handle_chase_behavior(delta)
		elif self.state == "patrol":
			self.handle_patrol_behavior(delta)
		elif self.state == "attack":
			self.handle_attack_behavior(delta)
		self.apply_movement(delta)
		self.vehicle.x = self.pos.x
		self.vehicle.y = self.pos.y
		self.vehicle.rotation = -self.heading.angle_degrees()



class SoldierAgent(Agent):
	def __init__(self,world, weapon):
		super().__init__(world)
		self.pos = Vector2D(20, 20)
		self.state = "objectives"
		for frame in PLAYER_ANIMATION.frames:
			frame.image.anchor_x = 35
			frame.image.anchor_y = 35
		self.vehicle = pyglet.sprite.Sprite(PLAYER_ANIMATION, x=self.pos.x, y=self.pos.y, batch=window.get_batch("main"))
		self.vehicle.scale = 3.0
		self.ammo = 0
		self.max_ammo = 10
		self.max_speed = 100
		self.weapon = weapon
		self.end_goal = window.goal_maker.pos
		self.safe_spot = window.safe_spot.pos
		self.fire_rate = 1.5
		self.attack_range = 100
		self.last_fire_time = 0
		self.attack_timer = 0
		self.marked_enemy = None
		self.next_step = None
		self.current_goal = None
		self.current_path = None
		self.max_health = 200

	def check_win_condition(self):
		if (self.pos - self.end_goal).length() < 10:
			print("Player reached the goal! Victory!")

			self.world.game_state = "win"
			self.draw_game_over_message()
			return True
		return False

	def check_safe_spot(self, delta):
		check_tuple = Vector2D(int(self.pos.x), int(self.pos.y))
		self.world.wrap_around(check_tuple)
		check_tuple = (check_tuple.x, check_tuple.y)

		if check_tuple in self.world.grid and self.world.grid[check_tuple]["safe_spot"]:
			self.health = min(self.health + 10 * delta, self.max_health)
			self.ammo = min(self.ammo + 0.5, self.max_ammo)
			print(f"🌿 Safe Spot: Healing {self.health}, Reloading {self.ammo}")

			return True
		return False

	def avoid_obstacle(self, delta):
		next_pos = self.pos + self.vel * delta
		next_pos_tuple = (int(next_pos.x), int(next_pos.y))
		if next_pos_tuple in self.world.grid and not self.world.grid[next_pos_tuple]["walkable"]:
			original_heading = Vector2D(self.heading.x, self.heading.y)
			rotation_angles = [30, -30, 45, -45, 60, -60, 90, -90, 135, -135, 180]

			for angle in rotation_angles:
				test_heading = Vector2D(original_heading.x, original_heading.y)
				test_heading.rotate(angle)
				adjusted_pos = self.pos + (test_heading.normalise() * self.vel.length() * delta)
				
				adjusted_tuple = (int(adjusted_pos.x), int(adjusted_pos.y))

				if self.world.grid[adjusted_tuple]["walkable"]:
					self.heading.rotate(angle)
					self.vel = self.heading.normalise() * self.vel.length()
					return
			self.heading.rotate(90)
			self.vel = Vector2D(0,0)

	def update_goal(self):
		if self.current_path and len(self.current_path) > 0:
			return

		end_goal_distance = self.pos.distance(self.end_goal)
		safe_spot_distance = self.pos.distance(self.safe_spot)

		if self.health < 50 or (self.ammo < 5 and end_goal_distance > safe_spot_distance):
			best_goal_tuple = (self.safe_spot.x, self.safe_spot.y)
		else:
			best_goal_tuple = (self.end_goal.x, self.end_goal.y)

		if self.current_goal is None or best_goal_tuple != (self.current_goal.x, self.current_goal.y):

			self.current_goal = Vector2D(best_goal_tuple[0], best_goal_tuple[1])
			self.current_path = self.world.get_path(self.pos, self.current_goal)

	def dodge(self, zombie):
		return self.flee(zombie.pos)

	def draw_game_over_message(self):
		if self.world.game_state == "win":
			self.game_over_label = pyglet.text.Label(
				"🎉 YOU WON!", font_name="Arial", font_size=36,
				x=400, y=300, anchor_x="center", anchor_y="center",
				color=(255, 255, 255, 255), batch=window.get_batch("winning")
			)
		else:
			self.game_over_label = pyglet.text.Label(
				"YOU LOSE!", font_name="Arial", font_size=36,
				x=400, y=300, anchor_x="center", anchor_y="center",
				color=(255, 255, 255, 255), batch=window.get_batch("winning")
			)
		window.cfg["WINNING"] = True
		self.world.paused = True


	def check_if_dodge(self):
		for zombie in self.world.targets:
			if (self.pos - zombie.pos).length() < 150:
				self.force = self.dodge(zombie)

	def follow_path(self, delta):
		if not self.current_path or len(self.current_path) < 1:
			return
		if self.next_step is None:
			self.next_step = Vector2D(self.current_path[0][0],self.current_path[0][1])
		if (self.pos - self.next_step).length() < max(self.vel.length() * 2.0, 50):
			self.current_path.pop(0)
			if self.current_path:
				self.next_step = Vector2D(self.current_path[0][0], self.current_path[0][1])
			else:
				self.next_step = None
				return
		self.force = self.seek(self.next_step)
		self.vel += self.force * delta


	def handle_attack_behavior(self, delta):
		self.attack_timer -= delta
		if self.marked_enemy and (self.pos - self.marked_enemy.pos).length() < self.attack_range:
			self.vel = Vector2D(0, 0)
			if self.attack_timer <= 0:
				self.fire()
				self.attack_timer = self.fire_rate
		else:
			self.state = "objectives"

	def update(self, delta):
		left_angle = self.heading.copy().rotate(-45)
		right_angle = self.heading.copy().rotate(45)

		left_x = self.pos.x + (left_angle.x * 100)
		left_y = self.pos.y + (left_angle.y * 100)
		right_x = self.pos.x + (right_angle.x * 100)
		right_y = self.pos.y + (right_angle.y * 100)
		self.vision_cone = pyglet.shapes.Polygon(
			(self.pos.x, self.pos.y),
			(left_x, left_y),
			(right_x, right_y),
			color=(255, 255, 0, 100), batch=window.get_batch("main")
		)
		if self.health <= 0:
			print("Player defeated! Game Over.")
			self.draw_game_over_message()
			self.execute()
			return

		if self.check_win_condition():
			return

		if self.marked_enemy and (self.pos - self.marked_enemy.pos).length() < 50:
			if self.state != "attack":
				self.state = "attack"
			self.handle_attack_behavior(delta)

		elif self.health < 50 or self.ammo < 5:
			if self.state != "survival":
				self.state = "survival"
				self.update_goal()
			if self.check_safe_spot(delta):
				self.vel = Vector2D(0,0)
				return
			if self.health > 100 and self.ammo > 8:
				self.state = "objectives"
				return
			self.follow_path(delta)
		else:
			if self.state != "objectives":
				self.state = "objectives"

			self.update_goal()
			self.detect_enemy()

			self.follow_path(delta)

			if self.marked_enemy:
				self.check_if_dodge()
		edge_margin = 50
		if self.pos.x < edge_margin or self.pos.x > self.world.cx - edge_margin:
			self.vel.x *= 0.7
		if self.pos.y < edge_margin or self.pos.y > self.world.cy - edge_margin:
			self.vel.y *= 0.7
		self.avoid_obstacle(delta)
		super().update(delta)
		self.vehicle.x = self.pos.x
		self.vehicle.y = self.pos.y
		self.vehicle.rotation = -self.heading.angle_degrees()


	def switch_weapon(self, new_weapon):
		print(f"Switching weapon to {new_weapon.mode}")
		self.weapon = new_weapon
	def detect_enemy(self):
		enemies_in_range = [enemy for enemy in self.world.targets if (self.pos - enemy.pos).length() < 150]
		if enemies_in_range:
			self.marked_enemy = min(enemies_in_range, key=lambda e: (self.pos-e.pos).length())

	def enemy_defeated(self):
		if self.marked_enemy:
			if self.marked_enemy.health <= 0:
				self.marked_enemy = None
				return True
		return False
	def predict_target(self, target):
		time_travel = (self.pos - target.pos).length() / self.weapon.speed
		future_pos = target.pos + target.vel * time_travel
		return future_pos
	def fire(self):
		current_time = time.time()
		if self.marked_enemy:
			if not self.enemy_defeated():
				if self.ammo > 0 and (current_time - self.last_fire_time >= self.fire_rate):
					self.ammo -= 1
					self.last_fire_time = current_time
					predicted_pos = self.predict_target(self.marked_enemy)
					accuracy_factor = 70.0 / self.weapon.accuracy
					random_offset = Vector2D(uniform(-accuracy_factor, accuracy_factor),
											 uniform(-accuracy_factor, accuracy_factor))
					direction = (predicted_pos - self.pos + random_offset).normalise()
					if self.weapon.mode == "rifle" or self.weapon.mode == "handgun":
						projectile = Projectile(self, self.marked_enemy, direction, self.world)
						self.world.projectiles.append(projectile)
					elif self.weapon.mode == "rocket":
						projectile = RocketProjectile(self, self.marked_enemy, direction, self.world)
						self.world.projectiles.append(projectile)
					elif self.weapon.mode == "handgrenade":
						projectile = HandGrenade(self, self.marked_enemy, direction, self.world)
						self.world.projectiles.append(projectile)


