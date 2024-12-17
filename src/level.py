class GameItem:
    def __init__(self, pos, value):
        self.pos = pos  # Tuple (x, y)
        self.value = value  # Item value (e.g., tile ID)


class LevelInfo:
    def __init__(self, map_data):
        self.size = self.parse_size(map_data)
        self.key = self.get_one_item(map_data, "layer_keys")
        self.door = self.get_one_item(map_data, "layer_door")
        self.agent = self.get_one_item(map_data, "layer_player")
        self.spikes = self.get_all_items(map_data, "layer_spikes")
        self.enemies = self.get_all_items(map_data, "layer_enemies")

    @staticmethod
    def parse_size(map_data):
        walls_layer = map_data["layers"].get("layer_walls")
        if not walls_layer:
            raise ValueError("No walls layer found in the map")
        return walls_layer["width"], walls_layer["height"]

    @staticmethod
    def get_one_item(map_data, layer_name):
        layer = map_data["layers"].get(layer_name)
        if not layer:
            raise ValueError(f"Layer {layer_name} not found in the map")

        for i in range(layer["width"]):
            for j in range(layer["height"]):
                if layer["tiles"][j][i]:
                    return (i, j)
        raise ValueError(f"No item found in layer {layer_name}")

    @staticmethod
    def get_all_items(map_data, layer_name):
        items = []
        layer = map_data["layers"].get(layer_name)
        if not layer:
            return items

        for i in range(layer["width"]):
            for j in range(layer["height"]):
                tile = layer["tiles"][j][i]
                if tile:
                    items.append(GameItem((i, j), tile))
        return items


# Example usage
# This assumes map_data is loaded from a JSON file that mirrors the structure of the original Map object.
# Example: map_data = json.load(open("path_to_map.json"))
