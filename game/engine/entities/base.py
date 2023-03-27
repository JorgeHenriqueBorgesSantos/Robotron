import math
import random
from typing import TYPE_CHECKING, Tuple
import pygame

if TYPE_CHECKING:
    from ..engine import Engine


class Base(pygame.sprite.Sprite):

    NONE = 0
    UP = 1
    UP_RIGHT = 2
    RIGHT = 3
    DOWN_RIGHT = 4
    DOWN = 5
    DOWN_LEFT = 6
    LEFT = 7
    UP_LEFT = 8

    def __init__(self, engine: 'Engine', **kwargs):
        super().__init__()
        self.engine = engine
        self.play_rect = self.engine.play_rect
        self.args = kwargs
        self.config_dict = self.load_config()

        self.cycle = None
        self.animations = self.get_animations()
        self.animation_step = 0
        self.animation_direction = None

        self.speed = 0
        self.move_delay = 0
        self.move_countdown = self.move_delay

        self.setup()
        self.update_animation()

        if 'center' in kwargs:
            self.rect = self.image.get_rect()
            self.rect.center = kwargs['center']
        else:
            self.random_location()

    def load_config(self):
        return self.engine.config.get(self.__class__.__name__.lower())

    def config(self, key: str, default: any = None):
        if key not in self.config_dict:
            print(f"Warning: Missing config key for class {self.__class__.__name__}: {key}")
        return self.config_dict[key] if key in self.config_dict else default

    def score(self):

        return self.config('score')

    def get_animations(self):

        raise NotImplementedError()

    def update(self):
        """ Just update state of sprites. """

    def get_vector(self, direction: int, speed: float = None):

        speed = speed or self.speed
        if direction == 0:
            return pygame.Vector2(0)
        elif direction == self.UP:
            return pygame.Vector2(0, -speed)
        elif direction == self.UP_RIGHT:
            return pygame.Vector2(speed, -speed)
        elif direction == self.RIGHT:
            return pygame.Vector2(speed, 0)
        elif direction == self.DOWN_RIGHT:
            return pygame.Vector2(speed, speed)
        elif direction == self.DOWN:
            return pygame.Vector2(0, speed)
        elif direction == self.DOWN_LEFT:
            return pygame.Vector2(-speed, speed)
        elif direction == self.LEFT:
            return pygame.Vector2(-speed, 0)
        elif direction == self.UP_LEFT:
            return pygame.Vector2(-speed, -speed)

        raise ValueError(f'Invalid direction: {direction}')

    def valid_move(self, direction: int):

        vector = self.get_vector(direction)
        test = self.rect.copy()
        test.center += vector

        if not self.inside(test):
            return False

        return True

    def inside(self, rect):

        if (rect.top <= self.play_rect.top or
                rect.left <= self.play_rect.left or
                rect.bottom >= self.play_rect.bottom or
                rect.right >= self.play_rect.right):
            return False

        return True

    def update_animation(self):

        if isinstance(self.animations, list):
            animations = self.animations
        else:
            animations = self.animations[self.animation_direction or 'down']

        if self.animation_step >= (self.cycle or len(animations)):
            self.animation_step = 0

        self.image = animations[self.animation_step]
        self.animation_step += 1

    def die(self, killer):

        del killer
        self.kill()

    def setup(self):

        self.reset()

    def reset(self):

        self.animation_step = 0
        self.update_animation()
        self.random_location()

    def random_direction(self):

        return random.randrange(1, 8)

    def random_location(self):

        (sprite_width, sprite_height) = self.image.get_rect().size

        self.rect = self.image.get_rect()
        player_box = self.engine._get_player_box()

        valid_location = False
        tries = 0
        while not valid_location:
            tries += 1
            self.rect.x = self.play_rect.x + random.randrange(self.play_rect.width - sprite_width)
            self.rect.y = self.play_rect.y + random.randrange(self.play_rect.height - sprite_height)

            if tries > 25:
                print("Warning!  Enemy Placement Overflow.")
                break

            if player_box.contains(self.rect):
                continue

            if any(self.rect.colliderect(sprite.rect)
                    for sprite in self.engine.all_group if self != sprite):
                continue

            valid_location = True

    def get_distance_to_sprite(self, sprite: 'Base'):

        my_x, my_y = self.rect.center
        their_x, their_y = sprite.rect.center
        return math.hypot(my_x-their_x, my_y-their_y)

    def get_distance_to_player(self):

        return self.get_distance_to_sprite(self.engine.player)

    def get_vector_to_point(self, point: Tuple[int, int], round_results: bool = False):

        x, y = point
        dx, dy = x - self.rect.x, y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
        if round_results:
            dx = round(dx)
            dy = round(dy)
        return pygame.Vector2(dx, dy)

    def move_toward_point(self, point: Tuple[int, int], speed: float):

        vector = self.get_vector_to_point(point)
        self.rect.center += vector * speed

    def get_vector_to_player(self):

        return self.get_vector_to_point(self.engine.player.rect.center)

    def move_toward_player(self, speed):

        vector = self.get_vector_to_player()
        self.rect.center += vector * speed
