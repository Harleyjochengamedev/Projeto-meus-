import tkinter as tk
import os

class Consulta:
    def __init__(self) -> None:
        self.tela_consulta = tk.Tk()
        self.rotulo_data = tk.Label(master=self.tela_consulta,text="Digite a data",font=("Arial",25))
        self.data = tk.Entry(master=self.tela_consulta,width=40)
        self.rotulo_horario = tk.Label(master=self.tela_consulta,text="Digite o horario")
        self.horario = tk.Entry(master=self.tela_consulta,width=40)
        self.rotulo_cpf = tk.Label(master=self.tela_consulta,text="Digite o seu cpf:")
        self.cpf = tk.Entry(master=self.tela_consulta,width=40)
        self.botao_enviar = tk.Button(master=self.tela_consulta,width=30,text="Agendar Consulta", command=self.guardar)
    def projetar(self):
        self.rotulo_cpf.pack()
        self.cpf.pack()
        self.rotulo_data.pack()
        self.data.pack()
        self.rotulo_horario.pack()
        self.horario.pack()
        self.botao_enviar.pack()
        self.tela_consulta.mainloop()
    def guardar(self):
        arquivo = open("guardarConsulta.txt","a")
        arquivo.write(f"CPF: {self.cpf.get()}")
        arquivo.write(f" Data: {self.data.get()}")
        arquivo.write(f" Horario: {self.horario.get()}")
        arquivo.write("\n")
        arquivo.close()

class Agendar_Exame:
    def __init__(self) -> None:
        self.tela_agendar_exame = tk.Tk()
        self.rotulo_data = tk.Label(master=self.tela_agendar_exame,text="Digite a data")
        self.data = tk.Entry(master=self.tela_agendar_exame,width=30)
        self.rotulo_horario = tk.Label(master=self.tela_agendar_exame,text="Digite o horario")
        self.horario = tk.Entry(master=self.tela_agendar_exame,width=30)
        self.tipo_exame = tk.Label(master=self.tela_agendar_exame,text="Digite o tipo de exame")
        self.exame = tk.Entry(master=self.tela_agendar_exame,width=30)
        self.botao_enviar = tk.Button(master=self.tela_agendar_exame,width=30,text="Agendar Exame")
    def projetar(self):
        self.rotulo_data.pack()
        self.data.pack()
        self.rotulo_horario.pack()
        self.horario.pack()
        self.tipo_exame.pack()
        self.exame.pack()
        self.botao_enviar.pack()
        self.tela_agendar_exame.mainloop()

class Resultado_Exame:
    def __init__(self) -> None:
        self.tela_resultado = tk.Tk()
        self.rotulo_resultado = tk.Label(master=self.tela_resultado,text="")
        self.arquivo_leitura = open("resultado.txt","r")
        self.arquivo_escrita = open("resultado.txt","a")
    def get_arquivo(self):
        self.rotulo_resultado["text"] = str(self.arquivo_leitura.read())
    def set_arquivo(self):
        self.arquivo_escrita.write("Exame tals, do fulano de tals")
    def fechar_arquivo_leitura(self):
        self.arquivo_leitura.close()
    def fechar_arquivo_escrita(self):
        self.arquivo_escrita.close()
    def projetar(self):
        self.rotulo_resultado.pack()
        self.tela_resultado.mainloop()