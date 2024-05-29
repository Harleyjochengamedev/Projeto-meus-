class Veiculo:
    def __init__(self,modelo,tipo, km) -> None:
        self.modelo = modelo
        self.tipo = tipo
        self.km = km

class Carro(Veiculo):
    def __init__(self, modelo, tipo, km,porta) -> None:
        Veiculo.__init__(self,modelo,tipo,km)
        self.porta = porta
        self.rodas = 4
    def exibeCarro(self)->None:
        print(self.modelo,self.tipo,self.rodas,self.porta)

#Veiculo é a superclasse ou pai ou mãe e Carro é subclasse filho
#Fazer veículos diferentes: Moto e outro

carro_ulisses = Carro("Modelo 1","Tipo 1",30000,4)

carro_ulisses.exibeCarro()
    