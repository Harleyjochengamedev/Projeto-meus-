class Moradia:
    def __init__(self, area, endereco):
        self.area = area
        self.endereco = endereco

class Casa:
    def __init__(self, moradia):
        self.moradia = moradia

class Parede:
    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura

class Telhado:
    def __init__(self, area_externa, area_interna, tipo_telha):
        self.area_externa = area_externa
        self.area_interna = area_interna
        self.tipo_telha = tipo_telha

class Espelho:
    def __init__(self, tipo_vidro):
        self.tipo_vidro = tipo_vidro

class Acabamento:
    def __init__(self, tipo):
        self.tipo = tipo
class Casa:
    def __init__(self, moradia):
        self.moradia = moradia
        self.paredes = []
        self.telhado = None
        self.espelho_corredor = None
        self.parede_banheiro = None
        self.parede_cozinha = None
        self.parede_quarto = None

class Moradia:
    def __init__(self, area, endereco):
        self.area = area
        self.endereco = endereco
        self.casa = None

class Parede:
    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura
        self.casa = None

class Telhado:
    def __init__(self, area_externa, area_interna, tipo_telha):
        self.area_externa = area_externa
        self.area_interna = area_interna
        self.tipo_telha = tipo_telha
        self.casa = None

class Espelho:
    def __init__(self, tipo_vidro):
        self.tipo_vidro = tipo_vidro
        self.casa = None

class Acabamento:
    def __init__(self, tipo):
        self.tipo = tipo
        self.paredes = []
# Criar uma moradia
moradia = Moradia(120.0, "Rua das Flores, 123")

# Criar uma casa
casa = Casa(moradia)

# Criar paredes
parede_cozinha = Parede(2.5, 3.0)
parede_banheiro = Parede(2.0, 2.5)
parede_quarto = Parede(2.5, 3.0)

# Adicionar paredes à casa
casa.paredes.append(parede_cozinha)
casa.paredes.append(parede_banheiro)
casa.paredes.append(parede_quarto)

# Criar telhado
telhado = Telhado(40.0, 30.0, "cerâmica")

# Adicionar telhado à casa
casa.telhado = telhado

# Criar espelho
espelho_corredor = Espelho("bisotado")

# Adicionar espelho à casa
casa.espelho_corredor = espelho_corredor

# Criar acabamento
acabamento = Acabamento("pintura")

# Adicionar acabamento às paredes
acabamento.paredes.append(parede_cozinha)
acabamento.paredes.append(parede_banheiro)
acabamento.paredes.append(parede_quarto)
