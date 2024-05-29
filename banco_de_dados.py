import sqlite3
from typing import Any
valor_final = 0
class Compra:
    def __init__(self) -> None:
        self.data = ''
        self.valor = ''
        self.hora = ''
    def __getdata__(self) -> Any:
        return self.data
    def __getvalor__(self) -> Any:
        return self.valor
    def __gethora__(self) -> Any:
        return self.hora
    def __setdata__(self, data: str) -> None:
        self.data = data
    def __setvalor__(self, valor: str) -> None:
        self.valor = valor
    def __sethora__(self, hora: str) -> None:
        self.hora = hora
    def criar_banco(self):
        conexao = sqlite3.connect("sistema_compra.db")
        cursor = conexao.cursor()
        cursor.execute('create table tiago_gastos(data text,valor text,hora text)')
        conexao.commit()
        conexao.close()
    def inserir_compra(self):
        conexao = sqlite3.connect("sistema_compra.db")
        cursor = conexao.cursor()
        sql = "INSERT INTO tiago_gastos VALUES ("+self.data+","+self.valor+","+self.hora+")"
        cursor.execute(sql)
        conexao.commit()
        conexao.close()
    def selecionar_todos(self):
        conexao = sqlite3.connect("sistema_compra.db")
        cursor = conexao.cursor()
        sql = "SELECT * FROM tiago_gastos"
        cursor.execute(sql)
        conexao.commit()
        linhas = cursor.fetchall()
        for linha in linhas:
            print(linha)
        conexao.close()

compra = Compra()
compra.__setdata__(input("digite data da compra: "))
compra.__setvalor__(input("digite o valor: "))
compra.__sethora__(input("Digite a hora: "))

compra.inserir_compra()

compra.selecionar_todos()