while True:
    populacao_A = int(input("Digite a população inicial do país A: "))
    if populacao_A <= 0:
        print("População inválida. Deve ser maior que zero.")
        continue

    crescimento_A = float(input("Digite a taxa de crescimento do país A (em decimal): "))
    if crescimento_A <= 0:
        print("Taxa de crescimento inválida. Deve ser maior que zero.")
        continue

    populacao_B = int(input("Digite a população inicial do país B: "))
    if populacao_B <= 0:
        print("População inválida. Deve ser maior que zero.")
        continue

    crescimento_B = float(input("Digite a taxa de crescimento do país B (em decimal): "))
    if crescimento_B <= 0:
        print("Taxa de crescimento inválida. Deve ser maior que zero.")
        continue

    anos = 0

    while populacao_A < populacao_B:
        anos += 1
        populacao_A = populacao_A + (populacao_A * crescimento_A)
        populacao_B = populacao_B + (populacao_B * crescimento_B)

    print(f"São necessários {anos} anos para que a população do país A ultrapasse ou iguale a população do país B.")

    repetir = input("Deseja repetir a operação? (s/n): ")
    if repetir.lower() != 's':
        break
