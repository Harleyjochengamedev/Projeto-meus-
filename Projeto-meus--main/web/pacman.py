import turtle
import random
# Adicionar a classe Labirinto aqui
class Labirinto:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.labirinto = [[' ' for _ in range(colunas)] for _ in range(linhas)]

    def adicionar_parede(self, linha, coluna):
        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            self.labirinto[linha][coluna] = '#'

    def remover_parede(self, linha, coluna):
        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            self.labirinto[linha][coluna] = ' '

    def eh_parede(self, linha, coluna):
        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            return self.labirinto[linha][coluna] == '#'
        return False

    def imprimir(self):
        for linha in self.labirinto:
            print(''.join(linha))
# Criar a janela do jogo
window = turtle.Screen()
window.title("PAC Man")
window.bgcolor("black")
window.setup(width=400, height=400)

# Variável para verificar se o jogo está em execução
running = True

# Criar o objeto PAC Man
pacman = turtle.Turtle()
pacman.shape("circle")
pacman.color("yellow")
pacman.penup()
pacman.speed(0)
pacman.goto(180, 180)
pacman.direction = "stop"

# Criar o objeto fantasma
ghost = turtle.Turtle()
ghost.shape("circle")
ghost.color("red")
ghost.penup()
ghost.speed(0)
ghost.goto(20, 20)
ghost.direction = random.choice(["up", "down", "left", "right"])

# Criar o objeto pontuação
score = turtle.Turtle()
score.shape("square")
score.color("white")
score.penup()
score.speed(0)
score.hideturtle()
score.goto(0, 180)
score.write("Pontuação: 0", align="center", font=("Arial", 20, "normal"))

# Variável para armazenar a pontuação
score_value = 0

# Funções para mover o PAC Man
def go_up():
    pacman.direction = "up"

def go_down():
    pacman.direction = "down"

def go_left():
    pacman.direction = "left"

def go_right():
    pacman.direction = "right"

def move():
    if pacman.direction == "up":
        y = pacman.ycor()
        pacman.sety(y + 20)
    if pacman.direction == "down":
        y = pacman.ycor()
        pacman.sety(y - 20)
    if pacman.direction == "left":
        x = pacman.xcor()
        pacman.setx(x - 20)
    if pacman.direction == "right":
        x = pacman.xcor()
        pacman.setx(x + 20)

# Funções para mover o fantasma
def move_ghost():
    if ghost.direction == "up":
        y = ghost.ycor()
        ghost.sety(y + 20)
    if ghost.direction == "down":
        y = ghost.ycor()
        ghost.sety(y - 20)
    if ghost.direction == "left":
        x = ghost.xcor()
        ghost.setx(x - 20)
    if ghost.direction == "right":
        x = ghost.xcor()
        ghost.setx(x + 20)

# Função para verificar a colisão entre o PAC Man e o fantasma
def check_collision():
    global score_value
    if pacman.distance(ghost) < 20:
        # Aumentar a pontuação
        score_value += 1
        score.clear()
        score.write(f"Pontuação: {score_value}", align="center", font=("Arial", 20, "normal"))
        # Mover o fantasma para uma posição aleatória
        x = random.randint(-180, 180)
        y = random.randint(-180, 180)
        ghost.goto(x, y)
        # Mudar a direção do fantasma
        ghost.direction = random.choice(["up", "down", "left", "right"])

# Função para verificar as bordas da janela
def check_border():
    global running
    # Verificar se o PAC Man saiu da janela
    if pacman.xcor() > 180 or pacman.xcor() < -180 or pacman.ycor() > 180 or pacman.ycor() < -180:
        # Parar o jogo
        pacman.direction = "stop"
        ghost.direction = "stop"
        running = False
        # Mostrar uma mensagem de fim de jogo
        game_over = turtle.Turtle()
        game_over.shape("square")
        game_over.color("white")
        game_over.penup()
        game_over.speed(0)
        game_over.hideturtle()
        game_over.write("Fim de jogo", align="center", font=("Arial", 30, "normal"))
    # Verificar se o fantasma saiu da janela
    if ghost.xcor() > 180 or ghost.xcor() < -180 or ghost.ycor() > 180 or ghost.ycor() < -180:
        # Mudar a direção do fantasma
        ghost.direction = random.choice(["up", "down", "left", "right"])

# Função para atualizar o jogo
def update():
    if running:
        move()
        move_ghost()
        check_collision()
        check_border()
        window.ontimer(update, 100)

# Associar as teclas do teclado com as funções de movimento
window.listen()
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")

# Iniciar o jogo
update()
turtle.done()
