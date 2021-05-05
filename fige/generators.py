import abc
import random
import uuid
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw
from tqdm import trange

import numpy as np


class BaseFigureGenerator(abc.ABC):
    OUTPUT_DIR = Path(__file__).parent.joinpath("data")
    FIGURE_NAME = None

    def get_filename(self, image):
        w, h = image.size
        return f"{self.FIGURE_NAME}_{w}x{h}_{uuid.uuid4().hex[:5]}.png"

    def save(self, image):
        image.save(self.OUTPUT_DIR.joinpath(self.get_filename(image)), "PNG")


class SquareGenerator(BaseFigureGenerator):
    FIGURE_NAME = "square"

    def __init__(
        self,
        base_size: np.array,
        rotation: Tuple[int] = (0, 360),
        scale: Tuple[float] = (0.1, 1.0),
        fill: Tuple[int] = (255, 255, 255)
    ):
        self._fill = fill
        self._scale = scale
        self._base_size = base_size
        self._rotation = rotation

    def get_rotation(self):
        return random.randint(*self._rotation)

    def get_scale(self):
        return random.uniform(*self._scale)

    def run(self, count: int = 1) -> None:
        for _ in trange(count):
            image = self._get_base_image()
            rotation = self.get_rotation()
            scale = self.get_scale()
            self.draw(image, rotation, scale)
            self.save(image)

    def _get_base_image(self, base_color=(255, 255, 255)):
        return Image.new("RGB", tuple(self._base_size), base_color)

    def draw(self, image, rotation, scale):
        draw = ImageDraw.Draw(image)
        draw.regular_polygon(
            (self._base_size / 2, min(self._base_size) / 2 * scale),
            n_sides=4,
            rotation=rotation,
            fill=self._fill,
            outline=(0, 0, 0),
        )


class CircleGenerator(BaseFigureGenerator):
    FIGURE_NAME = "circle"

    def __init__(
            self,
            base_size: np.array,
            scale: Tuple[float] = (0.05, 0.99),
            fill: Tuple[int] = (255, 255, 255)
    ):
        self._fill = fill
        self._scale = scale
        self._base_size = base_size

    def get_scale(self):
        return random.uniform(*self._scale)

    def run(self, count: int = 1) -> None:
        for _ in trange(count):
            image = self._get_base_image()
            scale = self.get_scale()
            self.draw(image, scale)
            self.save(image)

    def _get_base_image(self, base_color=(255, 255, 255)):
        return Image.new("RGB", tuple(self._base_size), base_color)

    def draw(self, image, scale):
        center_vec = self._base_size / 2
        first_point = center_vec * (1 - scale)
        second_point = center_vec * (1 + scale)
        draw = ImageDraw.Draw(image)
        print([first_point, second_point])
        draw.ellipse(
            [*first_point, *second_point],
            fill=self._fill,
            outline=(0, 0, 0),
        )


class TriangleGenerator(BaseFigureGenerator):
    FIGURE_NAME = "triangle"

    def __init__(
            self,
            base_size: np.array,
            scale: Tuple[float] = (0.05, 1),
            angle: Tuple[int] = (20, 120),
            fill: Tuple[int] = (255, 255, 255)
    ):
        self._angle = angle
        self._fill = fill
        self._scale = scale
        self._base_size = base_size

    def get_scale(self):
        return random.uniform(*self._scale)

    def run(self, count: int = 1) -> None:
        for _ in trange(count):
            image = self._get_base_image()
            scale = self.get_scale()
            self.draw(image, scale)
            self.save(image)

    def _get_base_image(self, base_color=(255, 255, 255)):
        return Image.new("RGB", tuple(self._base_size), base_color)

    def _get_angles(self):
        starting_angle = np.random.randint(0, 360)
        second_angle = starting_angle + np.random.uniform(*self._angle)
        third_angle = second_angle + np.random.uniform(*self._angle)
        return np.array([starting_angle, second_angle, third_angle])

    def get_points(self, radius, angles, center):
        x = np.cos(angles * np.pi / 180.) * radius + center[0]
        y = np.sin(angles * np.pi / 180.) * radius + center[1]
        return np.array((x, y)).T

    def draw(self, image, scale):
        radius = min(self._base_size) / 2 * scale
        center = self._base_size / 2
        angles = self._get_angles()
        points = self.get_points(radius, angles, center)
        draw = ImageDraw.Draw(image)
        draw.polygon(
            list(points.flatten()),
            fill=self._fill,
            outline=(0, 0, 0),
        )
        # draw.ellipse(((center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)), outline=0)
