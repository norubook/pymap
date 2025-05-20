
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("キーイベント確認")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

log_text = ""

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            log_text = f"KEYDOWN: key={event.key}, unicode='{event.unicode}'"
            print(log_text)  # ← コンソールにも表示

    rendered = font.render(log_text, True, (255, 255, 255))
    screen.blit(rendered, (20, 120))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
