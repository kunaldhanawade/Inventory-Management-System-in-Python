import tkinter
from tkinter import *
from tkinter import messagebox
import random
from tkcalendar import *
from tkinter import ttk
from datetime import date, datetime
import matplotlib.pyplot as plt

# database connection
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
database = client["my_inventory"]

class Customer_App:
    def __init__(self, master):
        self.master = master
        master.title("Customer")

        global customer_phone_no, customer_bill_no, customer_name, tree
        customer_phone_no = StringVar()
        customer_bill_no = StringVar()
        customer_name = StringVar()

        title = Label(
            self.master,
            text="CUSTOMER PURCHASE DETAILS",
            bd=12,
            relief=GROOVE,
            bg="#fedcba",
            fg="#000",
            font=("times new roman", 30, "bold"),
            pady=2,
        ).pack(fill=X)

        frame1 = LabelFrame(
            self.master,
            bg="#abcdef",
        )
        frame1.pack(pady=5)

        customer_phone_no_lbl = Label(
            frame1,
            text="Customer Phone No. :",
            font=("times new roman", 18, "bold"),
            bg="#abcdef",
        ).grid(row=0, column=0, padx=10, pady=10)

        customer_phone_no_txt = Entry(
            frame1,
            width=15,
            textvariable=customer_phone_no,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(row=0, column=1, padx=10, pady=10)

        get_details_btn = Button(
            frame1,
            text="Get Details",
            command=self.show_details,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).grid(row=0, column=2, padx=10, pady=10)

        customer_name_lbl = Label(
            frame1,
            text="Customer Name :",
            font=("times new roman", 18, "bold"),
            bg="#abcdef",
        ).grid(row=2, column=0, padx=10, pady=10)

        customer_name_txt = Label(
            frame1,
            width=15,
            textvariable=customer_name,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
            bg="white",
        ).grid(row=2, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")

        frame2 = Frame(
            self.master,
            bg="#abcdef",
        )
        frame2.pack(pady=5)

        tree = ttk.Treeview(
            frame2,
            column=(
                "Billing Date",
                "Product ID",
                "Product Name",
                "Product Quantity",
                "Product Price",
            ),
            show="headings",
            height=5,
        )
        tree.column("# 1", anchor=CENTER, width=160)
        tree.heading("# 1", text="Billing Date")
        tree.column("# 2", anchor=CENTER, width=130)
        tree.heading("# 2", text="Product ID")
        tree.column("# 3", anchor=CENTER, width=140)
        tree.heading("# 3", text="Product Name")
        tree.column("# 4", anchor=CENTER, width=140)
        tree.heading("# 4", text="Product Quantity")
        tree.column("# 5", anchor=CENTER, width=130)
        tree.heading("# 5", text="Product Price")

        tree.pack(side="left", pady=5)

        vertical_scrollbar = Scrollbar(
            frame2,
            orient="vertical",
            command=tree.yview,
        )
        vertical_scrollbar.pack(side="left", fill=Y)

        tree.configure(yscrollcommand=vertical_scrollbar.set)

        view_graph = Button(
            self.master,
            text="View Graph",
            command=self.view_graph,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).pack(pady=5)

        clear_tree_btn = Button(
            self.master,
            text="Clear Table",
            command=lambda: tree.delete(*tree.get_children()),
            width=15,
            bd=7,
            font="arial 12 bold",
        ).pack(pady=5)

        exit_btn = Button(
            self.master,
            text="Exit",
            command=self.master.destroy,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).pack(pady=5)

    def show_details(self):
        global dict

        collection = database["stock_details"]
        product_id_list = collection.distinct("product_id")
        dict = {}
        for id in product_id_list:
            dict[id] = 0

        tree.delete(*tree.get_children())
        collection = database["sales_details"]

        if customer_phone_no.get() == "":
            messagebox.showerror("Error", "Enter Phone Number", parent=self.master)
        elif len(customer_phone_no.get()) != 10:
            messagebox.showerror("Error", "Invalid Phone Number", parent=self.master)
            customer_phone_no.set("")
        else:
            for data in collection.find():
                if data["customer_phone_no"] == customer_phone_no.get():
                    customer_bill_no.set(data["bill_no"])
                    customer_name.set(data["customer_name"])
                    for items in data["products_bought"]:
                        tree.insert(
                            "",
                            "end",
                            text="1",
                            values=(
                                data["billing_date"],
                                items[3],
                                items[0],
                                items[2],
                                items[1],
                            ),
                        )

                        for id in product_id_list:
                            if id == str(items[3]):
                                some_variable = float(dict[id])
                                some_variable += float(items[2])
                                dict[id] = some_variable

    def view_graph(self):
        products = list(dict.keys())
        values = list(dict.values())

        plt.bar(products, values, color="maroon", width=0.4)

        plt.xlabel("Products Purchased")
        plt.ylabel("Total Quantity Purchased")
        plt.title("Graph- Products Purchased vs Total Quantity Purchased")
        plt.show()
