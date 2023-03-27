import random
import pygame
from .base import Base


class EnforcerBullet(Base):

    MAX_SPEED = 30
    DEFAULT_TIME_TO_LIVE = 50

    WEIGHT = 2
    WIDTH = HEIGHT = 16

    def setup(self):
        self.time_to_live = self.config('time_to_live', self.DEFAULT_TIME_TO_LIVE)
        self.max_speed = self.config('max_speed', self.MAX_SPEED)
        self.max_distance = self.engine._get_play_area_distance()
        self.vector = None

    def get_trajectory(self):

        if not self.vector:
            engine = self.engine
            distance_to_player = self.get_distance_to_player()
            speed = ((distance_to_player * self.max_speed) / self.max_distance) + 1
            player_rect = engine.player.rect
            x_trajectory = random.randint(player_rect.left - 10, player_rect.right + 10)
            y_trajectory = random.randint(player_rect.top - 10, player_rect.bottom + 10)
            new_vector = pygame.Vector2(x_trajectory, y_trajectory) - pygame.Vector2(self.rect.center)
            if new_vector.length() == 0:

                return self.get_trajectory()
            self.vector = new_vector.normalize() * speed
            self.random_vector = pygame.Vector2(random.random(), random.random())
        else:
            self.random_vector *= 1.01

        return self.vector + self.random_vector

    def get_animations(self):

        image1 = pygame.Surface([self.WIDTH, self.HEIGHT]).convert()
        pygame.draw.line(image1, [255, 255, 255], (self.WIDTH, 0), (0, self.HEIGHT), self.WEIGHT)
        pygame.draw.line(image1, [255, 255, 255], (0, 0), (self.WIDTH, self.HEIGHT), self.WEIGHT)
        image1.set_colorkey((0, 0, 0))
        image2 = pygame.Surface([self.WIDTH, self.HEIGHT]).convert()
        pygame.draw.line(image2, [255, 255, 255], (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT), self.WEIGHT)
        pygame.draw.line(image2, [255, 255, 255], (0, self.HEIGHT // 2), (self.WIDTH, self.HEIGHT // 2), self.WEIGHT)
        image2.set_colorkey((0, 0, 0))
        return [image1, image2]

    def update(self):
        if self.time_to_live % 3 == 0:
            self.update_animation()
        self.rect.center += self.get_trajectory()
        self.rect.clamp_ip(self.play_rect)

        self.time_to_live -= 1
        if self.time_to_live <= 0:
            self.kill()

    def reset(self):

        self.kill()


class Enforcer(Base):

    MAX_SPEED = 20
    SHOOT_DELAYS = [10, 30]

    def get_animations(self):

        return self.engine._get_sprites(['enforcer2', 'enforcer3', 'enforcer4', 'enforcer5', 'enforcer6', 'enforcer1'])

    def setup(self):
        self.max_speed = self.config('max_speed', self.MAX_SPEED)
        self.shoot_delays = self.config('shoot_delays', self.SHOOT_DELAYS)

        self.animation_step = 0
        self.animation_delay = 0
        self.update_animation()

        self.rect = self.image.get_rect()
        self.active = 0

        self.max_distance = self.engine._get_play_area_distance()
        self.offset_update = 0
        self.random_offset = 0
        self.shoot_delay = random.randint(*self.shoot_delays)

    def update(self):
        self.update_animation()
        self.move()
        self.shoot()

    def update_animation(self):

        if self.animation_step < len(self.animations):
            if self.animation_delay == 0:
                self.image = self.animations[self.animation_step]
                self.animation_step += 1
                self.animation_delay = 3
            else:
                self.animation_delay -= 1
        else:
            self.active = True

    def move(self):

        if self.active:
            if self.offset_update <= 0:
                self.random_offset = random.randint(-5, 1)
                self.offset_update = random.randint(10, 30)

            self.offset_update -= 1

            distance_to_player = self.get_distance_to_player()
            speed = ((distance_to_player * self.max_speed) / self.max_distance) + 1
            self.move_toward_player(speed + self.random_offset)
            self.rect.clamp_ip(self.play_rect)

    def shoot(self):

        self.shoot_delay -= 1
        if self.shoot_delay <= 0:
            self.shoot_delay = random.randint(*self.shoot_delays)
            self.engine._add_enemy(EnforcerBullet(self.engine, center=self.rect.center))

    def reset(self):

        self.kill()
