class Pessoa:
    def __init__(self, idade, nome) -> None:
        self.nome = nome
        self.idade = idade
    def apresentacao(self)->None:
        print(self.idade, " anos, meu nome é ", self.nome)

class Aluno(Pessoa):
    def __init__(self,idade,nome,serie)->None:
        Pessoa.__init__(self, idade, nome)
        self.serie = serie
    def getSerie(self)->str:
        return self.serie
    
douglas = Aluno(16,"Douglas","2 ano médio")
douglas.apresentacao()
serie_douglas = douglas.getSerie()
print(serie_douglas)