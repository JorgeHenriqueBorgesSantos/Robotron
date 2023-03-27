from .base import Base


class Floater(Base):

    def setup(self):
        self.delay = self.args['delay'] if 'delay' in self.args else 15

    def get_animations(self):

        keys = self.args.keys()

        if 'sprite' in keys:
            sprite = self.args['sprite']
        elif 'sprite_name' in keys:
            sprite = self.engine._get_sprite(str(self.args['sprite_name']))
        else:
            raise ValueError("Invalid sprite passed.")

        return [sprite]

    def update(self):
        self.delay -= 1
        if self.delay == 0:
            self.kill()
