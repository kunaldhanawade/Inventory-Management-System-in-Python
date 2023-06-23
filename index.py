import tkinter
from tkinter import *
from tkcalendar import *

# database connection
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
database = client["my_inventory"]

from login import Login

# window
root = tkinter.Tk()
root.title("WELCOME TO DAIRY FARM")
root.state("zoomed")
root.config(background="#000")
app = Login(root)
root.mainloop()