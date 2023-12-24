while True:
    nome = input("Digite o nome (maior que 3 caracteres): ")
    if len(nome) <= 3:
        print("Nome inválido. Deve ter mais de 3 caracteres.")
        continue

    idade = int(input("Digite a idade (entre 0 e 150): "))
    if idade < 0 or idade > 150:
        print("Idade inválida. Deve estar entre 0 e 150.")
        continue

    salario = float(input("Digite o salário (maior que zero): "))
    if salario <= 0:
        print("Salário inválido. Deve ser maior que zero.")
        continue

    sexo = input("Digite o sexo ('f' ou 'm'): ")
    if sexo not in ['f', 'm']:
        print("Sexo inválido. Deve ser 'f' ou 'm'.")
        continue

    estado_civil = input("Digite o estado civil ('s', 'c', 'v', 'd'): ")
    if estado_civil not in ['s', 'c', 'v', 'd']:
        print("Estado civil inválido. Deve ser 's', 'c', 'v' ou 'd'.")
        continue

    print("Informações válidas!")
    break
