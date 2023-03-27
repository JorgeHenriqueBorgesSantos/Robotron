import random
import pygame
from .floater import Floater
from .family import Family


class Prog(Family):

    SPEED = 3
    MOVE_DELAY = 5
    PROGRAMMING_TIME = 60

    def setup(self):
        self.speed = self.config('speed', Prog.SPEED)
        self.move_delay = self.config('move_delay', Prog.MOVE_DELAY)
        self.programming_time = self.config('programming_time', Prog.PROGRAMMING_TIME)

        self.vector = None
        self.offset = 0
        self.trail_group = pygame.sprite.Group()

        self.reset()

    def load_config(self):

        return self.engine.config.get('prog')

    def get_animations(self):

        prefix = self.args['family']
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

        image = animations[self.animation_step]
        color = ((255, 0, 0), (0, 255, 0), (0, 255, 0))[self.engine.frame % 3]
        inv = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        inv.fill(color)
        inv.blit(image, (0, 0), None, pygame.BLEND_RGB_SUB)
        self.image = inv

    def reset(self):
        return self.kill()

    def move(self):

        if self.vector is None or self.engine.frame % self.move_delay == 0:
            prect = self.engine.player.rect
            x = 1 if prect.x > self.rect.x else -1
            y = 1 if prect.y > self.rect.y else -1

            if random.random() < 0.25:
                x = -x
            if random.random() < 0.25:
                y = -y
            self.vector = pygame.Vector2(x, y)
        self.engine._add_sprite(Floater(self.engine, center=self.rect.center, sprite=self.image, delay=5))
        self.rect.center += self.vector * self.speed
        self.rect.clamp_ip(self.play_rect)

    def collected(self):
        pass

    def die(self, killer):

        del killer
        for sprite in self.trail_group:
            sprite.kill()
        self.kill()

    def update(self):

        self.update_animation()

        if self.programming_time > 0:
            if self.engine.frame % 2 == 0:
                self.rect.y -= self.offset
                self.offset = random.randint(0, self.rect.height) - (self.rect.height // 2)
                self.rect.y += self.offset
            self.programming_time -= 1
        else:
            self.move()
