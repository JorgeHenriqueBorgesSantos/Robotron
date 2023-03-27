import math
import os
from typing import List, Tuple
import pygame
from .config import Config
from .graphics import load_graphics
from .entities import Player, Mommy, Daddy, Mikey, Grunt, Electrode, Hulk, Sphereoid, Quark, Brain


class Engine:

    def __init__(self,
                 start_level: int = 1,
                 lives: int = 3,
                 fps: int = 0,
                 config_path: str = None,
                 godmode: bool = False,
                 headless: bool = False):
        self.godmode = godmode
        self.start_level = start_level - 1
        self.level = self.start_level
        self.start_lives = lives
        self.lives = lives
        self.fps = fps

        self.score = 0
        self.extra_lives = 0
        self.done = False
        self.frame = 0

        self.config = Config(config_path)

        pygame.init()
        pygame.display.set_caption('Robotron 2084')

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        screen_size = self.config.get('screen_size')
        if headless:
            print("Using dummy video driver.")
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.screen = pygame.display.set_mode(screen_size)
        self.graphics = load_graphics()

        self.play_area = self.config.get('play_area')
        (top, left, bottom, right) = self.play_area
        self.play_rect = pygame.Rect(left, top, right - left, bottom - top)

        self.family_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.to_kill_group = pygame.sprite.Group()
        self.all_group = pygame.sprite.Group()
        self.waves = self.config.get('waves')
        self.to_kill_group_types = ['Grunt', 'Sphereoid', 'Enforcer', 'Brain', 'Quark', 'Tank']
        self.enemies = ['grunt', 'electrode', ]

        self.extra_life_score = self.config.get('extra_life_score')
        self.player = None
        self.player_box = None
        self.family_collected = 0

        self._initialize_level()

    def handle_input(self, move, shoot):

        if not self.done:
            self.player.move(move)
            self.player.shoot(shoot)

    def set_level(self, level):

        self.level = level - 1
        self._initialize_level()

    def _initialize_level(self):

        for sprite in self.all_group:
            sprite.kill()

        self.player = Player(self)
        self._add_sprite(self.player)

        self.family_collected = 0

        wave_level = self.level if self.level < 20 else 20 + self.level % 20
        level_data = self.waves[wave_level]
        (grunts, electrodes, hulks, brains, sphereoids, quarks, mommies, daddies, mikeys) = level_data
        _ = [self._add_family(Mikey(self)) for _ in range(mikeys)]
        _ = [self._add_family(Mommy(self)) for _ in range(mommies)]
        _ = [self._add_family(Daddy(self)) for _ in range(daddies)]
        _ = [self._add_enemy(Grunt(self)) for _ in range(grunts)]
        _ = [self._add_enemy(Electrode(self)) for _ in range(electrodes)]
        _ = [self._add_enemy(Hulk(self)) for _ in range(hulks)]
        _ = [self._add_enemy(Sphereoid(self)) for _ in range(sphereoids)]
        _ = [self._add_enemy(Quark(self)) for _ in range(quarks)]
        _ = [self._add_enemy(Brain(self)) for _ in range(brains)]

    def _set_family_collected(self):

        self.family_collected += 1
        self.score += min(self.family_collected * 1000, 5000)
        return self.family_collected

    def _get_play_area_distance(self):

        w, h = self.play_rect.size
        return math.hypot(w, h)

    def _get_family_group(self) -> pygame.sprite.Group:

        return self.family_group

    def _get_enemy_group(self) -> pygame.sprite.Group:

        return self.enemy_group

    def _get_all_group(self) -> pygame.sprite.Group:

        return self.all_group

    def _get_sprite(self, sprite_name: str) -> pygame.Surface:

        return self.graphics[sprite_name]

    def _get_sprites(self, sprite_names: List[str]) -> List[pygame.Surface]:

        return [self.graphics[name] for name in sprite_names]

    def _get_player_box(self):

        if self.player_box is None:
            (x, y) = self.player.rect.center
            (w, h) = (self.play_rect.width // 3, self.play_rect.height // 3)
            self.player_box = pygame.Rect(x - w // 2, y - h // 2, w, h)

        return self.player_box

    def _add_background(self):

        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, [238, 5, 8], self.play_rect.inflate(15, 15), 5)

    def _add_info(self):

        text = self.font.render(
            f'Score: {self.score} Level: {self.level + 1} Lives: {self.lives} {"GAME OVER" if self.done else ""}',
            True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (self.play_rect.x, self.play_rect.y - 40))

    def _add_sprite(self, sprite: pygame.sprite):

        self.all_group.add(sprite)

    def _add_family(self, family: pygame.sprite):

        self.family_group.add(family)
        self.all_group.add(family)

    def _add_enemy(self, enemy: pygame.sprite):

        self.enemy_group.add(enemy)
        self.all_group.add(enemy)

        if enemy.__class__.__name__ in self.to_kill_group_types:
            self.to_kill_group.add(enemy)

    def update(self):

        pygame.event.pump()
        self.clock.tick(self.fps)
        self.frame += 1

        if self.extra_life_score > 0:
            if self.score // self.extra_life_score > self.extra_lives:
                self.lives += 1
                self.extra_lives += 1

        if not self.done:
            self.all_group.update()

            if not self.godmode and pygame.sprite.spritecollide(self.player, self.enemy_group, False):
                self.family_collected = 0
                if self.lives > 0:
                    self.lives -= 1
                    for sprite in self.all_group:
                        sprite.reset()
                else:
                    self.done = True

            if not self.to_kill_group:
                self.level += 1
                self._initialize_level()

        self.draw()
        image = self.get_image()

        return (image, self.score, self.lives, self.level, self.done)

    def draw(self):

        self._add_background()
        self._add_info()
        self.all_group.draw(self.screen)
        pygame.display.update()

    def family_remaining(self):

        return len(self.family_group)

    def get_sprite_data(self) -> List[Tuple[int, int, str]]:

        (top, left, _, _) = self.play_area

        data = []
        for enemy in self.all_group:
            if enemy.__class__.__name__ != 'Floater':
                data.append((enemy.rect.x - left, enemy.rect.y - top, enemy.__class__.__name__))

        return data

    def reset(self):

        self.frame = 0
        self.level = self.start_level
        self.score = 0
        self.lives = self.start_lives
        self.extra_lives = 0
        self.done = False

        self._initialize_level()

        return self.get_image()

    @ staticmethod
    def get_image() -> List:

        return pygame.surfarray.array3d(pygame.display.get_surface()).swapaxes(0, 1)
