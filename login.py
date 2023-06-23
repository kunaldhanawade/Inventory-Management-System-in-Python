from tkinter import *
from tkinter import messagebox
from tkcalendar import *
from PIL import ImageTk, Image

# database connection
from pymongo import MongoClient

import owner
import bill
import customer

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
database = client["my_inventory"]

class Login:
    def __init__(self, master):
        self.master = master
        master.title("LOGIN")

        global username, password
        username = StringVar()
        password = StringVar()

        # frame
        frame1 = LabelFrame(
            self.master,
            bd=10,
            font=("times new roman", 15, "bold"),
            bg="#E8E8E8",
        )
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER)

        # logo image
        self.img = ImageTk.PhotoImage(Image.open("logo.jpeg"))
        imageLabel = Label(frame1, image=self.img, width=400, height=300).grid(
            row=0, column=0, pady=10, columnspan=2
        )

        # username label and username entry box
        usernameLabel = Label(
            frame1,
            text="USER NAME :",
            font=("times new roman", 18, "bold"),
            width=15,
            bg="#fff",
            fg="#000",
        ).grid(row=1, column=0, padx=15, pady=5)

        usernameEntry = Entry(
            frame1,
            textvariable=username,
            font=("times new roman", 18, "bold"),
            width=15,
            bg="#fff",
            fg="#000",
        ).grid(row=1, column=1, padx=15, pady=5)

        # password label and password entry box
        passwordLabel = Label(
            frame1,
            text="PASSWORD :",
            font=("times new roman", 18, "bold"),
            width=15,
            bg="#fff",
            fg="#000",
        ).grid(row=2, column=0, padx=15, pady=5)

        passwordEntry = Entry(
            frame1,
            textvariable=password,
            show="*",
            font=("times new roman", 18, "bold"),
            width=15,
            bg="#fff",
            fg="#000",
        ).grid(row=2, column=1, padx=15, pady=5)

        # login button
        ownerloginButton = Button(
            frame1,
            text="Login as Owner",
            command=self.owner_login,
            font=("times new roman", 18, "bold"),
            width=15,
            bg="green",
            fg="#000",
        ).grid(row=3, column=0, columnspan=2, pady=5)

        employeeloginButton = Button(
            frame1,
            text="Login as Employee",
            command=self.employee_login,
            font=("times new roman", 18, "bold"),
            width=15,
            bg="yellow",
            fg="#000",
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # find customer button
        salesReportButton = Button(
            frame1,
            text="View Sales Report",
            command=self.employee_login_2,
            font=("times new roman", 18, "bold"),
            width=15,
            bg="blue",
            fg="#000",
        ).grid(row=5, column=0, columnspan=2, pady=5)

        # quit button
        quitButton = Button(
            frame1,
            text="Quit Application",
            command=self.master.destroy,
            font=("times new roman", 18, "bold"),
            width=15,
            bg="red",
            fg="#000",
        ).grid(row=6, column=0, columnspan=2, pady=5)

    def owner_login(self):
        uname = username.get()
        pwd = password.get()

        if uname == "" and pwd == "":
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
            # self.give_access_to_owner()
        elif uname == "admin" and pwd == "1234":
            self.give_access_to_owner()
        else:
            messagebox.showerror(
                "Error", "Invalid Username or Password", parent=self.master
            )

        username.set("")
        password.set("")

    def give_access_to_owner(self):
        self.newwindow = Toplevel(self.master)
        self.newwindow.state("zoomed")
        self.newwindow.config(background="#fff")
        self.app = owner.Owner_App(self.newwindow)

    def employee_login(self):
        uname = username.get()
        pwd = password.get()

        if uname == "" and pwd == "":
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
        elif uname == "admin" and pwd == "1234":
            self.give_access_to_employee()
        else:
            collection = database["employee_details"]
            data = collection.find_one({"emp_id": uname, "emp_login_pwd": pwd})
            if str(data) == "None":
                messagebox.showerror(
                    "Error", "Invalid Username or Password", parent=self.master
                )
            else:
                self.give_access_to_employee()

        username.set("")
        password.set("")

    def give_access_to_employee(self):
        self.newwindow = Toplevel(self.master)
        self.newwindow.state("zoomed")
        self.newwindow.config(background="#fff")
        self.app = bill.Bill_App(self.newwindow)

    def employee_login_2(self):
        uname = username.get()
        pwd = password.get()

        if uname == "" and pwd == "":
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
        elif uname == "admin" and pwd == "1234":
            self.find_customer_details()
        else:
            collection = database["employee_details"]
            data = collection.find_one({"emp_id": uname, "emp_login_pwd": pwd})
            if str(data) == "None":
                messagebox.showerror(
                    "Error", "Invalid Username or Password", parent=self.master
                )
            else:
                self.find_customer_details()

        username.set("")
        password.set("")

    def find_customer_details(self):
        self.newwindow = Toplevel(self.master)
        self.newwindow.state("zoomed")
        self.newwindow.config(background="#abcdef")
        self.app = customer.Customer_App(self.newwindow)
