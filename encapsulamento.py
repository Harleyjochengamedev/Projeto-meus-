class DataTable:
    def __init__(self, name):
        self._name = name
        self._columns = []
        self._references = []
        self._referenced = []
        self._data = []

    def _get_name(self):
        print("Getter executado!")
        return self._name

    name = property(_get_name)

# Criando uma instância da classe DataTable
table = DataTable("Empreendimento")

# Acessando a propriedade 'name'
print(table.name)

