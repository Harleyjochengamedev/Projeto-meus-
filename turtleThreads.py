import turtle
import time
import threading

janela = turtle.Screen()
janela.setup(0.9,0.9)
janela.title("Simulação de threads")

kamehameha = turtle.Turtle()
kamehameha.penup()
kamehameha.shape("circle")
kamehameha.color(0,0,0.35)
kamehameha.setposition(-580,0)
kamehameha.stamp()

galikiho = turtle.Turtle()
galikiho.penup()
galikiho.shape("circle")
galikiho.color(0,0,0.8)
galikiho.setposition(580,0)
galikiho.stamp()

def moverKamehameha():
    kamehameha.pendown()
    for i in range(80):
        kamehameha.setx(kamehameha.xcor() + 10)
        print("Goku")
        print(i)
        time.sleep(1)


def moverGalikiho():
    galikiho.pendown()
    for i in range(58):
        galikiho.setx(galikiho.xcor()-10)
        print("Vegeta")
        print(i)
        time.sleep(1)

goku = threading.Thread(target=moverKamehameha)
vegeta = threading.Thread(target=moverGalikiho)

goku.start()
vegeta.start()

turtle.done()