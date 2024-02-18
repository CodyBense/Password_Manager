"""
TODO:
Edit so that create, edit, and delete bring up a second window
comment and cleanup code
FIX CAPITALIZATION
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
                host='192.168.0.26',
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
    def editusername(self, wb, usr):
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
    def editpassword(self, wb, pwd):
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
        self.frLeft = customtkinter.CTkFrame(master=self)
        self.frLeft.grid(
            row=0,
            column=0,
            rowspan=2,
            columnspan=1,
            sticky="nsew"
        )

        # textbox
        self.savedLogins = customtkinter.CTkTextbox(master=self.frLeft)
        self.savedLogins.pack(fill="both", expand=True)

        # create right frame and widgets
        self.frRight = customtkinter.CTkFrame(master=self)
        self.frRight.grid(
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

        # labels
        # self.lbusername = customtkinter.ctklabel(
        #     master=self.frRight,
        #     text="username"
        # )
        # self.lbusername.place(x=50, y=100)
        #
        # self.lbpassword = customtkinter.ctklabel(
        #     master=self.frRight,
        #     text="password"
        # )
        # self.lbpassword.place(x=50, y=150)

        # entry
        # self.eusername = customtkinter.ctkentry(master=self.frRight, width=150)
        # self.eusername.place(x=125, y=100)
        # self.epassword = customtkinter.ctkentry(master=self.frRight, width=150)
        # self.epassword.place(x=125, y=150)

        # buttons
        self.btnCreate = customtkinter.CTkButton(
                master=self.frRight, text="create", command=self.actNewCreate
                )
        self.btnCreate.place(x=125, y=200)

        self.btnFind = customtkinter.CTkButton(
                master=self.frRight, text="find", command=self.actNewFind
                )
        self.btnFind.place(x=125, y=250)

        self.btnEdit = customtkinter.CTkButton(
                master=self.frRight, text="edit", command=self.actNewEdit
                )
        self.btnEdit.place(x=125, y=300)

        self.btnDelete = customtkinter.CTkButton(
                master=self.frRight, text="delete", command=self.actNewDelete
                )
        self.btnDelete.place(x=125, y=350)

        # self.btncopyusername = customtkinter.CTkButton(
        #         master=self.frRight,
        #         width=20,
        #         text="",
        #         command=self.actcopytoclipboarduser,
        #         image=self.piCopytoClipbpard
        #         )
        # self.btncopyusername.place(x=300, y=100)
        #
        # self.btncopypassword = customtkinter.CTkButton(
        #         master=self.frRight,
        #         width=20,
        #         text="",
        #         command=self.actcopytoclipboardpass,
        #         image=self.piCopytoClipbpard
        #         )
        # self.btncopypassword.place(x=300, y=150)

        # set values
        self.setTb()

    """
    TODO:
    Figure out why buttons look weird after toplevel window is closed
    change packs to place
    workd on edit and delete functions
    """

    def actNewCreate(self):

        def actNewCreate():
            website = eWebsite.get()
            username = eUsername.get()
            password = ePassword.get()

            if password == '':
                password = self.genPassword()

            self.pm.add(website, username, password)

            self.setTb()

            create_window.destroy()
            create_window.update()
            app.update()

        create_window = customtkinter.CTkToplevel(self)
        create_window.title("New Login")

        eWebsite = customtkinter.CTkEntry(
            master=create_window, placeholder_text="Website", width=150
        )
        eWebsite.place(x=225, y=50)

        eUsername = customtkinter.CTkEntry(
            create_window, placeholder_text="Username", width=150
        )
        eUsername.place(x=225, y=100)

        ePassword = customtkinter.CTkEntry(
            create_window, placeholder_text="Password", width=150
        )
        ePassword.place(x=225, y=150)

        btnCreate = customtkinter.CTkButton(
            master=create_window, text="Create", command=actNewCreate
        )
        btnCreate.place(x=225, y=200)

    def actNewFind(self):
        def actNewFind():

            eUsername.delete(0, "end")
            ePassword.delete(0, "end")
            website = eWebsite.get()

            login_info = self.pm.find(website)

            eUsername.insert(0, login_info[0])
            ePassword.insert(0, login_info[1])

        def actClose():
            find_window.destroy()
            find_window.update()
            app.update()

        # copys text to clipboard
        def actCopyToClipboardUser():
            pyperclip.copy(eUsername.get())

        def actCopyToClipboardPass():
            pyperclip.copy(ePassword.get())

        find_window = customtkinter.CTkToplevel(self)
        find_window.title("Find Login")

        eWebsite = customtkinter.CTkEntry(
            master=find_window, placeholder_text="Website", width=150
        )
        eWebsite.place(x=225, y=50)

        eUsername = customtkinter.CTkEntry(
            find_window, placeholder_text="Username", width=150
        )
        eUsername.place(x=225, y=100)

        ePassword = customtkinter.CTkEntry(
            find_window, placeholder_text="Password", width=150
        )
        ePassword.place(x=225, y=150)

        btnFind = customtkinter.CTkButton(
            master=find_window, text="Find", command=actNewFind
        )
        btnFind.place(x=225, y=200)

        btnClose = customtkinter.CTkButton(
            master=find_window, text="Close", command=actClose
        )
        btnClose.place(x=225, y=250)

        btnCopyUsername = customtkinter.CTkButton(
            master=find_window,
            width=20,
            text="",
            command=actCopyToClipboardUser,
            image=self.copy
        )

        btnCopyPassword = customtkinter.CTkButton(
            master=find_window,
            width=20,
            text="",
            command=actCopyToClipboardPass,
            image=self.copy
        )

        btnCopyUsername.place(x=400, y=100)
        btnCopyPassword.place(x=400, y=150)

    def actNewEdit(self):

        def edit():
            pass

        edit_window = customtkinter.CTkToplevel(self)
        edit_window.title("Edit Login")

        eWebsite = customtkinter.CTkEntry(
            master=edit_window, placeholder_text="Website", width=150
        )
        eWebsite.place(
            relx=0.5,
            rely=0.5,
            anchor=tkinter.N
        )

        eUsername = customtkinter.CTkEntry(
            edit_window, placeholder_text="Username", width=150
        )
        eUsername.place(
            relx=0.5,
            rely=0.5,
            anchor=tkinter.N
        )

        ePassword = customtkinter.CTkEntry(
            edit_window, placeholder_text="Password", width=150
        )
        ePassword.place(
            relx=0.5,
            rely=0.5,
            anchor=tkinter.N
        )

    def actNewDelete(self):
        pass

    #
    # # actions and functions
    # # creates login info
    # def actCreate(self):
    #     dgWebsite = customtkinter.CTkInputDialog(
    #             text="Enter website:", title="Create Login"
    #             )
    #     website = dgWebsite.get_input()
    #
    #     dgUsername = customtkinter.CTkInputDialog(
    #             text="Enter username:", title="Create Login"
    #             )
    #     username = dgUsername.get_input()
    #
    #     dgPassword = customtkinter.CTkInputDialog(
    #         text="Enter Password (Leave empty to generate a password):",
    #         title="Create Password"
    #     )
    #     password = dgPassword.get_input()
    #
    #     if password == '':
    #         password = self.genPassword()
    #
    #     self.pm.add(website, username, password)
    #
    #     self.setTb()
    #
    # # finds the login info
    # def actFind(self):
    #     login_info = []
    #     self.eUsername.delete(0, "end")
    #     self.ePassword.delete(0, "end")
    #     dgWebsite = customtkinter.CTkInputDialog(
    #             text="Enter website:", title="Find Password"
    #             )
    #     website = dgWebsite.get_input()
    #
    #     login_info = self.pm.find(website)
    #
    #     self.eUsername.insert(0, login_info[0])
    #     self.ePassword.insert(0, login_info[1])
    #
    # # edits the login info
    # def actEdit(self):
    #     dgWebsite = customtkinter.CTkInputDialog(
    #             text="Enter website:", title="Edit"
    #             )
    #     website = dgWebsite.get_input()
    #
    #     dgChoice = customtkinter.CTkInputDialog(
    #             text="Edit (u)sername or (p)assword:", title="Edit"
    #             )
    #     choice = dgChoice.get_input()
    #
    #     if choice == "u":
    #         dgUsername = customtkinter.CTkInputDialog(
    #                 text="Enter new username:", title="Edit"
    #                 )
    #         username = dgUsername.get_input()
    #
    #         self.pm.editUsername(website, username)
    #     elif choice == "p":
    #         dgPassword = customtkinter.CTkInputDialog(
    #             text="Enter Password (Leave empty to generate a password):",
    #             title="Edit"
    #         )
    #         password = dgPassword.get_input()
    #
    #         if password == '':
    #             password = self.genPassword()
    #
    #         self.pm.editPassword(website, password)
    #
    # # deletes login info
    # def actDelete(self):
    #     dgWebsite = customtkinter.CTkInputDialog(
    #             text="Enter website:", title="Delete login"
    #             )
    #     website = dgWebsite.get_input()
    #
    #     self.pm.delete(website)
    #
    #     self.setTb()
    #

    # set tb to show websites for saved logins
    def setTb(self):
        saved_website = self.pm.show_all()
        self.savedLogins.configure(state="normal")
        self.savedLogins.delete("0.0", "end")
        for x in range(0, len(saved_website)):
            self.savedLogins.insert("end", f"{saved_website[x][0]}\n")
        self.savedLogins.configure(state="disabled")

    # generates a password
    def genPassword(self):
        excludeValues = [
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
        def randomASCIIValue():
            return choice([i for i in range(33, 122) if i not in excludeValues])

        # creates the password
        for i in range(0, 10):
            password += "".join(chr(randomASCIIValue()))
        password += "__"
        return password


if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.update()
