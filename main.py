# TODO: change how eidt works, work on second windown
import mysql.connector

import customtkinter
from PIL import Image, ImageTk
import pyperclip
from random import choice

customtkinter.set_appearance_mode("System")
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

    # TODO: update to do either on
    # edit a saved username
    def editUsername(self, wb, usr):
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
    def editPassword(self, wb, pwd):
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


# class EditLogin(customtkinter.CTkToplevel):
#     pm = PM()
#
#     def __init__(self):
#         super().__init__()
#         self.geometry("200x150")
#
#         self.btnUsername = customtkinter.CTkButton(
#                 self,
#                 text="Edit Username",
#                 command=self.actEditUsername
#                 )
#
#         self.btnUsername.pack(padx=20, pady=20)
#
#         self.btnPassword = customtkinter.CTkButton(
#                 self,
#                 text="Edit Password",
#                 command=self.actEditPassword
#                 )
#
#         self.btnPassword.pack(padx=20, pady=20)
#
#     def actEditUsername(self):
#         dgWebsite = customtkinter.CTkInputDialog(
#                 text="Enter website:", title="Edit Username"
#                 )
#         website = dgWebsite.get_input()
#
#         dgUsername = customtkinter.CTkInputDialog(
#                 text="Enter new username", title="Edit Username"
#                 )
#         username = dgUsername.get_input()
#
#         self.pm.editUsername(website, username)
#
#     def actEditPassword(self):
#         dgWebsite = customtkinter.CTkInputDialog(
#                 tex="Enter website:", title="Edit Password"
#                 )
#         website = dgWebsite.get_input()
#
#         dgPassword = customtkinter.CTkInputDialog(
#                 text="Enter new password (Leave blank for a gen password)", title="Edit Password"
#                 )
#         password = dgPassword.get_input()
#
#         self.pm.editPassword(website, password)


class App(customtkinter.CTk):
    pm = PM()

    def __init__(self):
        super().__init__()

        # attributes
        # self.edit_window = None
        self.geometry(f"{1100}x{580}")
        self.title("Password Manager")
        self.minsize(300, 200)
        # self.iconbitmap("/home/codybense/Code/Applications/Password_Manager/Icons/cat.svg")
        # self.ico = Image.open("/home/Code/Applications/Password_Manager/Icons/cat.svg")
        # self.photo = ImageTk.PhotoImage(self.ico)
        # self.wm_iconphoto(True, self.photo)

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
        self.piCopyToClipbpard = customtkinter.CTkImage(
            Image.open(r"/home/codybense/Code/Applications/Password_Manager/Icons/copy.png"),
            # size=(10, 10)
        )

        # labels
        self.lbUsername = customtkinter.CTkLabel(
            master=self.frRight,
            text="Username"
        )
        self.lbUsername.place(x=50, y=100)

        self.lbPassword = customtkinter.CTkLabel(
            master=self.frRight,
            text="Password"
        )
        self.lbPassword.place(x=50, y=150)

        # entry
        self.eUsername = customtkinter.CTkEntry(master=self.frRight, width=150)
        self.eUsername.place(x=125, y=100)
        self.ePassword = customtkinter.CTkEntry(master=self.frRight, width=150)
        self.ePassword.place(x=125, y=150)

        # buttons
        self.btnCreate = customtkinter.CTkButton(
                master=self.frRight, text="Create", command=self.actCreate
                )
        self.btnCreate.place(x=125, y=200)

        self.btnFind = customtkinter.CTkButton(
                master=self.frRight, text="Find", command=self.actFind
                )
        self.btnFind.place(x=125, y=250)

        self.btnEdit = customtkinter.CTkButton(
                master=self.frRight, text="Edit", command=self.actEdit
                )
        self.btnEdit.place(x=125, y=300)

        self.btnDelete = customtkinter.CTkButton(
                master=self.frRight, text="Delete", command=self.actDelete
                )
        self.btnDelete.place(x=125, y=350)

        self.btnCopyUsername = customtkinter.CTkButton(
                master=self.frRight,
                width=20,
                text="",
                command=self.actCopyToClipboardUser,
                image=self.piCopyToClipbpard
                )
        self.btnCopyUsername.place(x=300, y=100)

        self.btnCopyPassword = customtkinter.CTkButton(
                master=self.frRight,
                width=20,
                text="",
                command=self.actCopyToClipboardPass,
                image=self.piCopyToClipbpard
                )
        self.btnCopyPassword.place(x=300, y=150)

        # set values
        self.setTb()

    # actions and functions
    # creates login info
    def actCreate(self):
        dgWebsite = customtkinter.CTkInputDialog(
                text="Enter website:", title="Create Login"
                )
        website = dgWebsite.get_input()

        dgUsername = customtkinter.CTkInputDialog(
                text="Enter username:", title="Create Login"
                )
        username = dgUsername.get_input()

        dgPassword = customtkinter.CTkInputDialog(
            text="Enter Password (Leave empty to generate a password):",
            title="Create Password"
        )
        password = dgPassword.get_input()

        if password == '':
            password = self.genPassword()

        self.pm.add(website, username, password)

        self.setTb()

    # finds the login info
    def actFind(self):
        login_info = []
        self.eUsername.delete(0, "end")
        self.ePassword.delete(0, "end")
        dgWebsite = customtkinter.CTkInputDialog(
                text="Enter website:", title="Find Password"
                )
        website = dgWebsite.get_input()

        login_info = self.pm.find(website)

        self.eUsername.insert(0, login_info[0])
        self.ePassword.insert(0, login_info[1])

    # edits the login info
    def actEdit(self):
        dgWebsite = customtkinter.CTkInputDialog(
                text="Enter website:", title="Edit"
                )
        website = dgWebsite.get_input()

        dgChoice = customtkinter.CTkInputDialog(
                text="Edit (u)sername or (p)assword:", title="Edit"
                )
        choice = dgChoice.get_input()

        if choice == "u":
            dgUsername = customtkinter.CTkInputDialog(
                    text="Enter new username:", title="Edit"
                    )
            username = dgUsername.get_input()

            self.pm.editUsername(website, username)
        elif choice == "p":
            dgPassword = customtkinter.CTkInputDialog(
                text="Enter Password (Leave empty to generate a password):",
                title="Edit"
            )
            password = dgPassword.get_input()

            if password == '':
                password = self.genPassword()

            self.pm.editPassword(website, password)

    # deletes login info
    def actDelete(self):
        dgWebsite = customtkinter.CTkInputDialog(
                text="Enter website:", title="Delete login"
                )
        website = dgWebsite.get_input()

        self.pm.delete(website)

        self.setTb()

    # copys text to clipboard
    def actCopyToClipboardUser(self):
        pyperclip.copy(self.eUsername.get())

    def actCopyToClipboardPass(self):
        pyperclip.copy(self.ePassword.get())

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
