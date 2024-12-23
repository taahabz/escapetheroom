import pygame
import time
from resources import init_resources
from editor import Editor
from simulation import Simulation, SimulationStats
from pygame.locals import *

# Configuration constants
WINDOW_TITLE = "Escape"
WINDOW_WIDTH = 800  # Replace with WINDOW_WIDTH from your constants
WINDOW_HEIGHT = 600  # Replace with WINDOW_HEIGHT from your constants
IS_FULL_SCREEN = False  # Replace with IS_FULL_SCREEN from your constants
WINDOW_BACKGROUND_COLOR = (0, 0, 0, 255)  # Replace with actual RGBA tuple

# Pygame initialization
pygame.init()

# Set up Pygame window
flags = pygame.FULLSCREEN if IS_FULL_SCREEN else 0
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
pygame.display.set_caption(WINDOW_TITLE)

# Initialize resources (after the Pygame window is created)

clock = pygame.time.Clock()

def main():
    """
    The main function that initializes resources, simulation, and editor, and then runs the simulation loop.
    """
    init_resources()  # This will initialize RESOURCES and TEXTURES

    # Create instances of Editor and Simulation
    editor = Editor()
    simulation = Simulation()
    simulation.initialize_population()
    # Create a SimulationStats instance to hold simulation statistics
    stats = SimulationStats()

    running = True
    while running:
        # Clear the screen before drawing new frame
        screen.fill(WINDOW_BACKGROUND_COLOR[:3])

        # Handle frame skipping if enabled in the editor settings
        if editor.settings.is_frame_skip:
            for _ in range(10):
                stats = simulation.update(editor) or stats

        # Update the simulation and draw it
        stats = simulation.update(editor) or stats
        simulation.draw(editor, screen)

        # Update and draw editor if necessary
        editor.update()
        editor.draw(stats, screen)

        # Slow mode handling if enabled in the editor settings
        if editor.settings.slow_mode:
            time.sleep(0.2)

        # Restart the simulation if the restart flag is set
        if editor.settings.is_restart:
            editor.settings.is_restart = False
            simulation = Simulation()  # Reset the simulation to start a new one

        # Check for exit events (close window or press ESC)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Handle draw toggle if the editor's settings disable drawing
        if not editor.settings.is_draw:
            for _ in range(100):
                stats = simulation.update(editor) or stats

        # Update the display with the new frame and control the frame rate
        pygame.display.flip()
        clock.tick(60)  # Adjust the frame rate as needed (60 FPS here)

    pygame.quit()  # Close Pygame gracefully when the loop exits

if __name__ == "__main__":
    main()  # Run the main function to start the simulation
