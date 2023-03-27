import random
import pygame
from .base import Base
from .floater import Floater


class Family(Base):

    SPEED = 4
    MOVE_DELAY = 5

    def setup(self):

        self.speed = self.config('speed', self.SPEED)
        self.move_delay = self.config('move_delay', self.MOVE_DELAY)

        self.reset()

    def load_config(self):

        return self.engine.config.get('family')

    def reset(self):

        self.move_direction = random.randrange(1, 8)
        self.update_animation()
        self.random_location()

    def get_animations(self):

        prefix = self.PREFIX
        return {
            'left': self.engine._get_sprites([prefix + '1', prefix + '2', prefix + '1', prefix + '3']),
            'right': self.engine._get_sprites([prefix + '4', prefix + '5', prefix + '4', prefix + '6']),
            'down': self.engine._get_sprites([prefix + '7', prefix + '8', prefix + '7', prefix + '9']),
            'up': self.engine._get_sprites([prefix + '10', prefix + '11', prefix + '10', prefix + '12']),
        }

    def update_animation(self):

        animations = self.animations[self.animation_direction or 'down']
        self.animation_step += 1
        if self.animation_step >= (self.cycle or len(animations)):
            self.animation_step = 0

        self.image = animations[self.animation_step]

    def move(self):

        if self.engine.frame % self.move_delay == 0:
            valid_directions = list(range(1, 8))

            direction = self.move_direction
            while not self.valid_move(direction):
                if direction in valid_directions:
                    valid_directions.remove(direction)
                if len(valid_directions) == 0:
                    direction = 0
                    break

                direction = random.choice(valid_directions)

            self.vector = self.get_vector(direction)
            self.rect.center += self.vector
            self.move_direction = direction

    def collected(self):

        level = self.engine._set_family_collected()
        level = min(level, 5)
        self.engine._add_sprite(Floater(self.engine, center=self.rect.center, sprite_name=str(level*1000)))
        self.kill()

    def die(self, killer):
        self.engine._add_sprite(Floater(self.engine, center=self.rect.center, sprite_name='familydeath'))
        self.kill()

    def update(self):

        self.update_animation()
        if self.engine.frame % self.move_delay == 0:
            self.move()

        for sprite in pygame.sprite.spritecollide(self, self.engine._get_enemy_group(), False):
            if sprite.__class__.__name__ == 'Hulk':
                self.die(sprite)


class Mommy(Family):

    PREFIX = 'mommy'


class Daddy(Family):

    PREFIX = 'daddy'


class Mikey(Family):

    PREFIX = 'mikey'
