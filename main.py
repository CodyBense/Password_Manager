"""
TODO:
"""
import mysql.connector

import tkinter
import customtkinter
from PIL import Image, ImageTk
import pyperclip
from random import choice

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


class PM:
    def __init__(self):
        self.cxn = mysql.connector.connect(
                user='root',
                password='ZSe45rdx##',
                database='logins',
                host='192.168.1.129',
                port=3306
                )

        self.cursor = self.cxn.cursor()

    # adds login info to database
    def add(self, wb, usr, pwd):

        add_login = ("INSERT INTO login "
                     "(website, username, password) "
                     "VALUES ( %s, %s, %s)")
        data_login = (wb, usr, pwd)

        self.cursor.execute(add_login, data_login)
        self.cxn.commit()

    # finds specific login
    def find(self, wb):
        query = ("SELECT username, password FROM login "
                 "WHERE website = %(website)s")
        query_condition = {'website': wb}

        self.cursor.execute(query, query_condition)

        for (username, password) in self.cursor:
            return username, password

    # todo: update to do either on
    # edit a saved username
    def edit_username(self, wb, usr):
        query = ("UPDATE login "
                 "SET username = %s "
                 "WHERE website = %s")
        query_condition = (
                usr,
                wb
                )

        self.cursor.execute(query, query_condition)
        self.cxn.commit()

    # edit a saved password
    def edit_password(self, wb, pwd):
        query = ("UPDATE login "
                 "SET password = %s "
                 "WHERE website = %s")
        query_condition = (
                pwd,
                wb
                )

        self.cursor.execute(query, query_condition)
        self.cxn.commit()

    # deletes a saved login
    def delete(self, wb):
        query = ("DELETE FROM login "
                 "WHERE website = %(website)s")
        query_condition = {'website': wb}

        self.cursor.execute(query, query_condition)
        self.cxn.commit()

    # shows all the websites with saved logins
    def show_all(self):
        saved_websites = []
        self.cursor.execute("SELECT * FROM login "
                            "ORDER BY website")
        for row in self.cursor.fetchall():
            saved_websites.append(row)
        return saved_websites


class App(customtkinter.CTk):
    pm = PM()

    def __init__(self):
        super().__init__()

        # attributes
        # self.edit_window = none
        self.geometry(f"{1100}x{580}")
        self.title("Password Manager")
        self.minsize(300, 200)
        # self.iconbitmap("/home/codybense/code/applications/password_manager/icons/cat.svg")
        # self.ico = image.open("/home/code/applications/password_manager/icons/cat.svg")
        # self.photo = imagetk.photoimage(self.ico)
        # self.wm_iconphoto(true, self.photo)

        # create 2x2 gird system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # creates left frame and widgets
        self.fr_left = customtkinter.CTkFrame(master=self)
        self.fr_left.grid(
            row=0,
            column=0,
            rowspan=2,
            columnspan=1,
            sticky="nsew"
        )

        # textbox
        self.saved_logins = customtkinter.CTkTextbox(master=self.fr_left)
        self.saved_logins.pack(fill="both", expand=True)

        # create right frame and widgets
        self.fr_right = customtkinter.CTkFrame(master=self)
        self.fr_right.grid(
            row=0,
            column=1,
            rowspan=2,
            columnspan=1,
            sticky="nsew"
        )

        # photo image
        self.copy = customtkinter.CTkImage(
            Image.open(
                r"/home/codybense/Code/Applications/Password_Manager/Icons/copy.png"
            ),
            # size=(10, 10)
        )

        # buttons
        self.btn_create = customtkinter.CTkButton(
                master=self.fr_right, text="create", command=self.act_new_create
                )
        self.btn_create.place(x=125, y=200)

        self.btn_find = customtkinter.CTkButton(
                master=self.fr_right, text="find", command=self.act_new_find
                )
        self.btn_find.place(x=125, y=250)

        self.btnEdit = customtkinter.CTkButton(
                master=self.fr_right, text="edit", command=self.act_new_edit
                )
        self.btnEdit.place(x=125, y=300)

        self.btnDelete = customtkinter.CTkButton(
                master=self.fr_right, text="delete", command=self.act_new_delete
                )
        self.btnDelete.place(x=125, y=350)

        # set values
        self.set_tb()

    """
    TODO:
    Figure out why buttons look weird after toplevel window is closed
    change packs to place
    workd on edit and delete functions
    """

    # opens new window to create a new login
    def act_new_create(self):

        # handles the creation of new login
        def act_create():
            website = entry_website.get()
            username = entry_username.get()
            password = entry_password.get()

            if password == '':
                password = self.gen_password()

            self.pm.add(website, username, password)

            self.set_tb()

            create_window.destroy()
            create_window.update()
            app.update()

        # close window
        def act_close():
            create_window.destroy()
            create_window.update()
            app.update()

        # creates window, enteries, and buttons
        create_window = customtkinter.CTkToplevel(self)
        create_window.title("New Login")

        entry_website = customtkinter.CTkEntry(
            master=create_window, placeholder_text="Website", width=150
        )
        entry_website.place(
            relx=0.5,
            rely=0.5,
            anchor=customtkinter.CENTER
        )

        entry_username = customtkinter.CTkEntry(
            create_window, placeholder_text="Username", width=150
        )
        entry_username.place(
            relx=0.5,
            rely=0.55,
            anchor=customtkinter.CENTER
        )

        entry_password = customtkinter.CTkEntry(
            create_window, placeholder_text="Password", width=150
        )
        entry_password.place(
            relx=0.5,
            rely=0.6,
            anchor=customtkinter.CENTER
        )

        btn_create = customtkinter.CTkButton(
            master=create_window,
            text="Create",
            command=act_create
        )
        btn_create.place(
            relx=0.5,
            rely=0.65,
            anchor=customtkinter.CENTER
        )

        btn_close = customtkinter.CTkButton(
            master=create_window,
            text="Close",
            command=act_close
        )
        btn_close.place(
            relx=0.5,
            rely=0.7,
            anchor=customtkinter.CENTER
        )

    # opens new window to find login info
    def act_new_find(self):

        # handles the finding of login info
        def act_find():

            entry_username.delete(0, "end")
            entry_password.delete(0, "end")
            website = entry_website.get()

            login_info = self.pm.find(website)

            entry_username.insert(0, login_info[0])
            entry_password.insert(0, login_info[1])

        # closes window
        def act_close():
            find_window.destroy()
            find_window.update()
            app.update()

        # copys text to clipboard
        def act_copy_user():
            pyperclip.copy(entry_username.get())

        def act_copy_pass():
            pyperclip.copy(entry_password.get())

        # creates widnow, enteries, and buttons
        find_window = customtkinter.CTkToplevel(self)
        find_window.title("Find Login")

        entry_website = customtkinter.CTkEntry(
            master=find_window, placeholder_text="Website", width=150
        )
        entry_website.place(
            relx=0.5,
            rely=0.5,
            anchor=customtkinter.CENTER
        )

        entry_username = customtkinter.CTkEntry(
            find_window, placeholder_text="Username", width=150
        )
        entry_username.place(
            relx=0.5,
            rely=0.55,
            anchor=customtkinter.CENTER
        )

        entry_password = customtkinter.CTkEntry(
            find_window, placeholder_text="Password", width=150
        )
        entry_password.place(
            relx=0.5,
            rely=0.6,
            anchor=customtkinter.CENTER
        )

        btn_find = customtkinter.CTkButton(
            master=find_window, text="Find", command=act_find
        )
        btn_find.place(
            relx=0.5,
            rely=0.65,
            anchor=customtkinter.CENTER
        )

        btn_close = customtkinter.CTkButton(
            master=find_window, text="Close", command=act_close
        )
        btn_close.place(
            relx=0.5,
            rely=0.7,
            anchor=customtkinter.CENTER
        )

        btn_copy_username = customtkinter.CTkButton(
            master=find_window,
            width=20,
            text="",
            command=act_copy_user,
            image=self.copy
        )

        btn_copy_password = customtkinter.CTkButton(
            master=find_window,
            width=20,
            text="",
            command=act_copy_pass,
            image=self.copy
        )

        btn_copy_username.place(
            relx=0.65,
            rely=0.55,
            anchor=customtkinter.CENTER
        )
        btn_copy_password.place(
            relx=0.65,
            rely=0.6,
            anchor=customtkinter.CENTER
        )

    # opens new windows to edit login info
    def act_new_edit(self):

        # hanles the editing of login info
        def act_edit():
            website = entry_website.get()
            username = entry_username.get()
            password = entry_password.get()

            if username != "" and password != "":
                self.pm.edit_username(website, username)
                self.pm.edit_password(website, password)
            elif username != "":
                self.pm.edit_username(website, username)
            elif password != "":
                self.pm.edit_password(website, password)

        # closes window
        def act_close():
            edit_window.destroy()
            edit_window.update()
            app.update()

        # creates window, entries, and buttons
        edit_window = customtkinter.CTkToplevel(self)
        edit_window.title("Edit Login")

        entry_website = customtkinter.CTkEntry(
            master=edit_window, placeholder_text="Website", width=150
        )
        entry_website.place(
            relx=0.5,
            rely=0.5,
            anchor=customtkinter.CENTER
        )

        entry_username = customtkinter.CTkEntry(
            edit_window, placeholder_text="Username", width=150
        )
        entry_username.place(
            relx=0.5,
            rely=0.55,
            anchor=customtkinter.CENTER
        )

        entry_password = customtkinter.CTkEntry(
            edit_window, placeholder_text="Password", width=150
        )
        entry_password.place(
            relx=0.5,
            rely=0.6,
            anchor=customtkinter.CENTER
        )

        btn_edit = customtkinter.CTkButton(
            master=edit_window,
            text="Edit",
            command=act_edit
        )
        btn_edit.place(
            relx=0.5,
            rely=0.65,
            anchor=customtkinter.CENTER
        )

        btn_close = customtkinter.CTkButton(
            master=edit_window,
            text="Close",
            command=act_close
        )
        btn_close.place(
            relx=0.5,
            rely=0.7,
            anchor=customtkinter.CENTER
        )

    # opens new window to delete login info
    def act_new_delete(self):

        # handles the deletion of login info
        def act_delete():
            self.pm.delete(entry_website.get())
            self.set_tb()

        # closes the window
        def act_close():
            delete_window.destroy()
            delete_window.update()
            app.update()

        # creates window, entries, and buttons
        delete_window = customtkinter.CTkToplevel(self)
        delete_window.title("Delete Login")

        entry_website = customtkinter.CTkEntry(
            master=delete_window, placeholder_text="Website", width=150
        )
        entry_website.place(
            relx=0.5,
            rely=0.5,
            anchor=customtkinter.CENTER
        )

        btn_delete = customtkinter.CTkButton(
            master=delete_window,
            text="Delete",
            command=act_delete
        )
        btn_delete.place(
            relx=0.5,
            rely=0.55,
            anchor=customtkinter.CENTER
        )

        btn_close = customtkinter.CTkButton(
            master=delete_window,
            text="Close",
            command=act_close
        )
        btn_close.place(
            relx=0.5,
            rely=0.6,
            anchor=customtkinter.CENTER
        )

    # set tb to show websites for saved logins
    def set_tb(self):
        saved_website = self.pm.show_all()
        self.saved_logins.configure(state="normal")
        self.saved_logins.delete("0.0", "end")
        for x in range(0, len(saved_website)):
            self.saved_logins.insert("end", f"{saved_website[x][0]}\n")
        self.saved_logins.configure(state="disabled")

    # generates a password
    def gen_password(self):
        exclude_values = [
            34,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            91,
            92,
            93,
            94,
            96,
        ]
        password = ""

        # generates accepted ascii values
        def random_ASCII_value():
            return choice([i for i in range(33, 122) if i not in exclude_values])

        # creates the password
        for i in range(0, 10):
            password += "".join(chr(random_ASCII_value()))
        password += "__"
        return password


if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.update()
