from .base import Base


class Electrode(Base):

    def reset(self):
        self.alive = True

    def get_animations(self):

        animation_levels = [
            self.engine._get_sprites(['electrode1', 'electrode2', 'electrode3']),
            self.engine._get_sprites(['electrode4', 'electrode5', 'electrode6']),
            self.engine._get_sprites(['electrode7', 'electrode8', 'electrode9']),
            self.engine._get_sprites(['electrode10', 'electrode11', 'electrode12']),
            self.engine._get_sprites(['electrode13', 'electrode14', 'electrode15']),
            self.engine._get_sprites(['electrode16', 'electrode17', 'electrode18']),
            [],
            self.engine._get_sprites(['electrode25', 'electrode26', 'electrode27']),
            [],
            self.engine._get_sprites(['electrode19', 'electrode20', 'electrode21']),
        ]
        return animation_levels[(self.engine.level % 10)]

    def update(self):
        if self.alive:
            if any(self.rect.colliderect(sprite.rect)
                   for sprite in self.engine._get_enemy_group() if self != sprite):
                self.alive = False
        else:
            self.animation_step += 1
            if self.animation_step >= len(self.animations):
                self.kill()
            else:
                self.image = self.animations[self.animation_step]

    def die(self, killer):
        self.alive = False
