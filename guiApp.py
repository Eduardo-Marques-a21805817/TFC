from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from tkinter import filedialog
#import tensorflow as tf 
import sqlite3
import mysql.connector



root = Tk()
root.title("TFC")
root.geometry("600x600")

listaDeColunas = []

#função para criar a connexão á DB
def connectToDB():
	DBendpoint = input.get()
	DBUsername = inputUser.get()
	DBPassword = inputPassword.get()
	DBName = inputDBName.get()

	if (DBendpoint == "DB endpoint" and DBName == "DB name" and DBUsername == "Username" and DBPassword == "Password"):
		messagebox.showinfo(title="Error", message="Could not Connect to database")


	DBConn = mysql.connector.connect(host=DBendpoint,user=DBUsername,password=DBPassword,db=DBName)




	if(DBConn.is_connected()==False):
		messagebox.showinfo(title="Error",message="Could not Connect to database")
	else:
		messagebox.showinfo(title="Error",message="Could Connect to database")

		cursor = DBConn.cursor()
		cursor.execute("Show tables;")
		listaTemp =cursor.fetchall()

		#print(DBConn)
		drop= OptionMenu(root,clicado,listaTemp)
		drop.grid(row=3,column=0,sticky="W")
		#for x in listaTemp:
			#drop.insert(x)


#função que verifica se houve conexão á DB
#def isThereDB():
	#print("things")

#caixa de texto para receber o endpoint da DB
textEnd = Label(root,text="DB Endpoint")
textEnd.grid(row=0,column=0,sticky="W")
input =Entry(root,width=60,borderwidth=5)
input.grid(row=1,column=0)


#input do nome da base de dados
textDBName = Label(root,text="DB Name")
textDBName.grid(row=2,column=0,sticky="W")
inputDBName =Entry(root,width=60,borderwidth=5)
inputDBName.grid(row=3,column=0,ipady=4,ipadx=4)


#caixa de texto para receber o username da DB
textName = Label(root,text="Username")
textName.grid(row=4,column=0,sticky="W")
inputUser=Entry(root,width=27,borderwidth=5)
inputUser.grid(row=5,column=0,ipady=4,ipadx=4,sticky="W")


#caixa de texto para receber a password da DB
textPass = Label(root,text="password")
textPass.grid(row=4,column=0,padx=4)
inputPassword=Entry(root,width=27,borderwidth=5)
inputPassword.grid(row=5,column=0,ipady=4,ipadx=4,sticky="E")


connectButton = Button(root,text="Connect",width=20,borderwidth=5, command=connectToDB)
connectButton.grid(row=5,column=1)







clicado = StringVar()
clicado.set("")





def fileSelect():
	root.filename = filedialog.askopenfilename(initialdir="",title="Select a file", filetypes=(("MP3 files","*.MP3"),("WAV files","*.WAV"),("RAR files","*.RAR")))
	myLabel = Label(root,text=root.filename).pack()



myButton = Button(root,text="Please Select a file", command=fileSelect)
#myButton.pack()





#e = Entry(root)
#e.pack()
#e.insert(0,"Enter your name")
#def myClick():
	#myLabel = Label(root,text=e.get())
	#myLabel.pack()

#myButton = Button(root,text="you name?",padx=50,pady=10,command=myClick)
#myButton.pack()








root.mainloop()


