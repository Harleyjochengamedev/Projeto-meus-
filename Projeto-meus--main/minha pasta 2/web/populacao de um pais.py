populacao_A = 80000
crescimento_A = 0.03
populacao_B = 200000
crescimento_B = 0.015

anos = 0

while populacao_A < populacao_B:
    anos += 1
    populacao_A = populacao_A + (populacao_A * crescimento_A)
    populacao_B = populacao_B + (populacao_B * crescimento_B)

print(f"São necessários {anos} anos para que a população do país A ultrapasse ou iguale a população do país B.")
