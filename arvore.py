linhas = int(input("Qual é a altura da árvore? "))
espacos = linhas - 1
asteriscos = 1

for i in range(linhas):
    print(" " * espacos + "*" * asteriscos + " " * espacos)
    espacos -= 1
    asteriscos += 2

print(" " * (linhas - 1) + "*")
