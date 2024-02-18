import random

def forca():
    palavras = ['abacate', 'abacaxi', 'acougue', 'pijama', 'maravilha']
    palavra_secreta = random.choice(palavras)
    letras_acertadas = ['_' for letra in palavra_secreta]
    acertou = False
    enforcou = False
    tentativas = 0
    erros = 0

    while (not acertou) and (not enforcou):
        print("\nPalavra secreta:", "".join(letras_acertadas))
        print("Tentativas:", tentativas)
        print("Erros:", erros)
        letra = input("Digite uma letra: ").lower()

        if len(letra) != 1:
            print("Digite apenas uma letra!")
        elif letra in palavra_secreta:
            for i in range(len(palavra_secreta)):
                if palavra_secreta[i] == letra:
                    letras_acertadas[i] = letra

            if "_" not in letras_acertadas:
                acertou = True
                print("\nParabéns! Você acertou a palavra secreta:", "".join(letras_acertadas))
        else:
            print("\nLetra incorreta! Tente novamente.")
            erros += 1
            tentativas += 1

            if erros == 7:
                enforcou = True
                print("\nQue pena! Você enforcou a forca. A palavra secreta era:", palavra_secreta) 

if __name__ == "__main__":
    forca()
