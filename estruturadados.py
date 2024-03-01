lista_numero = [0,1,2,3,4,5,6,7,8,9]
lista_alfabeto_minusculo = ['a','b','c','d','e','f','g','h','i','j','l','m','n','o','p','q','r','s','u','v','x','z']

dicionario_entidades = {
    'instituição': []
}

entidades = dict()
entidades['Instituições'] = []
#adiciona no último
lista_numero.append(10)

#adiciona no penúltimo da lista
lista_numero.insert(-1,18)

#remover um elemento
lista_numero.remove(18)

#remove o primeiro elemento
lista_numero.pop()

#concatenação de listas
lista_numero.extend(lista_alfabeto_minusculo)

#reverter a lista
lista_numero.reverse()

#desordenando a lista
lista_numero = [9,1,2,3,4,5,6,7,8,0]

#ordenar por valor
lista_numero.sort()

#lista pega pelo índice
print(lista_numero.index(0))
print(lista_numero)


