# database
from tkinter import *
from tkinter import ttk, messagebox
from Cryptodome.Cipher import AES
import sqlite3
# a: username
# b: key

def options(a,b):
    root = Tk()
    root.title("VaultClick Password Manager")
    root.geometry("800x500")
    root.iconbitmap('C:/Users/Manjeet Saini/PycharmProjects/PasswordManager/Vault.ico')
    root.minsize(800, 500)
    root.maxsize(800, 500)

    def encrypt(plaintext):


        def pad_plain(plaintext):
            l = len(plaintext)
            y = l + len(str(l)) + 1
            p_plaintext = plaintext + (32 - y % 32) * '[' + '[' + str(l)
            # print("after modify :", p_plaintext)
            return p_plaintext

        p_plaintext = pad_plain(plaintext)
        p_plaintext = p_plaintext.encode('UTF-8')
        key = b
        # print(key)
        key = key.encode('UTF-8')
        # print(key)
        cipher = AES.new(key, AES.MODE_ECB)
        eps = cipher.encrypt(p_plaintext)
        # print("encrypted : ", eps)

        return eps

    def decrypt(epass):
        # print(epass)
        key = b
        # print(key)
        key = key.encode('UTF-8')
        # print(key)
        cipher2 = AES.new(key, AES.MODE_ECB)
        data = cipher2.decrypt(epass)

        # print(data)

        password = data.decode('UTF-8')
        i = len(password) - 1
        while password[i] != "[":
            i -= 1

        x = int(password[i + 1:])
        # print("plain text : ", password[:x])
        password = password[:x]

        return password

    def vpass():
        try:
            # clear
            f_web.delete(0, END)
            f_user.delete(0, END)
            f_pass.delete(0, END)
            x = my_tree.focus()
            i = my_tree.item(x)
            d = str(i['values'][0])
            w = str(i['values'][1])
            u = str(i['values'][2])

            conn = sqlite3.connect("Manager.db")
            c = conn.cursor()  # create cursor
            sqle = '''SELECT  password from {} WHERE pid= ?'''.format(a)
            c.execute(sqle, (d,))
            x = c.fetchall()
            ep = x[0][0]
            pw = decrypt(ep)
            f_web.insert(0, w)
            f_user.insert(0, u)
            f_pass.insert(0, pw)
        except:
            inf = "No Selection"
            messagebox.showerror("Showerror", inf)

    def add():
        w = f_web.get()
        us = f_user.get()
        ps = f_pass.get()
        eps = encrypt(ps)
        if len(w) > 2 and len(us) > 3 and len(ps) > 3:
            try:
                conn = sqlite3.connect("Manager.db")
                c = conn.cursor()  # create cursor
                sql_cmd = "INSERT INTO {} VALUES(?,?,?,?)".format(a)
                c.execute(sql_cmd, (None, w, us, eps))
                conn.commit()  # comit change
                conn.close()  # close connection
                inf = "Record Added Successfully "
                messagebox.showinfo("Successful Addition ", inf)
                f_web.delete(0, END)
                f_user.delete(0, END)
                f_pass.delete(0, END)

            except:
                inf = "Invalid Details"
                messagebox.showerror("Showerror", inf)
        else:
            inf = "Invalid Details"
            messagebox.showerror("Showerror", inf)

    def update():
        try:
            w = f_web.get()
            us = f_user.get()
            ps = f_pass.get()
            if len(w) < 1 and len(us) < 0 and len(ps) < 0:
                inf = "Invalid Details"
                messagebox.showerror("Showerror", inf)
            else:
                x = my_tree.focus()
                i = my_tree.item(x)
                d = str(i['values'][0])
                eps=encrypt(ps)
                conn = sqlite3.connect("Manager.db")
                c = conn.cursor()  # create cursor
                sql_cmd = "UPDATE {} SET website = ?, username = ?, password = ?  WHERE pid =?".format(a)
                c.execute(sql_cmd, (w, us, eps, d))
                my_tree.delete(x)
                my_tree.insert(parent='', index='end', iid=int(x), text="Parent", values=(d, w, us))
                conn.commit()  # comit change
                conn.close()  # close connection
                inf = "Record successfully Update"
                messagebox.showinfo("Successful Updated", inf)
        except:
            inf = "No Selection"
            messagebox.showerror("Showerror", inf)

    def record():
        try:
            for item in my_tree.get_children():
                my_tree.delete(item)
            conn = sqlite3.connect("Manager.db")
            c = conn.cursor()  # create cursor
            sql_selectall = '''SELECT * from {}'''.format(a)
            c.execute(sql_selectall)
            x = c.fetchall()
            for i in range(len(x)):
                my_tree.insert(parent='', index='end', iid=i, text="Parent", values=(x[i][0], x[i][1], x[i][2]))

            conn.commit()
            conn.close()

        except:
            pass

    def delete():
        try:
            x = my_tree.focus()
            i = my_tree.item(x)
            d = str(i['values'][0])
            conn = sqlite3.connect("Manager.db")
            c = conn.cursor()  # create cursor
            sql_cmd = '''DELETE FROM   {} WHERE pid = ? '''.format(a)
            c.execute(sql_cmd, (d,))
            my_tree.delete(x)
            conn.commit()  # comit change
            conn.close()  # close connection
            inf = "Record successfully Delete"
            messagebox.showinfo("Successful Deletion", inf)
        except:
            inf = "No Selection"
            messagebox.showerror("Showerror", inf)

    tree_frame = Frame(root)
    tree_frame.grid(row=0, column=0, padx=10, pady=10)
    my_tree = ttk.Treeview(tree_frame)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    my_tree.pack()
    # config scroll
    tree_scroll.config(command=my_tree.yview)

    # define our column
    my_tree['columns'] = ("PasswordID", "Website", "Username")
    # format column
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("PasswordID", anchor=CENTER, width=80, minwidth=80, stretch=NO)
    my_tree.column("Website", anchor=W, width=200, minwidth=200, )
    my_tree.column("Username", anchor=W, width=200, minwidth=200, stretch=NO)
    # heading
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("PasswordID", text="PasswordID", anchor=W)
    my_tree.heading("Website", text="Website", anchor=W)
    my_tree.heading("Username", text="Username", anchor=W)

    button_frame = Frame(root)
    button_frame.grid(row=0, column=1, padx=5, pady=20)
    l_header = Label(button_frame, text="Welcome : " + a).grid(row=0, column=0)
    b_show = Button(button_frame, text="View Records", padx=10, pady=10, command=record)
    b_show.grid(row=1, column=0, pady=10)

    b_add = Button(button_frame, text=" Add Password ", padx=10, pady=10, command=add)
    b_add.grid(row=2, column=0, padx=10, pady=10)

    b_update = Button(button_frame, text="Update Records", padx=10, pady=10, command=update)
    b_update.grid(row=3, column=0, pady=10)

    b_delte = Button(button_frame, text=" Delete Records ", padx=10, pady=10, command=delete)
    b_delte.grid(row=4, column=0, pady=10)

    b_showpass = Button(button_frame, text=" Show Password ", padx=10, pady=10, command=vpass)
    b_showpass.grid(row=5, column=0, pady=10)

    add_frame = Frame(root)
    add_frame.grid(row=2, column=0, padx=10)
    l_website = Label(add_frame, text="Website")
    l_website.grid(row=0, column=0)

    l_username = Label(add_frame, text="Username")
    l_username.grid(row=0, column=1)

    l_password = Label(add_frame, text="Password")
    l_password.grid(row=0, column=2)

    # textfield

    f_web = Entry(add_frame, width=30)
    f_web.grid(row=1, column=0, padx=10)
    f_user = Entry(add_frame, width=30)
    f_user.grid(row=1, column=1, padx=10)
    f_pass = Entry(add_frame, width=30)
    f_pass.grid(row=1, column=2, padx=10)

    root.mainloop()
