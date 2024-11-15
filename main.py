#!/usr/bin/env python3

from cgitb import text
from os.path import basename, splitext
import tkinter as tk
from tkinter import LEFT, RIGHT, ttk
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

        self.fee = 4
        self.feemod = 1

        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="Hello World")
        self.lbl.pack()

        self.varAuto = tk.BooleanVar()
        self.currency = tk.StringVar()
        self.ammount = tk.StringVar()
        self.rate = tk.StringVar()
        self.exrate = {}

        self.chboxAuto = tk.Checkbutton(
            self,
            text="Automaticky stahovat kurzovní lístek",
            variable=self.varAuto,
            command=self.chbtnAutoClick,
        )
        self.chboxAuto.pack()

        self.btnDownload = tk.Button(
            self, text="Stáhnout kurzovní lístek", command=self.download
        )
        self.btnDownload.pack()
        
        self.lblFrame = tk.LabelFrame(self, text="Transakce")
        self.lblFrame.pack(anchor="w", padx=5)
        self.varTransaction = tk.StringVar()
        self.rbtnPurchase = tk.Radiobutton(
            self.lblFrame, value="purchace", variable=self.varTransaction, text="Nákup", command=self.changeTransaction
        )
        self.rbtnPurchase.pack()
        self.rbtnSale = tk.Radiobutton(
            self.lblFrame, text="Prodej", variable=self.varTransaction, value="sale", command=self.changeTransaction
        )
        self.rbtnSale.pack()
        
        self.currFrame = tk.LabelFrame(self, text="Mněna")
        self.currFrame.pack(anchor="w", padx=5)
        self.combo = ttk.Combobox(self.currFrame, textvariable=self.currency)
        self.combo["values"] = "Nenalezeno!"
        self.combo.current(0)
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
       
        self.rateFrame = tk.LabelFrame(self, text="Kurz")
        self.amLabel = tk.Label(self.rateFrame, text="CZK")
        self.raLabel = tk.Label(self.rateFrame, text="UNKNOW")
        self.entryAmmount = MyEntry(self.rateFrame,textvariable=self.ammount ,state="readonly")
        self.entryRate = MyEntry(self.rateFrame,textvariable=self.rate , state="readonly")
        self.rateFrame.pack(anchor="w", padx=5)
        self.entryAmmount.grid(row=0)
        self.amLabel.grid(row=0,column=1)
        self.entryRate.grid(row=1)
        self.raLabel.grid(row=1, column=1)

        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()
        self.btn2 = tk.Button(self, text="About", command=self.about)
        self.btn2.pack()

    def on_select(self,event = None):
        selected = self.currency.get()
        print(selected)
        if self.exrate == {}:
            pass
        else:
            info = self.exrate[selected]
            print(self.feemod)
            self.ammount.set(info[0])
            self.rate.set(info[1] * self.feemod)
            self.raLabel.config(text=info[2])
    
    def changeTransaction(self,event = None):
        if self.varTransaction.get() == "purchace":
            self.feemod = 1 - (0.01 * self.fee)
        else:
            self.feemod = 1 + (0.01 * self.fee)
        self.on_select(None)



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
        URL = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt"
        try:
            response = requests.get(URL)
            data = response.text
            with open("kurzovni_listek.txt", "w") as f:
                f.write(data)
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")

        for line in data.splitlines()[2:]:
            country, currency, amount, code, rate = line.split("|")
            self.exrate[f"{country}({code})"] = [float(amount), float(rate), str(code)]
        print(data)
        print(self.exrate)
        self.combo.config(values=list(self.exrate.keys()))


app = Application()
app.mainloop()
