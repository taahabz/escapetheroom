import random
import pygame
from collections import defaultdict
from game import Game  # Assuming Game is implemented elsewhere
from agent import AgentCommand
from configs import UNIT_FRAME_SIZE, FRAME_SCALE
from resources import RESOURCES, init_resources

from ff import FF

class FFInfo:
    def __init__(self):
        if RESOURCES is None or RESOURCES.lvl_info is None:
            raise RuntimeError("RESOURCES or lvl_info is not initialized properly.")
        self.key = FF(RESOURCES.lvl_info["key"], RESOURCES.lvl_info["size"]).solve()
        self.door = FF(RESOURCES.lvl_info["door"], RESOURCES.lvl_info["size"]).solve()

class Population:
    def __init__(self, num_games, pop_retention_rate, pop_expo_percentage, num_games_in_row):
        self.ff_info = FFInfo()
        self.games = [Game() for _ in range(num_games)]
        self.num_games = num_games
        self.pop_retention_rate = pop_retention_rate
        self.pop_expo_percentage = pop_expo_percentage
        self.num_games_in_row = num_games_in_row

    def update(self, frame_count, editor):
        # User input applies only to the first game
        self.handle_user_input()

        if not editor.settings['is_ai_enabled']:
            return

        for game in self.games:
            game.update(frame_count)

    def selection(self):
        gene_pool = self.calc_fitness()
        new_games = []

        num_retained = int(self.num_games * (self.pop_retention_rate / 100))
        num_expo = int(self.num_games * (self.pop_expo_percentage / 100))
        num_children = self.num_games - num_retained - num_expo

        for _ in range(num_children):
            first = random.choices(self.games, weights=gene_pool)[0]
            second = random.choices(self.games, weights=gene_pool)[0]
            new_game = Game.crossover(first, second)
            new_games.append(new_game)

        # Retain the best games from the current generation
        self.games.sort(key=lambda g: g.fitness, reverse=True)
        retained_agents = [Game.clone_with_moves(game) for game in self.games[:num_retained]]

        # Exploration agents
        exploration_agents = [Game() for _ in range(num_expo)]

        self.games = retained_agents + exploration_agents + new_games

    def calc_fitness(self):
        max_fitness = 0.0
        weights = []

        for game in self.games:
            agent_pos = game.get_current_agent_pos()
            ff_key = self.ff_info.key.get(agent_pos, 0)
            ff_door = self.ff_info.door.get(agent_pos, 0)
            fitness = game.fitness(ff_key, ff_door)
            max_fitness = max(max_fitness, fitness)
            weights.append(fitness)

        if max_fitness > 0:
            weights = [weight / max_fitness * 100.0 for weight in weights]

        return weights

    def handle_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.games[0].update_manual(AgentCommand.TOP)
        elif keys[pygame.K_a]:
            self.games[0].update_manual(AgentCommand.LEFT)
        elif keys[pygame.K_s]:
            self.games[0].update_manual(AgentCommand.BOTTOM)
        elif keys[pygame.K_d]:
            self.games[0].update_manual(AgentCommand.RIGHT)

    def draw(self, editor):
        if not editor.settings['is_show_multiple']:
            self.games[0].draw(0, 0)
            return

        offset_x = 0
        offset_y = 0
        grid_padding = 40
        game_width, game_height = self.games[0].lvl.size
        game_width *= UNIT_FRAME_SIZE * FRAME_SCALE
        game_height *= UNIT_FRAME_SIZE * FRAME_SCALE

        for game in self.games:
            game.draw(offset_x, offset_y)
            offset_x += game_width + grid_padding

            if offset_x >= game_width * self.num_games_in_row:
                offset_y += game_height + grid_padding
                offset_x = 0
