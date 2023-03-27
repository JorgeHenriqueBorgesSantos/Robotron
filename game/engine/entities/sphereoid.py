import random
from .enforcer import Enforcer
from .generator import Generator


class Sphereoid(Generator):

    SPEED = 5
    MOVE_DELAYS = [10, 32]
    MOVE_CURVATURES = [-50, 50]

    def reset(self):
        super().reset()
        self.speed = self.config('speed', self.SPEED)
        self.move_delays = self.config('move_delays', self.MOVE_DELAYS)
        self.move_curvatures = self.config('move_curvatures', self.MOVE_CURVATURES)
        self.update_curvature_and_countdowns()

    def get_animations(self):

        return self.engine._get_sprites([
            'sphereoid1', 'sphereoid2', 'sphereoid3', 'sphereoid4',
            'sphereoid5', 'sphereoid6', 'sphereoid7', 'sphereoid8'])

    def get_spawn(self):

        return Enforcer(self.engine, center=self.rect.center)

    def update_curvature_and_countdowns(self):

        self.move_curvature.x = random.randint(*self.move_curvatures) / 1000
        self.move_curvature.y = random.randint(*self.move_curvatures) / 1000
        self.move_delay = random.randrange(*self.move_delays)

    def move(self):

        if not self.alive:
            return

        self.move_delay -= 1
        if self.move_delay == 0:
            self.update_curvature_and_countdowns()

        self.move_deltas.x = min(self.speed, max(-self.speed, self.move_deltas.x + self.speed * self.move_curvature.x))
        self.move_deltas.y = min(self.speed, max(-self.speed, self.move_deltas.y + self.speed * self.move_curvature.y))
        self.rect.center += self.move_deltas
        self.rect.clamp_ip(self.play_rect)
