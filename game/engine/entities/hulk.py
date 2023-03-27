import random
import pygame
from .base import Base


class Hulk(Base):

    def get_animations(self):

        return {
            'left': self.engine._get_sprites(['hulk1', 'hulk2', 'hulk1', 'hulk3']),
            'right': self.engine._get_sprites(['hulk7', 'hulk8', 'hulk7', 'hulk9']),
            'down': self.engine._get_sprites(['hulk4', 'hulk5', 'hulk4', 'hulk6']),
            'up': self.engine._get_sprites(['hulk4', 'hulk5', 'hulk4', 'hulk6'])
        }

    def reset(self):
        self.update_animation()
        self.random_location()

        self.speed = 7
        self.turn_percentage = 20
        self.move_delay = (5, 25)
        self.move_countdown = random.randrange(*self.move_delay)

        self.move_directions = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        self.direction = random.choice(self.move_directions)
        self.animation_direction = self.get_direction_string(self.direction)

    def get_direction_string(self, direction: int):

        if direction == self.UP:
            return 'up'
        if direction == self.DOWN:
            return 'down'
        if direction in [self.LEFT, self.UP_LEFT, self.DOWN_LEFT]:
            return 'left'
        if direction in [self.RIGHT, self.UP_RIGHT, self.DOWN_RIGHT]:
            return 'right'

    def turn(self):

        idx = self.move_directions.index(self.direction)
        if random.randrange(0, 1) == 0:
            idx += 1
            if idx >= len(self.move_directions):
                idx = 0
        else:
            idx -= 1
            if idx < 0:
                idx = len(self.move_directions) - 1

        self.direction = self.move_directions[idx]

    def move(self):

        if random.randrange(1, 100) < self.turn_percentage:
            self.turn()

        i = 0
        while not self.valid_move(self.direction):
            self.turn()
            i += 1
            if i > 100:
                print("Hulk stuck in a loop", self.rect.center)
                self.reset()

        self.rect.center += self.get_vector(self.direction)
        self.rect.clamp_ip(self.play_rect)
        self.animation_direction = self.get_direction_string(self.direction)
        self.update_animation()

    def update(self):
        if self.move_countdown <= 0:
            self.move()
            self.move_countdown = random.randrange(*self.move_delay)
        else:
            self.move_countdown -= 1

        for sprite in pygame.sprite.spritecollide(self, self.engine.family_group, False):
            sprite.die(self)

    def die(self, killer):

        self.rect.center += self.get_vector(killer.direction, 3)
        self.rect.clamp_ip(self.play_rect)
