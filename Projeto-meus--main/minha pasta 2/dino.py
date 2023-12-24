import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configura o tamanho da janela
window_size = (800, 600)
window = pygame.display.set_mode(window_size)

# Configura a cor do Dino e do obstáculo
dino_color = (0, 255, 128)  # verde
obstacle_color = (255, 225, 0)  # amarelo

# Configura a posição inicial e o tamanho do Dino
dino_x = 50
dino_y = window_size[1] - 50
dino_size = 50

# Configura a velocidade do Dino
dino_speed = 0.5  # Velocidade ajustada

# Configura a gravidade
gravity = 0.25  # Gravidade ajustada

# Configura a posição inicial e o tamanho do obstáculo
obstacle_x = window_size[0]
obstacle_y = window_size[1] - 25
obstacle_width = 25
obstacle_height = 50

# Configura a velocidade do obstáculo
obstacle_speed = 1

# Configura a pontuação
score = 0

# Configura o estado do jogo
game_over = False

# Loop principal do jogo
while True:
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    score = 0
                    obstacle_x = window_size[0]
                    dino_y = window_size[1] - 50
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Verifica se a tecla de espaço foi pressionada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino_speed = -7.5  # Força do pulo ajustada

        # Aplica a gravidade
        dino_speed += gravity
        dino_y += dino_speed

        # Verifica se o Dino está no chão
        if dino_y > window_size[1] - 50:
            dino_y = window_size[1] - 50
            dino_speed = 0

        # Move o obstáculo
        obstacle_x -= obstacle_speed

        # Verifica se o obstáculo saiu da tela
        if obstacle_x < 0:
            obstacle_x = window_size[0]
            score += 1

        # Verifica se o Dino colidiu com o obstáculo
        if dino_x < obstacle_x + obstacle_width and dino_x + dino_size > obstacle_x and dino_y < obstacle_y + obstacle_height and dino_y + dino_size > obstacle_y:
            game_over = True

        # Preenche a tela com preto
        window.fill((0, 0, 0))

        # Desenha o Dino
        pygame.draw.rect(window, dino_color, pygame.Rect(dino_x, dino_y, dino_size, dino_size))

        # Desenha o obstáculo
        pygame.draw.rect(window, obstacle_color, pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Exibe a pontuação
        font = pygame.font.Font(None, 36)
        text = font.render("Pontuação: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 10))

    # Exibe a tela de fim de jogo
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Fim de jogo! Pressione Enter para jogar novamente.", 1, (255, 255, 255))
        window.blit(text, (window_size[0] // 2 - text.get_width() // 2, window_size[1] // 2 - text.get_height() // 2))

    # Atualiza a tela
    pygame.display.flip()
