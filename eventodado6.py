import random
import tkinter as tk

def lancar():
    resultado["text"] = str(random.randint(1,6))

tela = tk.Tk()
tela.columnconfigure(0,minsize=150)
tela.rowconfigure([0,1], minsize=50)

botao = tk.Button(text="Lançar o dado",command=lancar)
resultado = tk.Label()

botao.grid(row=0,column=0)
resultado.grid(row=1,column=0)

tela.mainloop()