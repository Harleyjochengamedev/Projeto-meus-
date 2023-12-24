'''
turma = ["Ana Clara", "Ana Jhuly", "Anna Clara", "Cauê"]


for i in range(0,5):
    print("Andei um passo")
    if(i == 4):
        print("Ataquei o zombie")
print("FIM!")

'''
attack = False
while(attack == False):
    entrada = input("Digite a etapa do jogo: (buraco|diamante|nada)")
    if(entrada == "buraco"):
        print("Pulo!!")
    elif(entrada == "diamante"):
        print("+1 Diamante")
    elif(entrada == "nada"):
        print("Ande...")
    else:
        attack = True

print("Ataquei o Zombie")










