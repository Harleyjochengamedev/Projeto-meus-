#Associação é uma relação de muitos para muitos, são desacoplados
#ou idependentes.

class Pessoa:
    def __init__(self) -> None:
        self.lista_contatos = []
    def incluir_contatos(self,contato):
        self.lista_contatos.append(contato)

class Contato:
    def __init__(self) -> None:
        self.nome = ''
        self.telefone = ''
    def set_nome(self,nome):
        self.nome = nome
    def set_telefone(self,telefone):
        self.telefone = telefone

contato = Contato()
contato.set_nome("Ananias")
contato.set_telefone("3293-9390")

pessoa = Pessoa()
pessoa.incluir_contatos(contato)

#Agregação é a relação de 1 para muitos, onde não há dependencias

class Cliente(Pessoa):
    def __init__(self) -> None:
        super().__init__()
        self.lista_notas = []
    def inserir_notas(self, nota_fiscal):
        self.lista_notas.append(nota_fiscal)
        
class Nota_Fiscal():
    def __init__(self) -> None:
        self.lista_item = []
    def inserir_item(self,item):
        self.lista_item.append(item)

nota_fiscal = Nota_Fiscal()

cliente = Cliente()
cliente.inserir_notas(nota_fiscal)


#Composição é a relação de 1 para muitos, há dependências

class Item():
    def __init__(self,nome,preco) -> None:
        self.nome = nome
        self.preco = preco

    def insere_nome(self,nome):
        self.nome = nome
    def insere_preco(self,preco):
        self.preco = preco

item = Item("banana",4.89)

nota_fiscal.inserir_item(item)