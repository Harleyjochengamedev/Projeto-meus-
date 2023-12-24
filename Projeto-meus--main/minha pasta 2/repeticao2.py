start = True
while(start == True):
    entrada = str(input("Digite a ação: "))
    if(entrada == "buraco"):
        print("Pular!")
    elif(entrada == "diamante"):
        print("+1 Diamante")
    elif(entrada == "zombie"):
        print("Atacar")
    else:
        print("1 Passo!")
    