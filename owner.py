from tkinter import *
from tkinter import messagebox
from tkcalendar import *

# database connection
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
database = client["my_inventory"]

class Owner_App:
    def __init__(self, master):
        self.master = master
        master.title("Owner")

        title = Label(
            self.master,
            text="OWNER CONTROLS",
            bd=12,
            relief=GROOVE,
            bg="#0530da",
            fg="white",
            font=("times new roman", 30, "bold"),
            pady=2,
        ).pack(fill=X)

        #### owner details frame####
        F1 = LabelFrame(
            self.master,
            bd=10,
            relief=GROOVE,
            text="Stock Details",
            font=("times new roman", 15, "bold"),
            bg="#123456",
            fg="gold",
        )
        F1.place(x=0, y=80, width=(self.master.winfo_screenwidth() / 2) - 5, height=568)

        # variables
        global product_id, product_name, product_type, product_quantity, product_price, data
        product_id = StringVar()
        product_name = StringVar()
        product_type = StringVar()
        product_quantity = StringVar()
        product_price = StringVar()

        product_id_lbl = Label(
            F1,
            text="PRODUCT ID :",
            font=("times new roman", 18, "bold"),
            bg="#123456",
            fg="white",
        ).grid(sticky=W, row=0, column=0, padx=20, pady=10)

        product_id_txt = Entry(
            F1, width=15, textvariable=product_id, font="arial 15", bd=7, relief=SUNKEN
        ).grid(sticky=W, row=0, column=1, padx=5)

        product_name_lbl = Label(
            F1,
            text="PRODUCT NAME :",
            font=("times new roman", 18, "bold"),
            bg="#123456",
            fg="white",
        ).grid(sticky=W, row=1, column=0, padx=20, pady=10)

        product_name_txt = Entry(
            F1,
            width=15,
            textvariable=product_name,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=1, column=1, padx=5)

        product_type_lbl = Label(
            F1,
            text="PRODUCT TYPE :",
            font=("times new roman", 18, "bold"),
            bg="#123456",
            fg="white",
        ).grid(sticky=W, row=2, column=0, rowspan=3, padx=20, pady=10)

        types = ["Dairy Products", "Sweets", "Drinks"]
        n = 2

        for type in types:
            product_type_btns = Radiobutton(
                F1,
                width=15,
                text=type,
                variable=product_type,
                value=type,
                font="arial 15",
                anchor=W,
                bg="#123456",
                fg="white",
            )
            product_type_btns.deselect()
            product_type_btns.grid(sticky=W, row=n, column=1, padx=5)
            n += 1

        product_quantity_lbl = Label(
            F1,
            text="PRODUCT QUANTITY :",
            font=("times new roman", 18, "bold"),
            bg="#123456",
            fg="white",
        ).grid(sticky=W, row=5, column=0, padx=20, pady=10)

        product_quantity_txt = Entry(
            F1,
            width=15,
            textvariable=product_quantity,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=5, column=1, padx=5)

        product_price_lbl = Label(
            F1,
            text="PRODUCT PRICE :",
            font=("times new roman", 18, "bold"),
            bg="#123456",
            fg="white",
        ).grid(sticky=W, row=6, column=0, padx=20, pady=10)

        product_price_txt = Entry(
            F1,
            width=15,
            textvariable=product_price,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=6, column=1, padx=5)

        add_stock_details_btn = Button(
            F1,
            text="Add Product Details",
            command=self.add_stock_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=8, column=0, padx=10, pady=10)

        show_stock_details_btn = Button(
            F1,
            text="Show Product Details",
            command=self.show_stock_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=8, column=1, padx=10, pady=10)

        update_stock_details_btn = Button(
            F1,
            text="Update Product Details",
            command=self.update_stock_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=9, column=0, padx=10, pady=10)

        clear_stock_details_btn = Button(
            F1,
            text="Clear Product Details",
            command=self.clear_stock_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=9, column=1, padx=10, pady=10)

        F2 = LabelFrame(
            self.master,
            bd=10,
            relief=GROOVE,
            text="Employee Details",
            font=("times new roman", 15, "bold"),
            bg="#654321",
            fg="gold",
        )
        F2.place(
            x=(self.master.winfo_screenwidth() / 2) + 5,
            y=80,
            width=(self.master.winfo_screenwidth() / 2) - 5,
            height=568,
        )

        # variables
        global emp_id, emp_name, emp_age, emp_gender, emp_dob, emp_aadhar, emp_salary, emp_login_pwd
        emp_id = StringVar()
        emp_name = StringVar()
        emp_age = StringVar()
        emp_gender = StringVar()
        emp_dob = StringVar()
        emp_aadhar = StringVar()
        emp_salary = StringVar()
        emp_login_pwd = StringVar()

        emp_id_lbl = Label(
            F2,
            text="EMPLOYEE ID :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=0, column=0, padx=20, pady=10)

        emp_id_txt = Entry(
            F2, width=15, textvariable=emp_id, font="arial 15", bd=7, relief=SUNKEN
        ).grid(sticky=W, row=0, column=1, padx=5)

        emp_name_lbl = Label(
            F2,
            text="EMPLOYEE NAME :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=1, column=0, padx=20, pady=10)

        emp_name_txt = Entry(
            F2, width=15, textvariable=emp_name, font="arial 15", bd=7, relief=SUNKEN
        ).grid(sticky=W, row=1, column=1, padx=5)

        emp_gender_lbl = Label(
            F2,
            text="EMPLOYEE GENDER :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=3, column=0, padx=20, pady=10)

        F3 = Frame(
            F2,
            width=180,
            height=40,
            bg="#654321",
        )
        F3.grid(sticky=W, row=3, column=1, padx=5)

        types = ["M", "F", "NB"]
        emp_gender.set("NB")
        n = 0

        for genders in types:
            gender_btns = Radiobutton(
                F3,
                text=genders,
                variable=emp_gender,
                value=genders,
                font="arial 15",
                anchor=W,
                bg="#654321",
                fg="white",
            )
            gender_btns.grid(sticky=W, row=0, column=n, padx=5)
            n += 1

        emp_dob_lbl = Label(
            F2,
            text="EMPLOYEE DOB :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=4, column=0, padx=20, pady=10)

        emp_dob_selector = DateEntry(
            F2,
            selectmode="day",
            width=23,
            textvariable=emp_dob,
        ).grid(sticky=W, row=4, column=1, padx=5)

        emp_aadhar_lbl = Label(
            F2,
            text="EMPLOYEE AADHAR NO. :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=5, column=0, padx=20, pady=10)

        emp_aadhar_txt = Entry(
            F2, width=15, textvariable=emp_aadhar, font="arial 15", bd=7, relief=SUNKEN
        ).grid(sticky=W, row=5, column=1, padx=5)

        emp_salary_lbl = Label(
            F2,
            text="EMPLOYEE SALARY :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=6, column=0, padx=20, pady=10)

        emp_salary_txt = Entry(
            F2, width=15, textvariable=emp_salary, font="arial 15", bd=7, relief=SUNKEN
        ).grid(sticky=W, row=6, column=1, padx=5)

        emp_login_pwd_lbl = Label(
            F2,
            text="LOGIN PASSWORD :",
            font=("times new roman", 18, "bold"),
            bg="#654321",
            fg="white",
        ).grid(sticky=W, row=7, column=0, padx=20, pady=10)

        emp_login_pwd_txt = Entry(
            F2,
            width=15,
            textvariable=emp_login_pwd,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=7, column=1, padx=5)

        add_employees_btn = Button(
            F2,
            text="Add Employee Details",
            command=self.add_employee_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=8, column=0, padx=10, pady=10)

        show_employees_btn = Button(
            F2,
            text="Show Employee Details",
            command=self.show_employee_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=8, column=1, padx=10, pady=10)

        update_employees_btn = Button(
            F2,
            text="Update Employee Details",
            command=self.update_employee_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=9, column=0, padx=10, pady=10)

        clear_employees_btn = Button(
            F2,
            text="Clear Employee Details",
            command=self.clear_employee_details,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(row=9, column=1, padx=10, pady=10)

    def add_stock_details(self):
        if (
            product_id.get() == ""
            and product_name.get() == ""
            and product_type.get() == ""
            and product_quantity.get() == ""
            and product_price.get() == ""
        ):
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
        elif (
            product_id.get() == ""
            or product_name.get() == ""
            or product_type.get() == ""
            or product_quantity.get() == ""
            or product_price.get() == ""
        ):
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
        else:
            record = {
                "product_id": product_id.get(),
                "product_name": product_name.get(),
                "product_type": product_type.get(),
                "product_quantity": product_quantity.get(),
                "product_price": product_price.get(),
            }
            collection = database["stock_details"]
            collection.insert_one(record)
            messagebox.showinfo(
                "Information", "Data Added Successfully", parent=self.master
            )

        self.clear_stock_details()

    def show_stock_details(self):
        global dict
        collection = database["stock_details"]
        if product_id == "":
            messagebox.showerror(
                "Error", "ID Field cannot be blank.", parent=self.master
            )

        else:
            data = collection.find_one({"product_id": product_id.get()})
            if str(data) == "None":
                messagebox.showerror(
                    "Data Not Found", "Invalid ID Provided", parent=self.master
                )
                self.clear_stock_details()

            else:
                product_id.set(data["product_id"])
                product_name.set(data["product_name"])
                product_type.set(data["product_type"])
                product_quantity.set(data["product_quantity"])
                product_price.set(data["product_price"])

    def update_stock_details(self):
        collection = database["stock_details"]
        if (
            product_id == ""
            or product_name == ""
            or product_type == ""
            or product_quantity == ""
            or product_price == ""
        ):
            messagebox.showerror(
                "Error", "Data Fields cannot be blank.", parent=self.master
            )
        elif product_id != "":
            myquery = {
                "product_id": product_id.get(),
            }

            newvalue = {
                "$set": {
                    "product_name": product_name.get(),
                    "product_type": product_type.get(),
                    "product_quantity": product_quantity.get(),
                    "product_price": product_price.get(),
                }
            }

            collection.update_one(myquery, newvalue)
            messagebox.showinfo(
                "Information", "Data Updated Successfully", parent=self.master
            )

            self.clear_stock_details()

        else:
            messagebox.showerror("Error", "Invalid ID Provided", parent=self.master)

    def clear_stock_details(self):
        product_id.set("")
        product_name.set("")
        product_type.set("Dairy Products")
        product_quantity.set("")
        product_price.set("")

    def add_employee_details(self):
        if (
            emp_id.get() == ""
            and emp_name.get() == ""
            # and emp_age.get() == ""
            and emp_gender.get() == ""
            and emp_dob.get() == ""
            and emp_aadhar.get() == ""
            and emp_salary.get() == ""
            and emp_login_pwd.get() == ""
        ):
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
            self.clear_employee_details()
        elif (
            emp_id.get() == ""
            or emp_name.get() == ""
            # or emp_age.get() == ""
            or emp_gender.get() == ""
            or emp_dob.get() == ""
            or emp_aadhar.get() == ""
            or emp_salary.get() == ""
            or emp_login_pwd.get() == ""
        ):
            messagebox.showerror(
                "Error", "Entry Fields cannot be blank.", parent=self.master
            )
            self.clear_employee_details()
        elif len(emp_aadhar.get()) != 12:
            messagebox.showerror(
                "Error", "Aadhar No. must be 12 digits", parent=self.master
            )
            emp_aadhar.set("")
        else:
            record = {
                "emp_id": emp_id.get(),
                "emp_name": emp_name.get(),
                # "emp_age": emp_age.get(),
                "emp_gender": emp_gender.get(),
                "emp_DOB": emp_dob.get(),
                "emp_aadhar": emp_aadhar.get(),
                "emp_salary": emp_salary.get(),
                "emp_login_pwd": emp_login_pwd.get(),
            }
            collection = database["employee_details"]
            collection.insert_one(record)
            messagebox.showinfo(
                "Information", "Data Added Successfully", parent=self.master
            )
            self.clear_employee_details()

    def show_employee_details(self):
        global dict
        collection = database["employee_details"]
        if emp_id == "":
            messagebox.showerror(
                "Error", "ID Field cannot be blank.", parent=self.master
            )
        else:
            data = collection.find_one({"emp_id": emp_id.get()})
            if str(data) == "None":
                messagebox.showerror(
                    "Data Not Found", "Invalid ID Provided", parent=self.master
                )
                self.clear_employee_details()

            else:
                emp_id.set(data["emp_id"])
                emp_name.set(data["emp_name"])
                # emp_age.set(data["emp_age"])
                emp_gender.set(data["emp_gender"])
                emp_dob.set(data["emp_DOB"])
                emp_aadhar.set(data["emp_aadhar"])
                emp_salary.set(data["emp_salary"])
                emp_login_pwd.set(data["emp_login_pwd"])

    def update_employee_details(self):
        collection = database["employee_details"]
        if (
            emp_id == ""
            or emp_name == ""
            # or emp_age == ""
            or emp_gender == ""
            or emp_dob == ""
            or emp_aadhar == ""
            or emp_salary == ""
            or emp_login_pwd == ""
        ):
            messagebox.showerror(
                "Error", "Data Fields cannot be blank.", parent=self.master
            )
        elif emp_id != "":
            myquery = {
                "emp_id": emp_id.get(),
            }

            newvalue = {
                "$set": {
                    "emp_name": emp_name.get(),
                    # "emp_age": emp_age.get(),
                    "emp_gender": emp_gender.get(),
                    "emp_DOB": emp_dob.get(),
                    "emp_aadhar": emp_aadhar.get(),
                    "emp_salary": emp_salary.get(),
                    "emp_login_pwd": emp_login_pwd.get(),
                }
            }

            collection.update_one(myquery, newvalue)
            messagebox.showinfo(
                "Information", "Data Updated Successfully", parent=self.master
            )
        else:
            messagebox.showerror("Error", "Invalid ID Provided", parent=self.master)

        self.clear_employee_details()

    def clear_employee_details(self):
        emp_id.set("")
        emp_name.set("")
        # emp_age.set("")
        emp_gender.set("")
        emp_dob.set("")
        emp_aadhar.set("")
        emp_salary.set("")
        emp_login_pwd.set("")
