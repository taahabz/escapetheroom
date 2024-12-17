from population import Population
from configs import NUM_FRAMES
from configs import UNIT_FRAME_SIZE, FRAME_SCALE, MUTATION_PROBABILITY
from resources import init_resources  # Import the init_resources function



class Simulation:
    def __init__(self):
        self.population = None  # Delay initialization
        self.frame_count = 0
        self.generation_count = 1

    def initialize_population(self):
        # Now `RESOURCES` is guaranteed to be initialized
        self.population = Population(
            num_games=10,
            pop_retention_rate=0.5,
            pop_expo_percentage=0.3,
            num_games_in_row=3,
        )

    def update(self, editor):
        """
        Update the simulation state.

        :param editor: Editor instance to check settings.
        :return: SimulationStats instance if not paused, otherwise None.
        """
        if editor.settings.is_pause:
            return None

        self.population.update(self.frame_count, editor)
        self.frame_count += 1

        if self.frame_count >= NUM_FRAMES and editor.settings.is_ai_enabled:
            self.start_new_generation(not editor.settings.is_random_ai)

        return SimulationStats(self.frame_count, self.generation_count)

    def start_new_generation(self, is_selection):
        """
        Start a new generation of the population.

        :param is_selection: Boolean indicating whether to perform selection or reset population.
        """
        if is_selection:
            self.population.selection()
        else:
            # Re-initialize population with the same parameters if not performing selection
            self.population = Population(num_games=10, 
                                         pop_retention_rate=0.5, 
                                         pop_expo_percentage=0.3, 
                                         num_games_in_row=3)

        self.frame_count = 0
        self.generation_count += 1

    def draw(self, editor):
        """
        Draw the current state of the simulation.

        :param editor: Editor instance to check if drawing is enabled.
        """
        if not editor.settings.is_draw:
            return

        self.population.draw(editor)

class SimulationStats:
    def __init__(self, frame_count=1, generation_count=1):
        """
        Initialize simulation statistics.

        :param frame_count: Current frame count.
        :param generation_count: Current generation count.
        """
        self.frame_count = frame_count
        self.generation_count = generation_count
