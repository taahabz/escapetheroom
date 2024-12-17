import pygame
import time
from resources import RESOURCES, TEXTURES  # Assuming resources and textures are managed similarly
from configs import IS_PLAY_SLEEP_ANIMATION
class AgentCommand:
    TOP = 0
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3

    @staticmethod
    def from_int(value):
        if value == 0:
            return AgentCommand.TOP
        elif value == 1:
            return AgentCommand.LEFT
        elif value == 2:
            return AgentCommand.BOTTOM
        else:
            return AgentCommand.RIGHT

    @staticmethod
    def to_int(command):
        return command

class Agent:
    def __init__(self):
        resources = RESOURCES.get()
        lvl = resources.lvl_info
        self.pos = lvl.agent  # (x, y)
        self.game_size = lvl.size  # (width, height)
        self.birth_ts = time.time()

    def update(self, command, has_all_keys):
        resources = RESOURCES.get()

        if self.is_agent_asleep():
            return

        # Update player position
        new_loc = list(self.pos)
        if command == AgentCommand.LEFT:
            new_loc[0] -= 1
        elif command == AgentCommand.RIGHT:
            new_loc[0] += 1
        elif command == AgentCommand.BOTTOM:
            new_loc[1] += 1
        elif command == AgentCommand.TOP:
            new_loc[1] -= 1

        # Ensure new position is not a wall or a door (unless all keys are collected)
        is_not_wall = not resources.lvl_map.get_tile("LAYER_WALLS", new_loc[0], new_loc[1])
        is_not_door = not resources.lvl_map.get_tile("LAYER_DOOR", new_loc[0], new_loc[1])

        if is_not_wall and (is_not_door or has_all_keys) and self.is_in_bounds(new_loc[0], new_loc[1]):
            self.pos = tuple(new_loc)

    def draw(self, scale_factor, offset_x, offset_y):
        textures = TEXTURES.get()
        elapsed_time = time.time() - self.birth_ts

        if elapsed_time < 1:
            texture = textures.agent_sleep1_texture
        elif elapsed_time < 2:
            texture = textures.agent_sleep2_texture
        elif elapsed_time < 3:
            texture = textures.agent_sleep3_texture
        else:
            texture = textures.agent_texture

        if not IS_PLAY_SLEEP_ANIMATION:
            texture = textures.agent_texture

        texture_rect = texture.get_rect()
        draw_x = self.pos[0] * scale_factor + offset_x
        draw_y = self.pos[1] * scale_factor + offset_y

        pygame.Surface.blit(pygame.display.get_surface(), texture, (draw_x, draw_y), texture_rect)

    def is_agent_asleep(self):
        if not IS_PLAY_SLEEP_ANIMATION:
            return False

        elapsed_time = time.time() - self.birth_ts
        return elapsed_time < 4

    def is_in_bounds(self, x, y):
        return 0 <= x < self.game_size[0] and 0 <= y < self.game_size[1]
