import math
from typing import List, Tuple

from pygame import Surface, draw, transform

class EnemyKind:
    """Represents the type of enemy: Spike or Crab."""

    def __init__(self, kind: str, value: float = 0.0):
        self.kind = kind  # "Spike" or "Crab"
        self.value = value  # Angle for Spike, Direction (bool) for Crab

class GameItem:
    """Game item structure with position and value."""

    def __init__(self, pos: Tuple[int, int], value: int):
        self.pos = pos
        self.value = value

class Enemy:
    """Represents a single enemy in the game."""

    def __init__(self, pos: Tuple[int, int], kind: EnemyKind, item: GameItem):
        self.pos = pos
        self.kind = kind
        self.item = item

    def update(self, agent_pos: Tuple[int, int], walls_layer) -> bool:
        """Updates the enemy's position and checks for collisions with the agent."""
        agent_x, agent_y = agent_pos

        if self.kind.kind == "Crab":
            direction = self.kind.value

            if self.item.value == 88:  # Vertical movement
                new_y = self.pos[1] + 1 if direction else self.pos[1] - 1
                if walls_layer[self.pos[0]][new_y]:
                    self.kind.value = not direction
                    new_y = self.pos[1] - 2 if direction else self.pos[1] + 2
                self.pos = (self.pos[0], new_y)
            else:  # Horizontal movement
                new_x = self.pos[0] - 1 if direction else self.pos[0] + 1
                if walls_layer[new_x][self.pos[1]]:
                    self.kind.value = not direction
                    new_x = self.pos[0] + 2 if direction else self.pos[0] - 2
                self.pos = (new_x, self.pos[1])

        elif self.kind.kind == "Spike":
            self.kind.value = (self.kind.value + 10.0) % 360.0

        # Check collision with agent
        return self.pos == (agent_x, agent_y)

    def draw(self, surface: Surface, textures: dict, scale_factor: float, offset_x: float, offset_y: float):
        """Renders the enemy on the screen."""
        if self.kind.kind == "Spike":
            texture_key = {
                101: "small_spike_texture",
                104: "large_spike_texture"
            }.get(self.item.value, None)
        else:
            texture_key = "crab_texture"

        if not texture_key:
            return  # Blank spike, do not render

        texture = textures[texture_key]
        render_scale = 2.0 if texture_key == "large_spike_texture" else 1.0

        rotation = 0.0
        if self.kind.kind == "Spike":
            rotation = math.radians(self.kind.value)
        elif self.kind.kind == "Crab":
            if self.item.value == 88:
                rotation = math.pi if self.kind.value else 0.0
            else:
                rotation = math.pi + math.pi / 2.0 if self.kind.value else math.pi / 2.0

        transformed_texture = transform.rotozoom(texture, -math.degrees(rotation), render_scale * scale_factor)
        surface.blit(transformed_texture, (
            self.pos[0] * scale_factor + offset_x,
            self.pos[1] * scale_factor + offset_y
        ))

class EnemyManager:
    """Manages all enemies and spikes in the game."""

    def __init__(self, enemies: List[GameItem], spikes: List[GameItem]):
        self.enemies = [Enemy(e.pos, EnemyKind("Crab", False), e) for e in enemies]
        self.spikes = [Enemy(s.pos, EnemyKind("Spike", 0.0), s) for s in spikes]

    def update(self, agent_pos: Tuple[int, int], walls_layer) -> bool:
        """Updates all enemies and checks for collisions with the agent."""
        for enemy in self.enemies:
            if enemy.update(agent_pos, walls_layer):
                return True

        for spike in self.spikes:
            if spike.update(agent_pos, walls_layer):
                return True

        return False

    def draw(self, surface: Surface, textures: dict, scale_factor: float, offset_x: float, offset_y: float):
        """Renders all enemies and spikes on the screen."""
        for enemy in self.enemies:
            enemy.draw(surface, textures, scale_factor, offset_x, offset_y)

        for spike in self.spikes:
            spike.draw(surface, textures, scale_factor, offset_x, offset_y)
