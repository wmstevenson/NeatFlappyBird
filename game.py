import pygame
from bird import Bird
from pipe import Pipe

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

FONT = pygame.font.Font('freesansbold.ttf', 32)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()


def draw_window(window, bird, pipes, score):

    window.fill((0,0,0))

    bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    text = FONT.render(f"{score}", True, (255, 255, 255))
    text_rect = text.get_rect()

    text_rect.center = (WINDOW_WIDTH / 2, 50)

    window.blit(text, text_rect)

    pygame.display.update()



def main():
    bird = Bird(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    pipes = [Pipe(WINDOW_HEIGHT, WINDOW_WIDTH)]
    score = 0

    run = True

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()

        for pipe in pipes:
            pipe.move()

        

        if not pipe.passed and pipe.x + pipe.WIDTH < bird.x:
            pipe.passed = True
            score += 1


        bird_rect = bird.get_rect()

        for pipe in pipes:
            top_rect, bottom_rect = pipe.get_rects()

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                run = False

        if bird.y - bird.RADIUS <= 0 or bird.y + bird.RADIUS >= WINDOW_HEIGHT:
            run = False


        if pipes[-1].x < WINDOW_WIDTH - 400:
            pipes.append(Pipe(WINDOW_HEIGHT, WINDOW_WIDTH))

        pipes = [pipe for pipe in pipes if pipe.x + pipe.WIDTH > 0]

        draw_window(window, bird, pipes, score)

    pygame.quit()


main()