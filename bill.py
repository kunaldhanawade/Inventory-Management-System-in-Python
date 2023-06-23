from tkinter import *
from tkinter import messagebox
import random
from tkcalendar import *
from tkinter import ttk
from datetime import date, datetime

# database connection
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
database = client["my_inventory"]

class Bill_App:
    def __init__(self, master):
        self.master = master
        master.title("Owner")

        title = Label(
            self.master,
            text="BILLING AREA",
            bd=12,
            relief=GROOVE,
            bg="#0530da",
            fg="white",
            font=("times new roman", 30, "bold"),
            pady=2,
        ).place(width=self.master.winfo_screenwidth())

        F1 = Frame(
            self.master,
            bd=10,
            relief=GROOVE,
            bg="#fedcba",
        )
        F1.place(x=0, y=80, width=(self.master.winfo_screenwidth() / 2) - 5, height=568)

        global product_id, product_category, customer_name, customer_phone_no, purchase_item, purchase_quantity, bill_no, tree
        product_id = StringVar()
        product_category = StringVar()
        customer_name = StringVar()
        customer_phone_no = StringVar()
        bill_no = StringVar()
        x = random.randint(1000, 9999)
        bill_no.set(str(x))
        purchase_item = StringVar()
        purchase_quantity = StringVar()

        purchase_item.set("Enter Quantity for Purchasing\n__________ for Rs. ___")

        product_id_lbl = Label(
            F1,
            text="FIND PRODUCT DETAILS BY\nID",
            font=("times new roman", 18, "bold"),
            bg="#fedcba",
        ).grid(sticky=W, row=0, column=0, padx=20, pady=5)

        product_id_txt = Entry(
            F1, width=15, textvariable=product_id, font="arial 15", bd=7, relief=SUNKEN
        ).grid(sticky=W, row=0, column=1, padx=5)

        get_stock_details_by_id_btn = Button(
            F1,
            text="Get Product Details",
            command=self.get_stock_details_by_id,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=1, column=1, padx=10, pady=10)

        product_id_lbl = Label(
            F1,
            text="FIND PRODUCT DETAILS BY\nCATEGORY",
            font=("times new roman", 18, "bold"),
            bg="#fedcba",
        ).grid(sticky=W, row=2, column=0, padx=20, pady=5)

        categories = ["Dairy Products", "Drinks", "Sweets"]
        product_category.set(categories[0])

        category_dropdown = OptionMenu(F1, product_category, *categories).grid(
            sticky=W, row=2, column=1, padx=20, pady=5
        )

        get_stock_details_by_category_btn = Button(
            F1,
            text="Get Product Details",
            command=self.get_stock_details_by_category,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=3, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")

        tree_frame = Frame(
            F1,
            bg="#fedcba",
        )
        tree_frame.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        tree = ttk.Treeview(
            tree_frame,
            column=("Product ID", "Product Name", "Product Quantity", "Product Price"),
            show="headings",
            height=5,
        )
        tree.column("# 1", anchor=CENTER, width=140)
        tree.heading("# 1", text="Product ID")
        tree.column("# 2", anchor=CENTER, width=140)
        tree.heading("# 2", text="Product Name")
        tree.column("# 3", anchor=CENTER, width=140)
        tree.heading("# 3", text="Product Quantity")
        tree.column("# 4", anchor=CENTER, width=140)
        tree.heading("# 4", text="Product Price")
        tree.bind("<ButtonRelease-1>", self.selectItem)

        tree.pack(side="left", pady=5)

        vertical_scrollbar = Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview,
        )
        vertical_scrollbar.pack(side="left", fill=Y)

        tree.configure(yscrollcommand=vertical_scrollbar.set)

        purchase_item_lbl = Label(
            F1,
            textvariable=purchase_item,
            font=("times new roman", 18, "bold"),
            bg="#fedcba",
        ).grid(sticky=W, row=5, column=0, padx=20, pady=5)

        purchase_qantity_txt = Entry(
            F1,
            width=15,
            textvariable=purchase_quantity,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=5, column=1, padx=5)

        add_product_btn = Button(
            F1,
            text="Add Product",
            command=self.add_product,
            width=20,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=6, column=1, padx=10, pady=10)

        F2 = Frame(
            self.master,
            bd=10,
            relief=GROOVE,
            bg="#789",
        )
        F2.place(
            x=(self.master.winfo_screenwidth() / 2) + 5,
            y=80,
            width=(self.master.winfo_screenwidth() / 2) - 5,
            height=568,
        )

        customer_name_lbl = Label(
            F2,
            text="Customer Name :",
            font=("times new roman", 18, "bold"),
            bg="#789",
        ).grid(sticky=W, row=0, column=0, padx=20, pady=10)

        customer_name_txt = Entry(
            F2,
            width=15,
            textvariable=customer_name,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=0, column=1, pady=5)

        customer_phone_no_lbl = Label(
            F2,
            text="Customer Phone No. :",
            font=("times new roman", 18, "bold"),
            bg="#789",
        ).grid(sticky=W, row=1, column=0, padx=20, pady=10)

        customer_phone_no_txt = Entry(
            F2,
            width=15,
            textvariable=customer_phone_no,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=1, column=1, pady=5)

        bill_no_lbl = Label(
            F2,
            text="Bill No. :",
            font=("times new roman", 18, "bold"),
            bg="#789",
        ).grid(sticky=W, row=2, column=0, padx=20, pady=5)

        bill_no_txt = Label(
            F2,
            width=15,
            textv=bill_no,
            font="arial 15",
            bd=7,
            relief=SUNKEN,
        ).grid(sticky=W, row=2, column=1, padx=5)

        textarea_frame = Frame(
            F2,
            bg="#789",
        )
        textarea_frame.grid(sticky=W, row=3, column=0, rowspan=4, padx=10, pady=15)

        self.bill_textarea = Text(
            textarea_frame,
            height=23,
            width=45,
        )
        self.bill_textarea.pack(side="left", pady=5)

        vertical_scrollbar = Scrollbar(
            textarea_frame,
            orient="vertical",
            command=self.bill_textarea.yview,
        )
        vertical_scrollbar.pack(side="left", fill=Y)

        self.bill_textarea.configure(yscrollcommand=vertical_scrollbar.set)

        generate_bill_btn = Button(
            F2,
            text="Generate Bill",
            command=self.generate_bill,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=3, column=1, padx=10, pady=10)

        clear_bill_btn = Button(
            F2,
            text="Clear Bill",
            command=self.clear_bill,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=4, column=1, padx=10, pady=10)

        save_bill_btn = Button(
            F2,
            text="Save Bill",
            command=self.save_bill,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=5, column=1, padx=10, pady=10)

        exit_btn = Button(
            F2,
            text="Exit",
            command=self.master.destroy,
            width=15,
            bd=7,
            font="arial 12 bold",
        ).grid(sticky=W, row=6, column=1, padx=10, pady=10)

    global items_list, total
    items_list = []
    total = 0

    def get_stock_details_by_id(self):
        global values

        tree.delete(*tree.get_children())

        collection = database["stock_details"]
        for data in collection.find():
            if data["product_id"] == product_id.get():
                purchase_item.set(
                    f"Enter Quantity for Purchasing\n{data['product_name']} for Rs. {data['product_price']}"
                )
                values = [
                    data["product_id"],
                    data["product_name"],
                    data["product_quantity"],
                    data["product_price"],
                ]
                tree.insert(
                    "",
                    "end",
                    text="1",
                    values=(
                        data["product_id"],
                        data["product_name"],
                        data["product_quantity"],
                        data["product_price"],
                    ),
                )

    def get_stock_details_by_category(self):
        tree.delete(*tree.get_children())

        collection = database["stock_details"]
        for data in collection.find():
            if data["product_type"] == product_category.get():
                tree.insert(
                    "",
                    "end",
                    text="1",
                    values=(
                        data["product_id"],
                        data["product_name"],
                        data["product_quantity"],
                        data["product_price"],
                    ),
                )

    def selectItem(self, a):
        global values
        curItem = tree.focus()
        items = tree.item(curItem)
        values = items["values"]
        purchase_item.set(
            f"Enter Quantity for Purchasing\n{values[1]} for Rs. {values[3]}"
        )

    def add_product(self):
        global values
        if (
            purchase_item.get()
            == "Enter Quantity for Purchasing\n__________ for Rs. ___"
            or purchase_quantity.get() == ""
        ):
            messagebox.showerror(
                "Error", "Select a Product to Purchase", parent=self.master
            )
        else:
            one_item = [values[1], values[3], purchase_quantity.get(), values[0]]
            items_list.append(one_item)
            purchase_item.set("")
            purchase_quantity.set("")

    def generate_bill(self):
        global total, grand_total, date, time
        now = datetime.now()
        date = now.strftime("%d / %m / %Y")
        time = now.strftime("%H : %M : %S")

        if items_list == []:
            messagebox.showerror("Error", "No Products Added", parent=self.master)
        elif customer_name.get() == "" or customer_phone_no.get() == "":
            messagebox.showerror(
                "Error", "Enter Customer Name and Phone Number", parent=self.master
            )
        elif len(customer_phone_no.get()) != 10:
            messagebox.showerror("Error", "Invalid Phone Number", parent=self.master)
            customer_phone_no.set("")
        else:
            self.bill_textarea.delete(1.0, END)
            self.bill_textarea.insert(END, "\t\tTIWARI DAIRY")
            self.bill_textarea.insert(END, f"\n\nBill Number    : \t\t{bill_no.get()}")
            self.bill_textarea.insert(END, f"\nBilling Date   : \t\t{date}")
            self.bill_textarea.insert(END, f"\nBilling Time   : \t\t{time}")
            self.bill_textarea.insert(
                END, f"\nCustomer Name  : \t\t{customer_name.get()}"
            )
            self.bill_textarea.insert(
                END, f"\nCustomer Phone : \t\t{customer_phone_no.get()}"
            )
            self.bill_textarea.insert(
                END, "\n==========================================="
            )
            self.bill_textarea.insert(END, "\nProduct\t\tPrice\tQuantity\tAmount")
            self.bill_textarea.insert(
                END, "\n___________________________________________"
            )

            for x in items_list:
                rate = float(x[1]) * float(x[2])
                self.bill_textarea.insert(END, f"\n{x[0]}\t\t{x[1]}\t{x[2]}\t\t{rate}")
                total = total + rate
            taxes = total * 0.12
            grand_total = total + taxes
            self.bill_textarea.insert(
                END, "\n___________________________________________"
            )
            self.bill_textarea.insert(END, f"\nTotal       : \t\t{total}")
            self.bill_textarea.insert(END, f"\nTaxes (12%) : \t\t{taxes}")
            self.bill_textarea.insert(
                END, "\n___________________________________________"
            )
            self.bill_textarea.insert(END, f"\nGrand Total : \t\t{grand_total}")
            self.bill_textarea.insert(
                END, "\n==========================================="
            )
            self.bill_textarea.insert(
                END, "\nThank you for purchasing... Please visit again:)"
            )

    def save_bill(self):
        bill_details = self.bill_textarea.get(1.0, END)
        ask = messagebox.askyesno(
            "Save Bill?", "Do you want to SAVE the bill?", parent=self.master
        )
        if ask > 0:
            file = open("bills/" + str(bill_no.get()) + ".txt", "w")
            file.write(bill_details)
            file.close
            messagebox.showinfo(
                "Note:", f"Bill {bill_no.get()} Saved Successfully", parent=self.master
            )
            collection = database["stock_details"]
            for x in items_list:
                xyz = collection.find_one({"product_id": str(x[3])})

                myquery = {
                    "product_id": str(x[3]),
                }
                newvalue = {
                    "$set": {
                        "product_quantity": str(
                            float(xyz["product_quantity"]) - float(x[2])
                        ),
                    }
                }
                collection.update_one(myquery, newvalue)

            billing_date = date + " - " + time

            record = {
                "bill_no": bill_no.get(),
                "billing_date": billing_date,
                "customer_name": customer_name.get(),
                "customer_phone_no": customer_phone_no.get(),
                "products_bought": items_list,
                "total": total,
                "grand_total": grand_total,
            }
            collection = database["sales_details"]
            collection.insert_one(record)
            messagebox.showinfo(
                "Note",
                "Data Saved Successfully",
                parent=self.master,
            )

            self.clear_bill()
        else:
            return

    def clear_bill(self):
        global items_list, total, grand_total
        customer_name.set("")
        customer_phone_no.set("")
        items_list = []
        total = 0
        grand_total = 0.0
        self.bill_textarea.delete(1.0, END)
