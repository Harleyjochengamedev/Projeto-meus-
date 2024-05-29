lista = [15,20,3,4,8]
# lista[n] + lista[n+1] = 7

def listaDois(numero,objetivo):
    hasher = {}
    for indice, i in enumerate(numero):
        if hasher.get(i) is not None:
            return[hasher.get(i),indice]
        hasher[objetivo-i] =indice

listaR = listaDois(lista,7)
print(listaR)