while True:
    usuario = input("Digite o nome do usuário: ")
    senha = input("Digite a senha: ")
    if usuario != senha:
        print("Usuário e senha aceitos!")
        break
    else:
        print("Erro: A senha não pode ser igual ao nome do usuário. Por favor, tente novamente.")
