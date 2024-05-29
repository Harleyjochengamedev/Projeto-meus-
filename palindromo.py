class bgcolor:
    OK = '\033[92m' #VERDE
    WAR = '\033[93m' #AMARELO
    FAIL = '\033[91m' #VERMELHO
    RESET = '\033[0m' #RESET

def reverso(lista):
    esquerda = 0
    direita = len(lista) - 1
    while esquerda < direita:
        lista[direita], lista[esquerda] = lista[esquerda], lista[direita]
        esquerda = esquerda + 1
        direita-=1

lista = ['o','s','s','o']
listaNome = ['t','i','a','g','o']

reverso(lista)
reverso(listaNome)
print(bgcolor.OK + "Lista: " + bgcolor.RESET,end='')
print(lista)
print(bgcolor.FAIL + "Lista Nome: " + bgcolor.RESET)
print(listaNome)


  
