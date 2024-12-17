import pygame
import os
import json

class Resources:
    def __init__(self, level_map_path, level_background_sprite_path, tileset_path):
        print(f"Loading map from: {level_map_path}")  # Debugging line
        self.lvl_map = self.load_map(level_map_path)
        self.lvl_background_sprite = self.load_texture(level_background_sprite_path)
        self.lvl_info = self.parse_level_info()
        print(f"Level info initialized: {self.lvl_info}")  # Debugging line

    @staticmethod
    def load_texture(path):
        """Loads a texture from a given path."""
        try:
            texture = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(texture, texture.get_rect().size)
        except pygame.error as e:
            raise RuntimeError(f"Failed to load texture: {path}, {e}")

    @staticmethod
    def load_map(path):
        """Loads a JSON map file from the specified path."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Map file not found at path: {path}")
        with open(path, 'r') as file:
            return json.load(file)

    def parse_level_info(self):
        """Parses level info from the map JSON."""
        try:
            width = self.lvl_map.get("width", None)
            height = self.lvl_map.get("height", None)
            tile_width = self.lvl_map.get("tilewidth", None)
            tile_height = self.lvl_map.get("tileheight", None)

            if not all([width, height, tile_width, tile_height]):
                raise ValueError("Incomplete map dimensions in lvl_map")

            print(f"Parsed map dimensions: width={width}, height={height}, "
                  f"tile_width={tile_width}, tile_height={tile_height}")  # Debugging line

            return {
                "width": width,
                "height": height,
                "tile_width": tile_width,
                "tile_height": tile_height,
            }
        except Exception as e:
            raise RuntimeError(f"Failed to parse level info: {e}")

# Global resources and textures
RESOURCES = None
TEXTURES = None

def init_resources():
    global RESOURCES, TEXTURES
    print("Initializing resources...")  # Debugging line

    # Adjust paths to be relative to the script's location
    level_map_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'lvl1.json')
    level_background_sprite_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'lvl1.png')
    tileset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'tileset.png')

    RESOURCES = Resources(level_map_path, level_background_sprite_path, tileset_path)
    TEXTURES = Textures()

    print("Resources initialized successfully.")
    print("Textures initialized successfully.")

class Textures:
    def __init__(self):
        self.agent_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'agent.png'))
        self.agent_sleep1_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'agent_sleeping.png'))
        self.agent_sleep2_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'agent_sleeping_2.png'))
        self.agent_sleep3_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'agent_sleeping_3.png'))
        self.key_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'key.png'))
        self.crab_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'crab.png'))
        self.small_spike_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'small_spike.png'))
        self.large_spike_texture = self.get_texture(os.path.join(os.path.dirname(__file__), '..', 'assets', 'large_spike.png'))

    @staticmethod
    def get_texture(path):
        """Loads a texture from a given path."""
        try:
            texture = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(texture, texture.get_rect().size)
        except pygame.error as e:
            raise RuntimeError(f"Failed to load texture: {path}, {e}")
