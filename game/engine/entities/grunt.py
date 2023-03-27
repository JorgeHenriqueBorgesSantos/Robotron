import random
from .base import Base


class Grunt(Base):


    def get_animations(self):

        return self.engine._get_sprites(['grunt1', 'grunt2', 'grunt1', 'grunt3'])

    def reset(self):
        self.speed = 7
        self.move_delay = (5, 25)
        self.move_countdown = random.randrange(*self.move_delay)

    def move(self):

        self.update_animation()
        self.move_toward_player(self.speed)

    def update(self):
        if self.move_countdown <= 0:
            self.move()
            self.move_countdown = random.randrange(*self.move_delay)
        else:
            self.move_countdown -= 1
