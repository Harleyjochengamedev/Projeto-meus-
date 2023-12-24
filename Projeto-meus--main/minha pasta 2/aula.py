import datetime

data_hoje = datetime.datetime.now()

anonasc = int(input("Digite o ano do seu nascimento: "))
mes_nascimento = int(input("Digite o mês do seu nascimento"))
dia_nascimento = int(input("Dia de nascimento"))



print(data_hoje.year() - anonasc)

print(data_hoje.month() - mes_nascimento)

print(data_hoje.day() - dia_nascimento)


# eita bagunça---
if (data_hoje.month() > mes_nascimento):
 print("Sua idade é: ",data_hoje.year() -anonasc)
elif (data_hoje.month() == mes_nascimento):
 if (data_hoje.day()< dia_nascimento):
  print("Sua idade é: ",data_hoje.year() -anonasc)
 if(data_hoje.day() > dia_nascimento):
  print("Sua idade é: ",data_hoje.year() -anonasc - 1)
 if (data_hoje.day() == dia_nascimento):
  print("Feliz aniversário Deus te abençoe e muitos anos de vida!")



 





