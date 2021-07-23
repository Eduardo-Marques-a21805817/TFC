from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import mysql.connector

from Music_classifier_service import music_classifier_service

root = Tk()
root.title("TFC")
root.geometry("600x600")
file_path = None
file_to_send=None
listaTemp = None
cursor = None
clicado = None
DBConn = None
field_types=None
field_names=None
entry = {}
label = {}
buttons = {}

MODEL_PATH = "modelo.h5"

listaDeColunas = []


def getAudioFile():
    root.filename = filedialog.askopenfilename(initialdir="C:/", title="select a music file",
                                               filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav"),))
    global file_path
    file_path = root.filename
   # print("this is the filepath {}".format(file_path))
    pathloc['text'] = file_path


def classify_music():
    genreLabel['text'] = "processing audio ...."
    global file_path
    if file_path is None:
       # print("this is the filepath {}".format(file_path))
        genreLabel['text'] = ""
    else:

        #print("this is the filepath {}".format(file_path))
        mss = music_classifier_service()
        genero = mss.predict(file_path)
        genreLabel['text'] = "The song is classified as:  {}".format(genero)


# função para criar a connexão á DB
def connectToDB():
    DBendpoint = input.get()
    DBUsername = inputUser.get()
    DBPassword = inputPassword.get()
    DBName = inputDBName.get()

    if (DBendpoint == "DB endpoint" and DBName == "DB name" and DBUsername == "Username" and DBPassword == "Password"):
        messagebox.showinfo(title="Error", message="Could not Connect to database")

    try:
        global DBConn
        DBConn = mysql.connector.connect(host=DBendpoint, user=DBUsername, password=DBPassword, db=DBName)

        if (DBConn.is_connected() == False):
            messagebox.showinfo(title="Error", message="Could not Connect to database")
        else:
            messagebox.showinfo(title="Error", message="Could Connect to database")

            global cursor
            cursor = DBConn.cursor(buffered=True)
            cursor.execute("Show tables;")

            global listaTemp
            listaTemp = cursor.fetchall()
           # print(listaTemp)

            global clicado
            clicado = StringVar()
            clicado.set("Select a table from the database")

            # print(DBConn)
            drop = OptionMenu(root, clicado, *listaTemp, command=create_entries_for_selected_table)
            drop.grid(row=8, column=0, sticky="W")
    except mysql.connector.Error as err:
        messagebox.showinfo(title="Error", message="Could not connect to database")
        # print(clicado)
        # for x in listaTemp:
        # drop.insert(x)


def create_entries_for_selected_table(event):
    chosen_table = clicado.get()
    chosen_table = chosen_table.replace("(", "")
    chosen_table = chosen_table.replace(")", "")
    chosen_table = chosen_table.replace("'", "")
    chosen_table = chosen_table.replace(",", "")
   # print("SELECT * FROM {}".format(chosen_table))
    j = 9
    cursor.execute("SELECT * FROM {}".format(chosen_table))

    num_fields = len(cursor.description)
    global field_names
    field_names = [i[0] for i in cursor.description]


    #print(cursor.fetchall())
    global entry
    global label
    global buttons
    # delete pre-existing entries
    for entrada in entry:
        entry[entrada].destroy()
    for desc in label:
        label[desc].destroy()
    for btn in buttons:
        buttons[btn].destroy()

    entry = {}
    label = {}
    buttons = {}
    #cursor.execute("SELECT DATA_TYPE FROM FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}'".format(chosen_table))
    global  field_types
    field_types = [i[1] for i in cursor.description]
   # print(field_types)
    global listaTemp
    k=0
    ##data codes 3= INT(long)
    #             253=varchar
    #            252=Blob e variantes(longblob tinyblob)
    for name in field_names:
        #label[name].destroy()
        #entry[name].destroy()
        #buttons[name].destroy()
        data_type=field_types[k]
        k+=1
        #print(data_type)
        if data_type==3:

            lb = Label(root, text=name)
            lb.grid(row=j, column=0, sticky=W)
            label[name] = lb
            j += 1

            e = Entry(root)
            e.grid(row=j, column=0, sticky=W)
            entry[name] = e
            j += 1

        elif data_type==253:

            lb = Label(root, text=name)
            lb.grid(row=j, column=0, sticky=W)
            label[name] = lb
            j += 1

            e = Entry(root)
            e.grid(row=j, column=0, sticky=W)
            entry[name] = e
            j += 1

        elif data_type==252:
            lb = Label(root, text=name)
            lb.grid(row=j, column=0, sticky=W)
            label[name] = lb
            j += 1
            global file_path
            global file_to_send
            file_to_send=file_path

            e = Button(root,text="mudar o ficheiro", command=change_file)
            e.grid(row=j, column=0, sticky=W)
            buttons[name] = e

            #lb2 = Label(root,text=os.path.split(file_to_send)[1])
            #lb2.grid(row=j,column=1,sticky=W)
            j += 1

    insert_button = Button(root,text="Make database entry",command=insert_into_db)
    insert_button.grid(row=j,column=0,sticky=W)

def insert_into_db():
    chosen_table = clicado.get()
    chosen_table = chosen_table.replace("(", "")
    chosen_table = chosen_table.replace(")", "")
    chosen_table = chosen_table.replace("'", "")
    chosen_table = chosen_table.replace(",", "")
    execute_string = "INSERT INTO {}(".format(chosen_table)
    global field_names
    global file_path
    global file_to_send
    global field_types
    k=0
    i=0
    list_of_values =[]
    for name in field_names:

        if name in entry:
            if field_types[k]==3:
                try:
                    valor_int = int(entry[name].get())
                    list_of_values.append(valor_int)
                except ValueError as verr:
                    messagebox.showinfo(title="Error", message="Exepected an integer in one of the columns")
            else:
                list_of_values.append(entry[name].get())
        elif name in buttons:
            if file_to_send is None:
                with open(file_path,"rb") as file:
                    binary_data_to_send=file.read()
                    list_of_values.append(binary_data_to_send)
            else:
                with open(file_to_send,"rb") as file:
                    binary_data_to_send=file.read()
                    list_of_values.append(binary_data_to_send)
       # if entry[name] in entry:
        #    list_of_values.append(entry[name].get())
        #    print(entry[name].get())
       # elif buttons[name] in buttons:
         #   list_of_values.append(entry[name].get())
        k+=1

        if i==0:
            execute_string+="{}".format(name)
            i+=1
        else:
            execute_string += ", {}".format(name)

    #cursor.execute(execute_string,)
    execute_string+=") VALUES("
    j=0
    for element in list_of_values:
        if j==0:
            execute_string +="%s"
            j+=1
        else:
            execute_string+=", %s"
    execute_string += ")"
    print(execute_string)
    cursor.execute(execute_string,list_of_values)
    global DBConn
    DBConn.commit()
    #print(list_of_values)


def change_file():
    root.filename = filedialog.askopenfilename(initialdir="C:/", title="select a music file",
                                               filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav"),))
    global file_to_send
    file_to_send =root.filename

# função que verifica se houve conexão á DB
# def isThereDB():
# print("things")

# caixa de texto para receber o endpoint da DB
textEnd = Label(root, text="DB Endpoint")
textEnd.grid(row=2, column=0, sticky="W")
input = Entry(root, width=60, borderwidth=5)
input.grid(row=3, column=0)

# input do nome da base de dados
textDBName = Label(root, text="DB Name")
textDBName.grid(row=4, column=0, sticky="W")
inputDBName = Entry(root, width=60, borderwidth=5)
inputDBName.grid(row=5, column=0, ipady=4, ipadx=4)

# caixa de texto para receber o username da DB
textName = Label(root, text="Username e Password")
textName.grid(row=6, column=0, sticky="W")
inputUser = Entry(root, width=27, borderwidth=5)
inputUser.grid(row=7, column=0, ipady=4, ipadx=4, sticky="W")

# caixa de texto para receber a password da DB
inputPassword = Entry(root, width=27, borderwidth=5)
inputPassword.grid(row=7, column=0, ipady=4, ipadx=4, sticky="E")

connectButton = Button(root, text="Connect", width=20, borderwidth=5, command=connectToDB)
connectButton.grid(row=7, column=1)

# choose file related
openFileButton = Button(root, text="select an audio file", width=20, borderwidth=5, command=getAudioFile)
openFileButton.grid(row=0, column=1)
pathloc = Label(root)
pathloc.grid(row=0, column=0)

classifyButton = Button(root, text="classify on genre", width=20, borderwidth=5, command=classify_music)
classifyButton.grid(row=1, column=1)
genreLabel = Label(root)
genreLabel.grid(row=1, column=0)


# genreLabel = Label(root)
# genreLabel.grid(row=1,column=0)


def fileSelect():
    root.filename = filedialog.askopenfilename(initialdir="", title="Select a file", filetypes=(
    ("MP3 files", "*.MP3"), ("WAV files", "*.WAV"), ("RAR files", "*.RAR")))
    myLabel = Label(root, text=root.filename).pack()


myButton = Button(root, text="Please Select a file", command=fileSelect)
# myButton.pack()


# e = Entry(root)
# e.pack()
# e.insert(0,"Enter your name")
# def myClick():
# myLabel = Label(root,text=e.get())
# myLabel.pack()

# myButton = Button(root,text="you name?",padx=50,pady=10,command=myClick)
# myButton.pack()


# if __name__=="__main__":


root.mainloop()
