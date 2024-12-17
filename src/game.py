import pygame
import random
from resources import RESOURCES, TEXTURES
from agent import Agent, AgentCommand
from enemy import EnemyManager
from configs import NUM_FRAMES
from configs import FF_WEIGHT_THRESHOLD, MUTATION_PROBABILITY, UNIT_FRAME_SIZE, FRAME_SCALE

class Game:
    def __init__(self):
        resources = RESOURCES
        self.lvl = resources.lvl_info
        self.fitness = 0.0
        self.is_key_collected = False
        self.is_complete = False
        self.is_dead = False

        self.agent = Agent()
        self.moves = [random.randint(0, 3) for _ in range(NUM_FRAMES)]
        self.enemy_manager = EnemyManager(self.lvl.enemies, self.lvl.spikes)

        self.num_key_steps = 0
        self.num_door_steps = 0

    @classmethod
    def with_moves(cls, moves):
        game = cls()
        game.moves = moves[:]
        return game

    @classmethod
    def clone_with_moves(cls, parent):
        return cls.with_moves(parent.moves)

    def get_current_agent_pos(self):
        return self.agent.pos

    def update(self, frame_count):
        if self.is_complete or self.is_dead:
            self.num_door_steps = NUM_FRAMES
            self.num_key_steps = NUM_FRAMES
            return

        self.num_door_steps += 1
        if not self.is_key_collected:
            self.num_key_steps += 1

        command = AgentCommand.from_int(self.moves[frame_count] if frame_count < len(self.moves) else 0)
        self.agent.update(command, self.is_key_collected)

        self.is_dead = self.enemy_manager.update(self.agent.pos)
        self.handle_key_collision()
        self.is_complete = self.check_player_at_door()

    def fitness_score(self, ff_key, ff_door):
        if self.is_complete:
            key_val = NUM_FRAMES - self.num_key_steps + 1.0
            door_val = NUM_FRAMES - self.num_door_steps + 1.0
            self.fitness = key_val * 20.0 + door_val * 20.0 + FF_WEIGHT_THRESHOLD * 2.0
        elif not self.is_key_collected:
            self.fitness = 1.0 / ff_key * 1000.0
        else:
            f_key = 10.0 + NUM_FRAMES / self.num_key_steps
            f_door = 1.0 / ff_door * 1000.0
            self.fitness = f_door + f_key
            if self.is_key_collected:
                self.fitness += 1000.0
        return self.fitness

    def update_manual(self, command):
        self.moves[0] = command.to_int()
        self.update(0)

    @staticmethod
    def crossover(first, second):
        split_point = random.randint(0, len(first.moves) - 1)
        new_moves = first.moves[:split_point] + second.moves[split_point:]

        for i in range(len(new_moves)):
            if random.random() < MUTATION_PROBABILITY * 0.001:
                new_moves[i] = random.randint(0, 3)

        return Game.with_moves(new_moves)

    def check_player_at_door(self):
        return self.agent.pos == self.lvl.door

    def handle_key_collision(self):
        if self.agent.pos == self.lvl.key:
            self.is_key_collected = True

    def draw(self, offset_x, offset_y):
        scale_factor = UNIT_FRAME_SIZE * FRAME_SCALE
        w = self.lvl.size[0] * scale_factor
        h = self.lvl.size[1] * scale_factor

        background_tint = (116, 242, 145) if self.is_complete else (255, 255, 255)
        pygame.draw.rect(pygame.display.get_surface(), background_tint, (offset_x, offset_y, w, h))

        if not self.is_key_collected:
            self._draw_texture(TEXTURES.key_texture, self.lvl.key, scale_factor, offset_x, offset_y)

        if not self.is_dead:
            self.agent.draw(scale_factor, offset_x, offset_y)

        self.enemy_manager.draw(scale_factor, offset_x, offset_y)

    @staticmethod
    def _draw_texture(texture, pos, scale_factor, offset_x, offset_y):
        screen = pygame.display.get_surface()
        rect = texture.get_rect()
        rect.topleft = (pos[0] * scale_factor + offset_x, pos[1] * scale_factor + offset_y)
        screen.blit(texture, rect)
