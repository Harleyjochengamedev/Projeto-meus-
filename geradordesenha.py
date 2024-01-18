# Importar o módulo random
import random

# Definir os caracteres possíveis para a senha
caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"

# Definir o tamanho da senha
tamanho = 10

# Gerar uma senha aleatória usando os caracteres e o tamanho
senha = "".join(random.choices(caracteres, k=tamanho))

# Mostrar a senha gerada
print("Sua senha é:", senha)