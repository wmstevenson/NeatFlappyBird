import os
import pygame
import neat
import pickle

from bird import Bird
from pipe import Pipe

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

FONT = pygame.font.Font("freesansbold.ttf", 32)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()


def draw_window(window, birds_list, pipes, score):
    window.fill((0, 0, 0))

    for bird in birds_list:
        bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    text = FONT.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 50))
    window.blit(text, text_rect)

    pygame.display.update()


def get_next_pipe(bird, pipes):
    for pipe in pipes:
        if pipe.x + pipe.WIDTH > bird.x:
            return pipe

    return pipes[0]


def main(genomes, config):

    neural_networks_list = []
    birds_list = []
    genomes_list = []

    for genome_id, genome in genomes:

        genome.fitness = 0

        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)

        neural_networks_list.append(neural_network)
        birds_list.append(Bird(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        genomes_list.append(genome)

    pipes = [Pipe(WINDOW_HEIGHT, WINDOW_WIDTH)]
    score = 0

    run = True

    while len(birds_list) > 0:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for x, bird in enumerate(birds_list):
            genomes_list[x].fitness += 0.1

            next_pipe = get_next_pipe(bird, pipes)

            next_pipe.color = (255, 0, 0)

            

            output = neural_networks_list[x].activate(
                (
                    bird.y,
                    bird.velocity_y,
                    next_pipe.x - bird.x,
                    next_pipe.top_pipe_bottom,
                    next_pipe.bottom_pipe_top,
                )
            )

            if output[0] > 0.5:
                bird.flap()

            bird.move()

        for pipe in pipes:
            pipe.move()

            if not pipe.passed and pipe.x + pipe.WIDTH < birds_list[0].x:
                pipe.passed = True
                score += 1

                for genome in genomes_list:
                    genome.fitness += 5
            
            if pipe.passed:
                pipe.color = (0, 200, 0)

        for x, bird in enumerate(birds_list):
            bird_rect = bird.get_rect()

            if bird.y - bird.RADIUS <= 0 or bird.y + bird.RADIUS >= WINDOW_HEIGHT:
                genomes_list[x].fitness -= 1
                neural_networks_list.pop(x)
                birds_list.pop(x)
                genomes_list.pop(x)

            for pipe in pipes:
                top_rect, bottom_rect = pipe.get_rects()

                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(
                    bottom_rect
                ):
                    genomes_list[x].fitness -= 1
                    neural_networks_list.pop(x)
                    birds_list.pop(x)
                    genomes_list.pop(x)

        if pipes[-1].x < WINDOW_WIDTH - 400:
            pipes.append(Pipe(WINDOW_HEIGHT, WINDOW_WIDTH))

        pipes = [pipe for pipe in pipes if pipe.x + pipe.WIDTH > 0]

        if score >= 100:
            break

        draw_window(window, birds_list, pipes, score)


def run_neat(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 25)

    with open("best_genome.pkl", "wb") as file:
        pickle.dump(winner, file)

        print("Saved final genome with fitness:", winner.fitness)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)
