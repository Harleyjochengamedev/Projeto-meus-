import tkinter as tk
from classes import Consulta,Agendar_Exame,Resultado_Exame
import tkinter.ttk as tkk

def gerando_consulta():
    consulta = Consulta()
    consulta.projetar()

def agendar_exame():
    agenda_exame = Agendar_Exame()
    agenda_exame.projetar()

def resultado_exame():
    resultado = Resultado_Exame()
    resultado.set_arquivo()
    resultado.get_arquivo()
    resultado.fechar_arquivo_leitura()
    resultado.fechar_arquivo_escrita()
    resultado.projetar()

#Widgets: Label, Button, Entry, Text, Frame
tela_principal = tk.Tk()

frame1 = tk.Frame(master=tela_principal,height=100)
frame1.pack(fill=tk.X)

boas_vindas = tk.Label(master=frame1,text="Seja bem vindo ao sistema Medicina",foreground='red',background='white',width=50,height=5)            

botao_consulta = tk.Button(master=frame1,text="AGENDAR CONSULTA",fg='white',bg='blue', width=35,height=5, command=gerando_consulta)

botao_agendar_exame = tk.Button(master=frame1,text="AGENDAR EXAME",fg='white',bg='black', width=35,height=5, command=agendar_exame)

botao_resultado = tk.Button(master=frame1,text="RESULTADO DE EXAMES",fg='white',bg='orange', width=35,height=5, command=resultado_exame)

botao_retorno = tk.Button(master=frame1,text="RETORNO",fg='white',bg='green' , width=35,height=5, command=gerando_consulta)

boas_vindas.pack()
botao_consulta.pack()
botao_agendar_exame.pack()
botao_resultado.pack()
botao_retorno.pack()
tela_principal.mainloop()