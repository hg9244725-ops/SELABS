
import math


class Target:
    def __init__(self, x, y, base_radius=40, min_radius=12, lifespan_frames=90):
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.min_radius = min_radius
        self.lifespan_frames = lifespan_frames
        self.age = 0

    def update(self):
        self.age += 1

    def expired(self):
        return self.age >= self.lifespan_frames

    def visual_radius(self):
        # Calculate the current radius as the target shrinks over time.
        t = min(1.0, self.age / self.lifespan_frames)
        return self.base_radius - (
            self.base_radius - self.min_radius
        ) * t

    def contains_point(self, x, y):
        # Only register a hit inside the currently visible target.
        # The collision radius now matches the shrinking visual radius.
        return math.hypot(self.x - x, self.y - y) <= self.visual_radius()
