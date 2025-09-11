import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 3
BIRD_SIZE = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.size = BIRD_SIZE

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(
            screen, YELLOW, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(
            screen, BLACK, (int(self.x), int(self.y)), self.size, 2)
        # Simple eye
        pygame.draw.circle(
            screen, BLACK, (int(self.x + 8), int(self.y - 8)), 5)
        pygame.draw.circle(
            screen, WHITE, (int(self.x + 10), int(self.y - 10)), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size,
                           self.size * 2, self.size * 2)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN,
                         (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK,
                         (self.x, 0, PIPE_WIDTH, self.height), 3)

        # Bottom pipe
        pygame.draw.rect(screen, GREEN,
                         (self.x, self.height + PIPE_GAP, PIPE_WIDTH,
                          SCREEN_HEIGHT - self.height - PIPE_GAP))
        pygame.draw.rect(screen, BLACK,
                         (self.x, self.height + PIPE_GAP, PIPE_WIDTH,
                          SCREEN_HEIGHT - self.height - PIPE_GAP), 3)

        # Pipe caps
        pygame.draw.rect(screen, GREEN,
                         (self.x - 5, self.height - 20, PIPE_WIDTH + 10, 20))
        pygame.draw.rect(screen, BLACK,
                         (self.x - 5, self.height - 20, PIPE_WIDTH + 10, 20), 3)

        pygame.draw.rect(screen, GREEN,
                         (self.x - 5, self.height + PIPE_GAP, PIPE_WIDTH + 10, 20))
        pygame.draw.rect(screen, BLACK,
                         (self.x - 5, self.height + PIPE_GAP, PIPE_WIDTH + 10, 20), 3)

    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH,
                                  SCREEN_HEIGHT - self.height - PIPE_GAP)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0


class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.game_started = False

    def spawn_pipe(self):
        if not self.pipes or self.pipes[-1].x < SCREEN_WIDTH - 200:
            self.pipes.append(Pipe(SCREEN_WIDTH))

    def update_pipes(self):
        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
            elif not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1

    def check_collisions(self):
        # Check ground and ceiling collision
        if self.bird.y + self.bird.size > SCREEN_HEIGHT or self.bird.y - self.bird.size < 0:
            self.game_over = True

        # Check pipe collisions
        for pipe in self.pipes:
            if pipe.collides_with(self.bird):
                self.game_over = True

    def draw_background(self):
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            color_intensity = 255 - int((y / SCREEN_HEIGHT) * 50)
            color = (135, 206, max(235 - int((y / SCREEN_HEIGHT) * 100), 100))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        # Ground
        pygame.draw.rect(self.screen, (139, 69, 19),
                         (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.rect(self.screen, BLACK,
                         (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50), 3)

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def draw_start_screen(self):
        title_text = self.big_font.render("Flappy Bird", True, BLACK)
        start_text = self.font.render("Press SPACE to start", True, BLACK)
        controls_text = self.font.render("Press SPACE to flap", True, BLACK)

        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        start_rect = start_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        controls_rect = controls_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(controls_text, controls_rect)

    def draw_game_over(self):
        game_over_text = self.big_font.render("Game Over!", True, RED)
        score_text = self.font.render(
            f"Final Score: {self.score}", True, BLACK)
        restart_text = self.font.render("Press R to restart", True, BLACK)
        quit_text = self.font.render("Press Q to quit", True, BLACK)

        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        score_rect = score_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.game_started = True
                    elif not self.game_over:
                        self.bird.jump()

                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

                elif event.key == pygame.K_q and self.game_over:
                    return False

        return True

    def run(self):
        running = True

        while running:
            running = self.handle_events()

            if self.game_started and not self.game_over:
                self.bird.update()
                self.spawn_pipe()
                self.update_pipes()
                self.check_collisions()

            # Drawing
            self.draw_background()

            if self.game_started:
                # Draw pipes
                for pipe in self.pipes:
                    pipe.draw(self.screen)

                # Draw bird
                self.bird.draw(self.screen)

                # Draw score
                self.draw_score()

                if self.game_over:
                    self.draw_game_over()
            else:
                # Draw bird in start position
                self.bird.draw(self.screen)
                self.draw_start_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
