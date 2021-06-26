# database

from tkinter import *
from tkinter import messagebox
import string
import random
import menutab
import sqlite3

root = Tk()
root.title("VaultClick")
root.iconbitmap('C:/Users/Manjeet Saini/PycharmProjects/PasswordManager/Vault.ico')
root.geometry("400x500")

root.minsize(400,500)
root.maxsize(400,500)


def ramdkey():
    res = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=32))

    return res


def submit( ):
    conn = sqlite3.connect("Manager.db")
    c = conn.cursor()  # create cursor
    sql_cmd = "SELECT * FROM Regusers where username = ? AND password=?"
    # sql_cmd = "SELECT * FROM Regusers where username =  AND password=? "
    a=s_user.get()
    b=p_pass.get()
    c.execute(sql_cmd,(a,b))
    row = c.fetchone()

    if row:
        messagebox.showinfo("info", "login successfully")
        f_user.delete(0, END)
        f_pass.delete(0, END)
        k = row[3]
        menutab.options(a,k)

    else:
        messagebox.showerror("Error", "Invalid Login credentials")
        f_user.delete(0, END)
        f_pass.delete(0, END)
    conn.commit()  # comit change
    conn.close()


def register():
    conn = sqlite3.connect("Manager.db")
    c = conn.cursor()  # create cursor
    # c.execute("INSERT INTO Regusers VALUES(:uname,:userid,:passw)",
    #           {
    #               'uname': f_nname.get(),
    #               'userid': f_nuser.get(),
    #               'passw': f_npass.get(),
    #
    #           })
    # # create password table
    # t = f_nuser.get()
    # sql_cmd = '''CREATE TABLE {}(pid integer PRIMARY KEY AUTOINCREMENT,website text NOT NULL ,username text ,password text NOT NULL)'''.format(t)
    # c.execute(sql_cmd)
    # conn.commit()  # comit change
    # conn.close()  # close connection
    # c.execute(""" CREATE TABLE Regusers (name text NOT NULL , username text PRIMARY KEY ,password text NOT NULL)""")

    sql = "CREATE TABLE IF NOT EXISTS Regusers (name text NOT NULL , username text PRIMARY KEY ,password text NOT NULL, key TEXT NOT NULL)"
    c.execute(sql)
    try:

        c.execute("INSERT INTO Regusers VALUES(:uname,:userid,:passw,:ukey)",
                  {
                      'uname': f_nname.get(),
                      'userid': f_nuser.get(),
                      'passw': f_npass.get(),
                      'ukey': ramdkey(),

                  })
        # create password table
        t = f_nuser.get()
        sql_cmd = '''CREATE TABLE {}(pid integer PRIMARY KEY ,website text NOT NULL ,
        username text ,password text NOT NULL)'''.format(t)
        c.execute(sql_cmd)
        conn.commit()  # comit change
        conn.close()  # close connection
        inf = "You have successfully registered! Please Login to continue"
        messagebox.showinfo("Successful registration", inf)
        f_nname.delete(0, END)
        f_nuser.delete(0, END)
        f_npass.delete(0, END)

    except:
        inf = "You are already registered! or Try with different username"
        messagebox.showerror("Showerror", inf)
        f_nname.delete(0, END)
        f_nuser.delete(0, END)
        f_npass.delete(0, END)


# ========================================================================================================================================
# text box
global a
global b

s_user = StringVar()
p_pass = StringVar()
f_user = Entry(root, width=30, textvariable=s_user)
f_user.grid(row=1, column=2, padx=10)
f_pass = Entry(root, width=30, textvariable=p_pass, show='*')
f_pass.grid(row=2, column=2, padx=10)

# lable
l_head = Label(root, text="Password Manager Login", padx=10, pady=25)
l_head.grid(row=0, column=0, padx=10, pady=10)
l_user = Label(root, text="Username")
l_user.grid(row=1, column=0, padx=10, pady=10)

l_pass = Label(root, text="Password")
l_pass.grid(row=2, column=0, padx=10, pady=10)
b_sub = Button(root, text="Login", padx=10, pady=10, command=submit)
b_sub.grid(row=3, column=0, columnspan=3, padx=10)

l_newreg = Label(root, text="New User Registration  ", padx=10, pady=10).grid(row=4, column=0)
# text box
f_nname = Entry(root, width=30)
f_nname.grid(row=5, column=2, padx=10)
f_nuser = Entry(root, width=30)
f_nuser.grid(row=6, column=2, padx=10)
f_npass = Entry(root, width=30, show='*')
f_npass.grid(row=7, column=2, padx=10)

l_name = Label(root, text="Name").grid(row=5, column=0, padx=10, pady=10)
l_nuser = Label(root, text="Username").grid(row=6, column=0, padx=10, pady=10)
l_npass = Label(root, text="Password").grid(row=7, column=0, padx=10, pady=10)
b_nreg = Button(root, text="Sign IN", padx=10, pady=10, command=register).grid(row=8, column=0, columnspan=3, padx=10)

root.mainloop()
