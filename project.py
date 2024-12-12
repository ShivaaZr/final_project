import sqlite3 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect('PhoneBook.db')
cursor =  conn.cursor()

new_mode =  False     
edit_mode = False    
Contacts_info = []    
current = 0      

#====================================== Function ==========================================


def create_tblUser():
    sql='''create table tblUser(
        Password integer primary key Autoincrement,
        Username text
    )
    '''
    cursor.execute(sql)
    conn.commit()
    
def create_tblContacts():
    sql='''create table tblContacts(
        ID integer,
        Name text,
        LastName text primary key, 
        PhoneNumber integer,
        CellNumber integer,
        Address text
    )
    '''
    cursor.execute(sql)
    conn.commit()

def Help():
        Help_text= """Enter your Password and Username to Login.
        If you don't have an account, Please Sign Up."""
        messagebox.showinfo("Help", Help_text) 

def login():
    cursor.execute("select * from tblUser where Username = ? and Password =?", (entryUsername.get(), entryPassword.get()))
    login = cursor.fetchone()
    if login:
        Contacts_page()
    else:
        messagebox.showerror("Error", "Usename or Password is wrong. Please Try Again.")   

def Contacts_page():
    def show_data(sql = 'select * from tblContacts'):
        global Contacts_info
        cursor.execute(sql)
        Contacts_info = cursor.fetchall()
        if Contacts_info == []:
            return
        ID.set(Contacts_info[current][0])
        Name.set(Contacts_info[current][1])
        LastName.set(Contacts_info[current][2])
        PhoneNumber.set(Contacts_info[current][3])
        CellNumber.set(Contacts_info[current][4])
        Address.set(Contacts_info[current][5])    
    

    def new_data(): 
        new_mode = True
        entryName.config(state ='normal')
        entryLastName.config(state ='normal')
        entryPhoneNumber.config(state ='normal')
        entryCellNumber.config(state ='normal')
        entryAddress.config(state ='normal')
        
        ID.set('')
        Name.set('')
        LastName.set('')
        PhoneNumber.set('')
        CellNumber.set('')
        Address.set('')
        
    def edit_data():
        edit_mode = True
        entryName.config(state ='normal')
        entryLastName.config(state ='normal')
        entryPhoneNumber.config(state ='normal')
        entryCellNumber.config(state ='normal')
        entryAddress.config(state ='normal')
        
    def submit_data():
        global new_mode
        global edit_mode
        sql = ''
        if new_mode == True:
            sql = f" insert into tblContacts (Name, LastName, PhoneNumber, CellNumber, Address) values ('{entryName.get()}','{entryLastName.get()}',{entryPhoneNumber.get()},{entryCellNumber.get()},'{entryAddress.get()}') "
            new_mode = False
        elif edit_mode == True:
            sql = f" update tblContacts set Name={entryName.get()}', LastName={entryLastName.get()}, PhoneNumber={entryPhoneNumber.get()}, CellNumber={entryCellNumber.get()} where ID={ID} "
            edit_mode = False
        
        entryName.config(state ='disable')
        entryLastName.config(state ='disable')
        entryPhoneNumber.config(state ='disable')
        entryCellNumber.config(state ='disable')
        entryAddress.config(state ='disable')
        cursor.execute(sql)
        conn.commit()
        messagebox.showinfo('Done','Your request is done successfully.')
        show_data()
        
    def cancel():
        show_data()
        entryName.config(state ='disable')
        entryLastName.config(state ='disable')
        entryPhoneNumber.config(stat ='disable')
        entryCellNumber.config(state ='disable')
        entryAddress.config(state ='disable')
        
    def delete():
        if messagebox.askyesno('Delete','Are you sure you want to delete this contact? ') is True:
            sql = f" delete from tblContacts where ID={ID}"
            cursor.execute(sql)
            conn.commit()
            messagebox.showinfo('Done','Your record is deleted successfully.')
            show_data()
            
    def next_rec():
        global current
        current += 1
        if current == len(Contacts_info):
            current = len(Contacts_info)-1
        show_data()

    def prev_rec():
        global current
        current -= 1
        if current == -1:
            current = 0
        show_data()

    def search():
        global current
        current = 0
        sql = f"select * from tblContacts where LastName like '%{entrySearch.get()}%' "
        show_data(sql)
    
#=============================== Contact Page Tkinter==================================================
    
    root= Toplevel(win)
    root.title("Contact Page")
    root.geometry("600x300")
    root.resizable(False, False)
        
    ID=IntVar(root)
    Name=StringVar(root)
    LastName=StringVar(root)
    PhoneNumber=IntVar(root)
    CellNumber=IntVar(root)
    Address=StringVar(root)
            
    fr1= Frame(root)
    fr1.pack(side=LEFT)
    lbID = ttk.Label(fr1, text="ID: ", font=("times", 12))
    lbID.pack(side=TOP, pady=5)
                    
    lbName = ttk.Label(fr1, text="Name: ", font=("times", 12))
    lbName.pack(side=TOP, pady=5)
                    
    lbLastname = ttk.Label(fr1, text="*Last Name: ", font=("times", 12))
    lbLastname.pack(side=TOP, pady=5)
                    
    lbPhone = ttk.Label(fr1, text="*Phone Number: ", font=("times", 12))
    lbPhone.pack(side=TOP, pady=5)
                
    lbCell = ttk.Label(fr1, text="*Cell Number: ", font=("times", 12))
    lbCell.pack(side=TOP, pady=5)
                    
    lbAddress = ttk.Label(fr1, text="Address: ", font=("times", 12))
    lbAddress.pack(side=TOP, pady=5)
    
    
                    
    fr2=Frame(root)
    fr2.pack(side=LEFT)
    entryID = ttk.Entry(fr2, width=25, textvariable=ID)
    entryID.pack(side=TOP, pady=5)
                    
    entryName = ttk.Entry(fr2, width=25, textvariable=Name)
    entryName.pack(side=TOP, pady=5)
                    
    entryLastName = ttk.Entry(fr2, width=25, textvariable=LastName)
    entryLastName.pack(side=TOP, pady=5)
                    
    entryPhoneNumber = ttk.Entry(fr2, width=25, textvariable=PhoneNumber)
    entryPhoneNumber.pack(side=TOP, pady=5)
                    
    entryCellNumber = ttk.Entry(fr2, width=25, textvariable=CellNumber)
    entryCellNumber.pack(side=TOP, pady=5)
                    
    entryAddress = ttk.Entry(fr2, width=25, textvariable=Address)
    entryAddress.pack(side=TOP, pady=5)
        
    entryID.config(state='disable')
    entryName.config(state='disable')
    entryLastName.config(state='disable')
    entryPhoneNumber.config(state='disable')
    entryCellNumber.config(state='disable')
    entryAddress.config(state='disable')

    fr3=Frame(root)
    fr3.pack(side=LEFT, padx=20)

    btnNew = ttk.Button(fr3, text="New",command=new_data)
    btnNew.pack(side=TOP, pady=5)

    btnEdite = ttk.Button(fr3, text="Edite", command=edit_data)
    btnEdite.pack(side=TOP, pady=5)

    btnDelete = ttk.Button(fr3, text="Delete", command=delete)
    btnDelete.pack(side=TOP, pady=5)

    btnSubmit = ttk.Button(fr3, text="Submit", command=submit_data)
    btnSubmit.pack(side=TOP, pady=5)
        
    btnCancel = ttk.Button(fr3, text="Cancel", command=cancel)
    btnCancel.pack(side=TOP, pady=5)

    fr4 = Frame(root)
    fr4.pack(side=LEFT, padx=20)
    btnNext=ttk.Button(fr4, text="Next",width=25, command=next_rec)
    btnNext.pack(side=TOP)
    
    btnPervious=ttk.Button(fr4, text="Pervious",width=25, command=prev_rec)
    btnPervious.pack(side=TOP,pady=5)
    
    lbSearch = ttk.Label(fr4, text="Search By Last Name : ", font=("times", 12))
    lbSearch.pack(side=TOP, pady=10)

    entrySearch = ttk.Entry(fr4, width=25)
    entrySearch.pack(side=TOP, pady=3)
    
    btnSearch = ttk.Button(fr4, text="Search", width=25, command=search)
    btnSearch.pack(side=TOP, pady=5)
        
    show_data()

#================================================= Sign Up Page ===========================================================

def sign_up_page(event):
    def sign_up_user():
            sql = f"insert into tblUser (Username, Password) values('{entrySignUser.get()}', '{entrySignPass.get()}')"
            cursor.execute(sql)
            conn.commit()
            messagebox.showinfo("Done", "Sign Up successful.")
            master.quit()
    master = Toplevel(win)
    master.geometry("300x300")
    master.title("Sign Up")
    
    lbSign = ttk.Label(master, text="Sign Up", font=("times", 16))
    lbSign.pack(side=TOP, pady=20)
    
    fr1 = Frame(master)
    fr1.pack(side=TOP, pady=5)
    lbSignUser = ttk.Label(fr1, text="Username: ", font=("times", 12))
    lbSignUser.pack(side=LEFT, pady=10)
    entrySignUser = ttk.Entry(fr1, width=25)
    entrySignUser.pack(side=LEFT, padx=5, pady=10)
    
    fr2 = Frame(master)
    fr2.pack(side=TOP, pady=10)
    lbSignPass = ttk.Label(fr2, text="Password: ", font=("times", 12))
    lbSignPass.pack(side=LEFT, pady=5)
    entrySignPass = ttk.Entry(fr2, width=25)
    entrySignPass.pack(side=LEFT, pady=5)
    
    fr3 = Frame(master)
    fr3.pack(side=TOP, pady=10)
    
    btnSign = ttk.Button(fr3, text="Sign Up", width=15, command=sign_up_user)
    btnSign.pack(side=BOTTOM, pady=5)
    
   
#========================================= Login Page ====================================
win = Tk()
win.geometry("400x300")
win.title("Phonebook")
win.resizable(False, False)

lbWelcome =ttk.Label(win, text="Welcome to Phonebook", font=("times", 16))
lbWelcome.pack(side=TOP, pady=25)

fr1 = Frame(win)
fr1.pack(pady=5)
lbUsername = ttk.Label(fr1, text="Username: ", font=("times", 12))
lbUsername.pack(side=LEFT)
entryUsername = ttk.Entry(fr1, width=20)
entryUsername.pack(side=LEFT)

fr2 = Frame(win)
fr2.pack(pady=10)
lbPassword = ttk.Label(fr2, text="Password: ", font=("times", 12))
lbPassword.pack(side=LEFT)
entryPassword = ttk.Entry(fr2, width=20)
entryPassword.pack(side=LEFT)

fr3=Frame(win)
fr3.pack(pady=15)
btnLogin = ttk.Button(fr3, text="Login", width=15, command=login)
btnLogin.pack()

fr4=Frame(win)
fr4.pack(pady=15)
lbNewuser = ttk.Label(fr4, text="New User? Sign Up ", font=("times", 12))
lbNewuser.bind("<Double-Button>", sign_up_page)
lbNewuser.pack()

menubar = Menu(win)
menubar.add_command(label="Help", command=Help)
menubar.add_command(label="Quit", command=win.quit)
win.config(menu=menubar)
#-------------------------------- Run -------------------------
win.mainloop()
conn.close()
