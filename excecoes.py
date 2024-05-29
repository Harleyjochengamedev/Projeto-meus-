from cores import *
try:
    numerador = int(input(cores.amarelo+"Digite o numerador: "+cores.resetar))
    denominador = int(input(cores.cor1+"Digite o denominador: "+ cores.resetar))
    resultado = numerador/denominador
    lista = []
    lista.append(resultado)
    print(lista[0])
except KeyboardInterrupt as ki:
    print(cores.vermelho+"Você quis interromper Ctrl + C, tudo bem, volte sempre!"+cores.resetar)
except NameError as ne:
    print(ne.__cause__)
except ValueError as ve:
    print(ve.__cause__)
    print(cores.vermelho + "numerador e denominador devem ser do tipo inteiro ou ponto flutuante"+cores.resetar)
except ZeroDivisionError as zde:
    print(zde.__cause__)
    print(cores.vermelho + "O denominador não pode ser zero, pois não existe no conjunto dos números reais a divisão"+ cores.resetar)
except IndexError as ie:
    print(ie.__cause__)
    print(cores.vermelho + "Fora dos limites da lista!"+ cores.resetar)
except TypeError as te:
    print(cores.vermelho+ f'o erro foi {te.__cause__}' + cores.resetar)
else:
    print(cores.cor2+f'O resultado foi: {resultado: .2f}'+cores.resetar)
finally:
    print(cores.cor1+"É sempre bom estar com você"+ cores.resetar)    