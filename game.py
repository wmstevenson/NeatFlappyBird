import os
import pygame
import neat
import pickle

from bird import Bird
from pipe import Pipe

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

FONT = pygame.font.Font("freesansbold.ttf", 32)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()


def draw_window(window, bird, ai_bird, ai_alive, pipes, score):
    window.fill((0, 0, 0))


    if ai_alive:
        ai_bird.draw(window)

    bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    text = FONT.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 50))
    window.blit(text, text_rect)

    pygame.display.update()


def collision(bird, pipes):
    if bird.y - bird.RADIUS <= 0 or bird.y + bird.RADIUS >= WINDOW_HEIGHT:
        return True

    bird_rect = bird.get_rect()

    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True

    return False


def get_next_pipe(bird, pipes):
    for pipe in pipes:
        if pipe.x + pipe.WIDTH > bird.x:
            return pipe

    return pipes[0]


def load_ai(config_path, genome_path):
    with open(genome_path, "rb") as file:
        genome = pickle.load(file)

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    neural_network = neat.nn.FeedForwardNetwork.create(genome, config)

    return neural_network


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    genome_path = os.path.join(local_dir, "best_genome.pkl")

    neural_network = load_ai(config_path, genome_path)

    bird = Bird(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    ai_bird = Bird(WINDOW_WIDTH / 2 - 30, WINDOW_HEIGHT / 2, color=(255, 0, 255))

    pipes = [Pipe(WINDOW_HEIGHT, WINDOW_WIDTH)]
    score = 0

    player_alive = True
    ai_alive = True

    while player_alive:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player_alive = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        if ai_alive:
            next_pipe = get_next_pipe(ai_bird, pipes)

            output = neural_network.activate(
                (
                    ai_bird.y,
                    ai_bird.velocity_y,
                    next_pipe.x - ai_bird.x,
                    next_pipe.top_pipe_bottom,
                    next_pipe.bottom_pipe_top,
                )
            )

            if output[0] > 0.5:
                ai_bird.flap()

        bird.move()

        if ai_alive:
            ai_bird.move()

        for pipe in pipes:
            pipe.move()

            if not pipe.passed and pipe.x + pipe.WIDTH < bird.x:
                pipe.passed = True
                score += 1

        if collision(bird, pipes):
            player_alive = False

        if ai_alive and collision(ai_bird, pipes):
            ai_alive = False

        if pipes[-1].x < WINDOW_WIDTH - 400:
            pipes.append(Pipe(WINDOW_HEIGHT, WINDOW_WIDTH))

        pipes = [pipe for pipe in pipes if pipe.x + pipe.WIDTH > 0]

        draw_window(window, bird, ai_bird, ai_alive, pipes, score)

    pygame.quit()


if __name__ == "__main__":
    main()
