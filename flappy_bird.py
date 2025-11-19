"""Simple Flappy Bird clone implemented with pygame.

Run `python flappy_bird.py` after installing dependencies from requirements.txt.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

import pygame

# Screen configuration
WIDTH = 400
HEIGHT = 600
FPS = 60

# Bird physics
GRAVITY = 0.35
FLAP_STRENGTH = -6.5
MAX_DROP_SPEED = 8

# Pipe configuration
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPAWN_INTERVAL = 1500  # milliseconds
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLUE = (33, 150, 243)
GREEN = (76, 175, 80)
YELLOW = (255, 235, 59)


@dataclass
class Bird:
    x: int
    y: int
    radius: int = 16
    velocity: float = 0.0

    def update(self) -> None:
        self.velocity = min(self.velocity + GRAVITY, MAX_DROP_SPEED)
        self.y += self.velocity

    def flap(self) -> None:
        self.velocity = FLAP_STRENGTH

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


@dataclass
class PipePair:
    x: int
    gap_y: int
    width: int = PIPE_WIDTH
    gap_height: int = PIPE_GAP
    passed: bool = False

    def update(self) -> None:
        self.x -= PIPE_SPEED

    @property
    def top_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, 0, self.width, self.gap_y - self.gap_height // 2)

    @property
    def bottom_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.gap_y + self.gap_height // 2, self.width, HEIGHT)

    def off_screen(self) -> bool:
        return self.x + self.width < 0


class FlappyBirdGame:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 32)
        self.reset()

    def reset(self) -> None:
        self.bird = Bird(x=WIDTH // 4, y=HEIGHT // 2)
        self.pipes: List[PipePair] = []
        self.spawn_pipe()
        self.score = 0
        self.running = True
        self.last_pipe_time = pygame.time.get_ticks()

    def spawn_pipe(self) -> None:
        gap_y = random.randint(150, HEIGHT - 150)
        self.pipes.append(PipePair(x=WIDTH + PIPE_WIDTH, gap_y=gap_y))

    def run(self) -> None:
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            if self.running:
                self.update()
            self.draw()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                if not self.running:
                    self.reset()
                self.bird.flap()

    def update(self) -> None:
        self.bird.update()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > PIPE_SPAWN_INTERVAL:
            self.spawn_pipe()
            self.last_pipe_time = current_time

        for pipe in list(self.pipes):
            pipe.update()
            if pipe.off_screen():
                self.pipes.remove(pipe)

            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1

            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.running = False

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= HEIGHT:
            self.running = False

    def draw(self) -> None:
        self.screen.fill(BLUE)
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, GREEN, pipe.top_rect)
            pygame.draw.rect(self.screen, GREEN, pipe.bottom_rect)
        pygame.draw.circle(self.screen, YELLOW, (self.bird.x, int(self.bird.y)), self.bird.radius)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if not self.running:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        text = self.font.render("Game Over!", True, WHITE)
        prompt = self.font.render("Press SPACE to retry", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(text, text_rect)
        self.screen.blit(prompt, prompt_rect)


def main() -> None:
    game = FlappyBirdGame()
    game.run()


if __name__ == "__main__":
    main()
