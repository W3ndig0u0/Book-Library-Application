import pygame
import os
import gameplay

pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800
FONT = pygame.font.SysFont("Arial", 60)
SMALL_FONT = pygame.font.SysFont("Arial", 24)
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BIRD_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird1.png"))
)
BASE_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
]

pygame.display.set_caption("Flappy Bird AI Trainer")
pygame.display.set_icon(BIRD_IMG)


def draw_menu(win):
    win.blit(BG_IMG, (0, 0))
    win.blit(BASE_IMGS[0], (0, 730))

    title_text = FONT.render("Flappy Bird", True, (255, 255, 255))
    win.blit(title_text, (WIN_WIDTH // 2 - title_text.get_width() // 2, 100))

    play_btn_rect = pygame.Rect(WIN_WIDTH // 2 - 75, WIN_HEIGHT // 2 + 20, 150, 70)
    pygame.draw.rect(win, (255, 255, 255), play_btn_rect)
    play_text = SMALL_FONT.render("Play", True, (0, 0, 0))
    win.blit(
        play_text,
        (
            play_btn_rect.centerx - play_text.get_width() // 2,
            play_btn_rect.centery - play_text.get_height() // 2,
        ),
    )

    settings_btn_rect = pygame.Rect(WIN_WIDTH // 2 - 75, WIN_HEIGHT // 2 + 115, 150, 70)
    pygame.draw.rect(win, (255, 255, 255), settings_btn_rect)
    settings_text = SMALL_FONT.render("Settings", True, (0, 0, 0))
    win.blit(
        settings_text,
        (
            settings_btn_rect.centerx - settings_text.get_width() // 2,
            settings_btn_rect.centery - settings_text.get_height() // 2,
        ),
    )

    pygame.display.update()


def main_menu():
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                play_btn_rect = pygame.Rect(
                    WIN_WIDTH // 2 - 75, WIN_HEIGHT // 2 + 20, 150, 70
                )
                settings_btn_rect = pygame.Rect(
                    WIN_WIDTH // 2 - 75, WIN_HEIGHT // 2 + 115, 150, 70
                )

                if play_btn_rect.collidepoint(mouse_pos):
                    print("Play button clicked!")
                    gameplay.play()
                elif settings_btn_rect.collidepoint(mouse_pos):
                    print("Settings button clicked!")

        draw_menu(win)


if __name__ == "__main__":
    main_menu()
