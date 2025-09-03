from vector2d import Vector2D

class Separation:
    def __init__(self, agent):
        self.agent = agent
        self.crowd_threshold = 4
        self.threshold_radius = 50
    def compute(self, group, delta):
        steering_force = Vector2D()
        bot_count = 0

        for bot in group:
            if bot != self.agent and bot.tagged:
                ToBot = bot.pos - self.agent.pos
                distance = ToBot.length()

                if distance < self.threshold_radius:
                    bot_count += 1
                    steering_force += ToBot.normalise() / distance
        if bot_count > self.crowd_threshold:
            wander_intensity = (bot_count - self.crowd_threshold) / self.crowd_threshold
            wander_force = self.agent.wander(delta) * (0.5 + (0.5 * wander_intensity))
            steering_force += wander_force

        return steering_force

class Alignment:
    def __init__(self, agent):
        self.agent = agent
    def compute(self, group):
        avg_heading = Vector2D()
        avg_count = 0

        for bot in group:
            if bot != self.agent and bot.tagged:
                avg_heading += bot.heading
                avg_count += 1
        if avg_count > 0:
            avg_heading /= float(avg_count)
            avg_heading -= self.agent.heading
        return avg_heading

class Cohesion:
    def __init__(self, agent):
        self.agent = agent
    def compute(self, group):
        centre_mass = Vector2D()
        steering_force = Vector2D()
        avg_count = 0

        for bot in group:
            if bot != self.agent and bot.tagged:
                centre_mass += bot.pos
                avg_count += 1
        if avg_count > 0:
            centre_mass /= float(avg_count)
            steering_force = self.agent.seek(centre_mass)

        return steering_force

