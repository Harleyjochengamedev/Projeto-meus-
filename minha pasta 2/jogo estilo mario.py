import pygame
from pygame.locals import *

pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))

# Configurações do jogador
LARGURA_JOGADOR = 60
ALTURA_JOGADOR = 80
JOGADOR_COR = (0, 0, 255)
jogador = pygame.Rect(LARGURA / 2, ALTURA / 2, LARGURA_JOGADOR, ALTURA_JOGADOR)

# Configurações do jogo
FPS = 60
VEL = 5

# Loop principal do jogo
rodando = True
while rodando:
    # Limita a taxa de quadros (frames)
    pygame.time.Clock().tick(FPS)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == QUIT:
            rodando = False

    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[K_UP] or teclas[K_w]:
        jogador.move_ip(0, -VEL)
    if teclas[K_DOWN] or teclas[K_s]:
        jogador.move_ip(0, VEL)
    if teclas[K_LEFT] or teclas[K_a]:
        jogador.move_ip(-VEL, 0)
    if teclas[K_RIGHT] or teclas[K_d]:
        jogador.move_ip(VEL, 0)

    # Mantém o jogador na tela
    if jogador.left < 0:
        jogador.left = 0
    if jogador.right > LARGURA:
        jogador.right = LARGURA
    if jogador.top <= 0:
        jogador.top = 0
    if jogador.bottom >= ALTURA:
        jogador.bottom = ALTURA

    # Renderização
    TELA.fill((0, 0, 0))
    pygame.draw.rect(TELA, JOGADOR_COR, jogador)

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o game
pygame.quit()
