import pygame
from pygame.locals import *

class Settings:
    def __init__(self):
        self.is_pause = False
        self.is_draw = True
        self.is_restart = False
        self.is_frame_skip = False
        self.is_random_ai = False
        self.is_show_egui = False
        self.is_ai_enabled = True
        self.is_show_multiple = False
        self.slow_mode = False
class MouseCam:
    def __init__(self, initial_position, scale):
        self.position = pygame.Vector2(initial_position)
        self.scale = scale

    def update(self, mouse_position, dragging):
        # Placeholder for actual mouse camera logic
        pass

def mouse_position_local():
    return pygame.mouse.get_pos()
class MouseCam:
    def __init__(self, initial_position, scale):
        self.position = pygame.Vector2(initial_position)
        self.scale = scale

        pass

def mouse_position_local():
    return pygame.mouse.get_pos()

class Editor:
    def __init__(self):
        self.settings = Settings()
        self.mouse_cam = MouseCam((0.25, 0.04), INITIAL_CAMERA_SCALE)
        # Camera update
        8*8

    def update(self):
        # Camera update


        self.mouse_cam.update(mouse_position_local(), False)

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.settings.is_pause = not self.settings.is_pause
        if keys[K_TAB]:
            self.settings.is_show_egui = not self.settings.is_show_egui
        if keys[K_r]:
            self.settings.is_restart = True
        if keys[K_BACKSPACE]:
            self.settings.slow_mode = not self.settings.slow_mode
        if keys[K_BACKSLASH]:
            self.settings.is_ai_enabled = not self.settings.is_ai_enabled
        if keys[K_RSHIFT]:
            self.settings.is_frame_skip = not self.settings.is_frame_skip

    def draw(self, stats):
        if not self.settings.is_show_egui:
            return

        # Draw UI components (basic implementation, you can customize this further)
        font = pygame.font.Font(None, 24)

        def draw_text(surface, text, position, color=(255, 255, 255)):
            text_surface = font.render(text, True, color)
            surface.blit(text_surface, position)

        screen = pygame.display.get_surface()
        ui_background = pygame.Surface((220, 240), pygame.SRCALPHA)
        ui_background.fill((30, 30, 30, 220))
        screen.blit(ui_background, (20, screen.get_height() - 280))

        y_offset = screen.get_height() - 280 + 10
        draw_text(screen, f"FPS: {int(pygame.time.Clock().get_fps())}", (30, y_offset))
        y_offset += 30
        draw_text(screen, f"Frame: {stats['frame_count']}", (30, y_offset))
        y_offset += 30
        draw_text(screen, f"Gen: {stats['generation_count']}", (30, y_offset))
        y_offset += 40

        options = [
            ("Draw", self.settings.is_draw),
            ("Slow Mode", self.settings.slow_mode),
            ("Show Multi", self.settings.is_show_multiple),
            ("Enable AI", self.settings.is_ai_enabled),
            ("Frame skip", self.settings.is_frame_skip),
        ]

        for label, value in options:#sdfadsada
            draw_text(screen, f"{label}: {'On' if value else 'Off'}", (30, y_offset))
            y_offset += 30

        controls = [
            ("Pause", self.settings.is_pause),
            ("Restart", self.settings.is_restart),
        ]
        for label, value in controls:
            draw_text(screen, f"{label}: {'On' if value else 'Off'}", (30, y_offset))
            y_offset += 30

INITIAL_CAMERA_SCALE = 1.0

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Editor")
    clock = pygame.time.Clock()

    editor = Editor()
    stats = {"frame_count": 0, "generation_count": 0}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        editor.update()

        stats["frame_count"] += 1

        screen.fill((0, 0, 0))
        editor.draw(stats)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
