imposto = 0.27
valor = 5000
print(valor - (valor*imposto))
print("Valor real: {0}".format(valor - (valor*imposto)))

#imposto = float(input("Imposto? "))
#valor = int(input("Valor a ser tributado: "))
resultado = valor - (valor*imposto)
print(resultado)

if imposto < 0.2:
    print("Medio")
elif imposto <0.5:
    print("Alto")
else:
    print("Muito alto")

while imposto > 0.2:
    print("Alguma coisa") 
    print("Alguma coisa")
    break

#cnducbdu
lista = ['valor','imposto','alto','baixo']
print(lista)
print(lista[0:4])
print(lista[4:2])
print(lista[-2])    

lista1 = []
if lista1:
    print("")
else:
    print("Listas vazias são consideradas como falsos")

def enumerar_lista(lista):
    for i,objeto_lista in enumerate(lista):
        print(i,objeto_lista)

def soma(a,b):
    print(a+b)

def subtrair(a,b):
    return a-b 

soma(5,6)
enumerar_lista(lista)
res = subtrair(6,5)
print(res)

data_hoje = [2024, 1,21]

import turtle

lapis = turtle.Pen()
lapis.forward(100)
lapis.right(40)
lapis.forward(100)

tartaruga = turtle.Turtle()
tartaruga.shape("turtle")
tartaruga.color('gold')
tartaruga.forward(100)
tartaruga.back(250)
tartaruga.left(25)
tartaruga.fd(100)
tartaruga.setpos(250,180)
tartaruga.setpos(150,180)
tartaruga.setpos(350,180)
tartaruga.setpos(250,380)
tartaruga.setpos(250,480)
tartaruga.setpos(250,80)

print(tartaruga.pos())

tartaruga.setx(100)
tartaruga.sety(200)
tartaruga.home()

tartaruga.color('red')
tartaruga.circle(90)

tartaruga.penup()

for i in range(0,8):
    tartaruga.fd(100)
    tartaruga.lt(50)

tartaruga.pendown()

for i in range(0,15):
    tartaruga.fd(150)
    tartaruga.rt(25)


tartaruga.pencolor('black')
tartaruga.speed(5)
tartaruga.pensize(20)

for i in range(0,70):
    tartaruga.fd(100)
    tartaruga.left(60)
    tartaruga.back(20)

tartaruga.pencolor('pink')
tartaruga.speed(10)
tartaruga.pensize(10)

for i in range(0,70):
    tartaruga.fd(100)
    tartaruga.left(60)
    tartaruga.back(20)

tartaruga.pencolor('blue')
tartaruga.speed(8)
tartaruga.pensize(15)

for i in range(0,70):
    tartaruga.fd(100)
    tartaruga.left(60)
    tartaruga.back(20)
    if i % 5 == 0:
        tartaruga.stamp()

tartaruga.pencolor('silver')
tartaruga.speed(5)
tartaruga.stamp()
tartaruga.pensize(5)
fonte1 = ("Comic Sans",20,"bold")


tartaruga.write("O Tiago manda", True,"center",fonte1)
tartaruga.forward(50)
tartaruga.write("nem nele mesmo", True,"center",fonte1)
tartaruga.forward(50)

tartaruga.clear()

tartaruga.home()
tartaruga.begin_fill()
tartaruga.circle(100)
tartaruga.end_fill()

tela = turtle.Screen()
tela.bgcolor('grey')
