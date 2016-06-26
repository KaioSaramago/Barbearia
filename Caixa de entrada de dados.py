from Tkinter import *
from functools import partial
import sqlite3
import tkMessageBox
import ttk

#variaveis
janela = Tk()
logado = "nenhum"

con1 = sqlite3.connect('serv.db')
c1 = con1.cursor()
con2 = sqlite3.connect('barbeiros.db')
c2 = con2.cursor()
con3 = sqlite3.connect('socios.db')
c3 = con3.cursor()

#c1.execute('CREATE TABLE serv(barbeiro text, servico text,preco int )')
#c2.execute('CREATE TABLE barbeiros(barbeiro text, porcentagem int,senha text)')
#c3.execute('CREATE TABLE socios(socio text, senha text)')
"""c2.execute("INSERT INTO barbeiros VALUES ('jorge', '30','123')")
c3.execute("INSERT INTO socios VALUES ('ana','123')")
con2.commit()
con3.commit()"""
def validardados():
    global logado
    log=login.get()
    sen=senha.get()
    c2.execute('SELECT * FROM barbeiros WHERE barbeiro="%s" AND senha="%s" '%(log,sen))
    if c2.fetchone() is not None:
        k = Label(janela,width = 25, text="Usuario Encontrado")
        k.grid(row=6, column=1)
        tkMessageBox.showinfo("Barbeiro(a) encontrado", "As opcoes de barbeiro(a) estao liberadas")
        logado=login.get()
        janela.title("%s - Barbeiro(a)" % login.get())
        login.delete(0, END)
        senha.delete(0, END)
    else:
        c3.execute('SELECT * FROM socios WHERE socio="%s" AND senha="%s" '%(log,sen))
        if c3.fetchone() is not None:
            k = Label(janela,width = 25, text="Usuario Encontrado")
            k.grid(row=6, column=1)
            tkMessageBox.showinfo("Socio encontrado", "As opcoes de socios estao liberadas")
            logado = login.get()
            janela.title("%s - Socio(a)" %login.get())
            login.delete(0, END)
            senha.delete(0, END)
        else:
            k = Label(janela,width = 25, text="usuario nao cadastrado",fg="red")
            k.grid(row=6,column=1)
            tkMessageBox.showinfo("Usuario nao encontrado","E necessario logar-se para ter acesso as opcoes")
            login.delete(0, END)
            senha.delete(0, END)
            logado = "nenhum"
def varstates():
   print("Corte: %d,\nCorte especial: %d, \nBarba:%d,\nBarba especial: %d" % (var1.get(), var2.get(),var3.get(),var4.get()))
def calcularpreco():
    x=0
    if (var1.get()==1):
        x=10 #preco do corte normal
    if (var2.get() == 1):
        x = x + 15 #preco do corte especial
    if (var3.get() == 1):
        x = x + 10  # preco da barba
    if (var4.get() == 1):
        x = x + 15  # preco da barba especial
    return x
def mostrarpreco():
    en1.delete(0,END)
    en1.insert(0, "%s" % calcularpreco())
def salvarnobanco():
    if (logado == "nenhum"):
        tkMessageBox.showinfo("Login nao detectado", "Para salvar informacoes no banco de dados e necessario estar logado")
    else:
        c1.execute("INSERT INTO serv VALUES ('%s','%s','%d')" % (logado, servicos(), calcularpreco()))
        print servicos()
        print calcularpreco()
        print logado
        con1.commit()
        tkMessageBox.showinfo("Sucesso", "Informacoes salvas no banco de dados\n\nPrestador de servico: %s\nServico(s)prestados: %s\nPreco: %d"% (logado, servicos(), calcularpreco()))
def servicos():
    x = " "
    if (var1.get() == 1):
            x = "Corte,"
    if (var2.get() == 1):
            x = x + " Corte especial,"
    if (var3.get() == 1):
            x = x + " Barba,"
    if (var4.get() == 1):
            x = x + " Barba especial,"
    return x

#variaveis do registro de pedido
var1 = IntVar()
Checkbutton(janela, text="Corte", variable=var1).grid(row=5, column=3,sticky=W)
var2 = IntVar()
Checkbutton(janela, text="Corte especial", variable=var2).grid(row=6, column=3,sticky=W)
var3 = IntVar()
Checkbutton(janela, text="Barba", variable=var3).grid(row=7, column=3,sticky=W)
var4 = IntVar()
Checkbutton(janela, text="Barba especial", variable=var4).grid(row=8, column=3,sticky=W)

#Entry
en1 = Entry(janela, width=25)
en1.grid(row=4,column=4)
login = Entry(janela, width = 25)
login.grid(row=2,column=1)
senha = Entry(janela, width = 25)
senha.grid(row=4,column=1)

#botoes
bt9 = Button(janela, width=25, text="Salvar no bando de dados",command=salvarnobanco).grid(row=12, column=3)
Button(janela, width = 25,text = "Cadastrar Barbeiro").grid(row = 4, column = 6)#FALTA FAZER
Button(janela, width = 25,text = "Cadastrar Socio").grid(row = 5, column = 6)#FALTA FAZER
Button(janela, width = 25,text = "Remover Barbeiro").grid(row = 6, column = 6)#FALTA FAZER
Button(janela, width = 25,text = "Remover Socio").grid(row = 7, column = 6)#FALTA FAZER
Button(janela, width = 25,text = "Gerar relatorio em txt").grid(row = 8, column = 6)#FALTA FAZER
Button(janela, width = 25,text = "Calcular preco",command =mostrarpreco).grid(row = 9, column = 3)
Button(janela, width = 25,text = "Validar dados",command =validardados).grid(row = 5, column = 1)

#labels
ttk.Separator(janela,orient=HORIZONTAL).grid(row=1, columnspan=5,column = 5,sticky="ew")
ttk.Separator(janela,orient=HORIZONTAL).grid(row=1, columnspan=5,column = 2,sticky="ew")
Label(janela, text= "login").grid(row=1,column=1)
Label(janela, text= "senha").grid(row=3,column=1)
Label(janela, text= "Menu Barbeiro:").grid(row=1,column=3)
Label(janela, text= "Menu Socio:").grid(row=1,column=6)
Label(janela, text= "Registrar servico:").grid(row=3,column=3)
Label(janela, text= "Preco:").grid(row=3,column=4)

janela.geometry("1000x500+100+100")
janela.title("Pagina inicial")
janela.mainloop()
