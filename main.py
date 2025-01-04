import math as m
import random as rd
from typing import Any
import pygame as pg
import numpy as np
import numpy.typing as npt

balls = 10
radius = 1
balls_positions: npt.NDArray[np.float64] = np.array(
    [[float(rd.randint(100, 700)), float(rd.randint(100, 500))] for _ in range(balls)],
    ndmin=2,
)
balls_velocities: npt.NDArray[np.float64] = np.array(
    [
        [rd.random() * rd.choice([1, -1]) * 2, rd.random() * rd.choice([1, -1]) * 2]
        for _ in range(balls)
    ],
    ndmin=2,
)

clock = pg.time.Clock()
screen = pg.display.set_mode((800, 600))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    screen.fill((0, 0, 0))
    gravity = [
        sum(
            [
                (1 / m.dist(p1, p2) ** 3 * (p2 - p1)) * 100
                for p2 in np.delete(balls_positions, np.where(balls_positions == p1), 0)
            ],
        )
        for p1 in balls_positions
    ]

    balls_velocities += gravity
    drag = -0.01 * balls_velocities
    balls_velocities += drag

    balls_positions += balls_velocities
    for i, pos in enumerate(balls_positions):
        # if pos[0] < 0 + radius or pos[0] > 800 - radius:
        #     balls_velocities[i][0] *= -1
        # if pos[1] < 0 + radius or pos[1] > 600 - radius:
        #     balls_velocities[i][1] *= -1
        pg.draw.circle(screen, (255, 255, 255), tuple(pos), radius)
    pg.display.flip()
    clock.tick(60)
