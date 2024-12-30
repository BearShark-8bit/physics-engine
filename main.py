from dataclasses import dataclass
import math
from typing import List, Self
import pygame


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_deg(cls, deg, hypot) -> Self:
        r = math.radians(deg)
        x, y = round(math.cos(r) * hypot, 2), round(math.sin(r) * hypot, 2)
        return cls(x, y)

    def __add__(self, other: Self):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: int):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    @property
    def hypot(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __matmul__(self, other: Self):
        return self.x * other.x + self.y * other.y

    def angle_clockwise(self, other: Self):
        return round(
            (
                math.degrees(
                    math.acos((self @ other) / (abs(self.hypot) * abs(other.hypot)))
                )
                if self.y > 0
                else 360
                - math.degrees(
                    math.acos((self @ other) / (abs(self.hypot) * abs(other.hypot)))
                )
            ),
            3,
        )

    def angle(self, other: Self):
        return round(
            math.degrees(
                math.acos((self @ other) / (abs(self.hypot) * abs(other.hypot)))
            ),
            3,
        )

    def rotated(self, deg):
        return self.from_deg(self.angle_clockwise(Vector(1, 0)) - deg, self.hypot)

    @property
    def tuple(self):
        return (self.x, self.y)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


class Decceleration(Vector): ...


class ExpressionVector(Vector): ...


@dataclass
class Ball:
    pos: Vector
    rad: int
    forces: List[Vector | Decceleration] | None = None

    @property
    def rect(self):
        return pygame.Rect(*self.pos.tuple, self.rad - 1, self.rad - 1)

    def update(self):
        if self.forces:
            self.pos = sum([self.pos, sum(self.forces)])

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, (255, 255, 255), self.pos.tuple, self.rad)


screen = pygame.display.set_mode((500, 500))
ball = Ball(Vector(250, 250), 10, [Vector(0.01, 0)])

while True:
    screen.fill((0, 0, 0))
    ball.update()
    ball.draw(screen)
    pygame.display.update()
