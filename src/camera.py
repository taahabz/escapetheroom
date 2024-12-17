import pygame
from pygame.math import Vector2

# Constants (equivalent to Rust's configs)
INITIAL_CAMERA_SCALE = 1.0

class MouseCam:
    def __init__(self, offset, scale):
        """
        Initialize the MouseCam.

        :param offset: Initial offset as a Vector2.
        :param scale: Initial scale.
        """
        self.offset = Vector2(offset)
        self.scale = scale

        self.last_mouse_pos = Vector2(0, 0)
        self.initial_offset = Vector2(offset)

    def get_cam(self, screen_size):
        """
        Get the current camera transformation.

        :param screen_size: Tuple (width, height) for the screen size.
        :return: A dictionary representing the camera state.
        """
        aspect = screen_size[0] / screen_size[1]
        return {
            "zoom": Vector2(self.scale, -self.scale * aspect),
            "offset": Vector2(self.offset.x, -self.offset.y),
            "target": Vector2(screen_size[0] / 2.0, screen_size[1] / 2.0),
            "rotation": 0.0,
        }

    def update(self, mouse_pos, should_offset, events, screen_size):
        """
        Update the camera based on input and events.

        :param mouse_pos: Current mouse position as a Vector2.
        :param should_offset: Boolean indicating if the camera offset should be updated.
        :param events: List of Pygame events.
        :param screen_size: Tuple (width, height) of the screen.
        """
        is_fast_zoom = pygame.key.get_pressed()[pygame.K_LCTRL]
        scale_factor = 1.5 if is_fast_zoom else 1.05

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # Middle mouse button resets the camera
                    self.offset = self.initial_offset
                    self.scale = INITIAL_CAMERA_SCALE
            elif event.type == pygame.MOUSEWHEEL:
                self.wheel_update(Vector2(mouse_pos), event.y, scale_factor)

        if pygame.mouse.get_pressed()[2]:  # Right mouse button for panning
            self.pan_update()

        if should_offset:
            self.offset += Vector2(mouse_pos) - self.last_mouse_pos

        self.last_mouse_pos = Vector2(mouse_pos)

        # This would set the camera in a rendering context.
        # For now, it simply provides the updated state.
        return self.get_cam(screen_size)

    def wheel_update(self, center, wheel_value, scale_factor):
        """
        Update the scale of the camera based on the mouse wheel.

        :param center: Center of zoom as a Vector2.
        :param wheel_value: Value of the mouse wheel.
        :param scale_factor: Factor by which to scale.
        """
        if wheel_value > 0:
            self.scale_mul(center, scale_factor)
        elif wheel_value < 0:
            self.scale_mul(center, 1.0 / scale_factor)

    def pan_update(self):
        """
        Update the camera offset based on mouse movement.
        """
        current_mouse_pos = Vector2(pygame.mouse.get_pos())
        mouse_delta = current_mouse_pos - self.last_mouse_pos
        self.last_mouse_pos = current_mouse_pos
        self.offset += mouse_delta

    def scale_mul(self, center, mul_to_scale):
        """
        Multiply the camera scale by a factor.

        :param center: Center of scaling as a Vector2.
        :param mul_to_scale: Multiplicative factor for the scale.
        """
        self.scale_new(center, self.scale * mul_to_scale)

    def scale_new(self, center, new_scale):
        """
        Set a new scale for the camera.

        :param center: Center of scaling as a Vector2.
        :param new_scale: New scale value.
        """
        self.offset = (self.offset - center) * (new_scale / self.scale) + center
        self.scale = new_scale

# Example usage:
# cam = MouseCam((0, 0), INITIAL_CAMERA_SCALE)
# while running:
#     events = pygame.event.get()
#     mouse_pos = pygame.mouse.get_pos()
#     cam.update(mouse_pos, should_offset=True, events=events, screen_size=(800, 600))
