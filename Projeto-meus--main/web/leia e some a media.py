numeros = []
for i in range(5):
    numero = float(input("Digite um número: "))
    numeros.append(numero)

soma = sum(numeros)
media = soma / len(numeros)

print(f"A soma dos números digitados é: {soma}")
print(f"A média dos números digitados é: {media}")
