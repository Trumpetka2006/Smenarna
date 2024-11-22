#!/usr/bin/env python3

from cgitb import text
from os.path import basename, splitext
import tkinter as tk
from tkinter import LEFT, RIGHT, ttk
import requests
import math
import datetime as dt
import os
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

        self.lbl = tk.Label(self, text="Chyba")
        btn = tk.Button(self, text="OK", command=self.close)
        self.lbl.pack()
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Smenarna"

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
        self.input = tk.IntVar()
        self.output = tk.IntVar()

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
        self.varTransaction.set("None")
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
        self.amLabel = tk.Label(self.rateFrame, text="UNKNOW")
        self.raLabel = tk.Label(self.rateFrame, text="CZK")
        self.entryAmmount = MyEntry(self.rateFrame,textvariable=self.ammount ,state="readonly")
        self.entryRate = MyEntry(self.rateFrame,textvariable=self.rate , state="readonly")
        self.rateFrame.pack(anchor="w", padx=5)
        self.entryAmmount.grid(row=0)
        self.amLabel.grid(row=0,column=1)
        self.entryRate.grid(row=1)
        self.raLabel.grid(row=1, column=1)

        self.calcFrame = tk.LabelFrame(self, text="Výpočet")
        self.calcInput = MyEntry(self.calcFrame, textvariable=self.input)
        self.calcBtn = tk.Button(self.calcFrame, text="Výpočet", state="disable", command=self.calculate)
        self.calcOutput = MyEntry(self.calcFrame, textvariable=self.output, state = "readonly")
        self.inLabel = tk.Label(self.calcFrame, text="UNKNOW")
        self.ouLabel = tk.Label(self.calcFrame, text="CZK")
        self.calcFrame.pack(anchor="w", padx=5)
        self.calcInput.grid(row=0,column=0)
        self.inLabel.grid(row=0, column=1)
        self.calcBtn.grid(row=2, column=0)
        self.calcOutput.grid(row=1,column=0)
        self.ouLabel.grid(row=1, column=1)

        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack()
        self.btn2 = tk.Button(self, text="About", command=self.about)
        self.btn2.pack()

        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                if f.read() == "1":
                    self.varAuto.set(True)
                    self.btnDownload.config(state="disable")
                else:
                    self.varAuto.set(False)
                f.close()
                print(self.varAuto.get())
        else:
            print("Save dont exist")

        if self.varAuto.get():
            self.download()
        self.load_date()

    def load_date(self):
        if os.path.exists("kurzovni_listek.txt"):
            with open("kurzovni_listek.txt", "r") as f:
                file_date = f.readline()
                f.close()
            print(file_date)
            date = dt.datetime.now()
            if int(file_date[:2]) < date.day -1 or file_date[3:6] != date.strftime("%b").upper() or int(file_date[7:12]) != date.year:
                print("Not up to date!")
                print(date.strftime("%b").upper())

    def on_select(self,event = None):
        self.output.set(0)
        selected = self.currency.get()
        print(selected)
        if self.exrate == {}:
            pass
        else:
            info = self.exrate[selected]
            print(self.feemod)
            self.ammount.set(info[0])
            self.rate.set(info[1] * self.feemod)
            self.amLabel.config(text=info[2])
            self.inLabel.config(text=info[2])
            if self.varTransaction.get() == "purchace" or self.varTransaction.get() == "sale":
                self.calcBtn.config(state= "normal")
    
    def changeTransaction(self,event = None):
        self.output.set(0)
        if self.varTransaction.get() == "purchace":
            self.feemod = 1 - (0.01 * self.fee)
        else:
            self.feemod = 1 + (0.01 * self.fee)
        self.on_select(None)
        if self.exrate != {}:
            self.calcBtn.config(state= "normal")

    def calculate(self, event=None):
        if self.varTransaction.get() == "purchace":
            self.output.set(math.floor((self.input.get()/float(self.ammount.get()))*float(self.rate.get())))
        elif self.varTransaction.get() == "sale":
            self.output.set(math.ceil((self.input.get()/float(self.ammount.get()))*float(self.rate.get())))


    def chbtnAutoClick(self, event=None):
        with open("settings.txt", "w") as f:
            if self.varAuto.get():
                self.btnDownload.configure(state="disabled")
                f.write("1")
                f.close()
                self.download()
            else:
                f.write("0")
                f.close()
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
            print("Falling back to local file")
            errwindow = About(self)
            errwindow.lbl.config(text="Nebylo možné stáhonut kurzovní lístke.\nZkontrolujet přípojení k internetu")
            errwindow.grab_set()

            if os.path.exists("kurzovni_listek.txt"):
                with open("kurzovni_listek.txt", "r") as f:
                    data = f.read()
                    f.close()
            else:
                print("Critical error!")
                self.destroy()

        for line in data.splitlines()[2:]:
            country, currency, amount, code, rate = line.split("|")
            self.exrate[f"{country}({code})"] = [float(amount), float(rate), str(code)]
        print(data)
        print(self.exrate)
        self.combo.config(values=list(self.exrate.keys()))


app = Application()
app.mainloop()
