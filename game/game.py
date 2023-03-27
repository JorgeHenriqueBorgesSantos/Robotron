from typing import Tuple
import numpy as np
import gym
from .engine import Engine
from .utils import crop


class Environment(gym.Env):

    FAMILY_REWARD = 10.0

    def __init__(self,
                 level: int = 1,
                 lives: int = 3,
                 fps: int = 0,
                 config_path: str = None,
                 godmode: bool = False,
                 always_move: bool = False,
                 headless: bool = True):

        self.engine = Engine(start_level=level, lives=lives, fps=fps, config_path=config_path,
                             godmode=godmode, headless=headless)
        width, height = self.engine.play_rect.size
        play_area = (height, width, 3)

        self.score = 0
        self.action_mod = 1 if always_move else 0
        self.actions = 8 if always_move else 9
        self.action_space = gym.spaces.Discrete(self.actions * self.actions)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=play_area, dtype=np.uint8)
        self.metadata = {'render.modes': ['human', 'rgb_array']}

    def get_board_size(self):

        return self.engine.play_rect.size

    def reset(self):

        self.score = 0
        return self.get_state(self.engine.reset())

    def step(self,  action: int) -> Tuple[np.ndarray, int, bool, dict]:

        if not 0 <= action <= self.action_space.n:
            raise ValueError(f'Action {action} is invalid.')

        move = action // self.actions
        shoot = action % self.actions

        self.engine.handle_input(move + self.action_mod, shoot + self.action_mod)
        (image, score, lives, level, dead) = self.engine.update()

        reward = (self.engine.score - self.score) / 100.0
        self.score = self.engine.score

        if dead:
            reward = -1

        return self.get_state(image), reward, dead, {
            'score': score,
            'level': level,
            'lives': lives,
            'family': self.engine.family_remaining(),
            'data': self.engine.get_sprite_data(),
        }

    def get_state(self, image):

        image = crop(image, self.engine.play_area)
        return image

    def render(self, mode='human'):

        image = self.engine.get_image()
        if mode == 'human':
            return image
        else:
            return self.get_state(image)
