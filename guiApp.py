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

#função para criar a connexão á DB
def connectToDB():
	DBendpoint = input.get()
	DBUsername = inputUser.get()
	DBPassword = inputPassword.get()
	DBName = inputDBName.get()
	DBConn = mysql.connector.connect(host=DBendpoint,user=DBUsername,password=DBPassword,db=DBName)
	#try:
	#	DBConn = mysql.connector.connect(host=DBendpoint,user=DBUsername,password=DBPassword)
	#except:
	#	messagebox.showinfo(title="Error",message="Could not Connect to database")
	#	drop= OptionMenu(root, clicado, "1","2","3","4","5")
	#	drop.grid(row=3,column=0,sticky="W")
	if(DBConn.is_connected()==False):
		messagebox.showinfo(title="Error",message="Could not Connect to database")

	else:
		messagebox.showinfo(title="Error",message="Could Connect to database")
		ListOfTables=[]
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
input =Entry(root,width=60,borderwidth=5)
input.grid(row=0,column=0)
input.insert(0,"DB endpoint")

#input do nome da base de dados
inputDBName =Entry(root,width=60,borderwidth=5)
inputDBName.grid(row=1,column=0)
inputDBName.insert(0,"DB name")

#caixa de texto para receber o username da DB
inputUser=Entry(root,width=27,borderwidth=5)
inputUser.grid(row=2,column=0,ipady=4,ipadx=4,pady=4,sticky="W")
inputUser.insert(0,"Username")

#caixa de texto para receber a password da DB
inputPassword=Entry(root,width=27,borderwidth=5)
inputPassword.grid(row=2,column=0,ipady=4,ipadx=4,pady=4,sticky="E")
inputPassword.insert(0, "Password")

connectButton = Button(root,text="Connect",width=20,borderwidth=5, command=connectToDB)
connectButton.grid(row=2,column=1)







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


