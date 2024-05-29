import threading
def tarefa1():
    numero = 0
    while numero < 9:
        print("Tarefa1")
        numero+= 1

def tarefa2():
    numero = 0
    while numero < 8:
        print("Tarefa2")
        numero+= 1

threading.Thread(target=tarefa1).start()
tarefa2()      