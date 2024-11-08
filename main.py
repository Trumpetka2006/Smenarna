#!/usr/bin/env python3

from cgitb import text
from os.path import basename, splitext
import tkinter as tk
import requests

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="Hello World")
        self.lbl.pack()

        self.varAuto = tk.BooleanVar()
        self.chboxAuto = tk.Checkbutton(self, text="Automaticky stahovat kurzovní lístek", variable=self.varAuto, command=self.chbtnAutoClick)
        self.chboxAuto.pack()

        self.btnDownload = tk.Button(self, text="Stáhnout kurzovní lístek", command=self.download)
        self.btnDownload.pack()

        self.lblFrame = tk.LabelFrame(self, text="Transakce")
        self.lblFrame.pack(anchor="w", padx=5)
        self.varTransaction = tk.StringVar()
        self.rbtnPurchase = tk.Radiobutton(self.lblFrame, value="purchace", variable=self.varTransaction, text="Nákup")
        self.rbtnPurchase.pack()
        self.rbtnSale = tk.Radiobutton(self.lblFrame, text="Prodej", variable=self.varTransaction, value="sale")
        self.rbtnSale.pack()


        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()
        self.btn2 = tk.Button(self, text="About", command=self.about)
        self.btn2.pack()

    def chbtnAutoClick(self, event=None):
        if self.varAuto.get():
            self.btnDownload.configure(state="disabled")
        else:
            self.btnDownload.configure(state="normal")

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()

    def download(self):
        URL="https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt"
        response = requests.get(URL)
        data = responses.text
        print(data)
        print(type(data))


app = Application()
app.mainloop()
