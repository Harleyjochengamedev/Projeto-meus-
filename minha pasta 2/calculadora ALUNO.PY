from datetime import datetime

def calcular_idade():
    ano_atual = datetime.now().year
    ano_nascimento = int(input("Digite o ano do seu nascimento: "))
    idade = ano_atual - ano_nascimento
    return idade

idade = calcular_idade()
print(f"Sua idade é {idade} anos.")

