import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3
from authentication import make_password_hash
from validators import validate_username,validate_password
from ui import COLORS,FONT

class RegisterPage(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=COLORS["bg"]); self.app=app
        panel=tk.Frame(self,bg=COLORS["navy"],width=390); panel.pack(side="left",fill="y"); panel.pack_propagate(False)
        tk.Label(panel,text="◈  HOMEWISE",bg=COLORS["navy"],fg="white",font=(FONT,23,"bold")).pack(anchor="w",padx=42,pady=(70,35))
        tk.Label(panel,text="A clearer picture\nof shared spending.",bg=COLORS["navy"],fg="white",font=(FONT,25,"bold"),justify="left").pack(anchor="w",padx=42)
        tk.Label(panel,text="Create your own local account. Your household records are separated from other accounts on this computer.",bg=COLORS["navy"],fg="#B9C8D9",font=(FONT,11),wraplength=290,justify="left").pack(anchor="w",padx=42,pady=18)
        right=tk.Frame(self,bg=COLORS["bg"]); right.pack(side="left",fill="both",expand=True)
        card=tk.Frame(right,bg="white",padx=40,pady=35,highlightbackground=COLORS["line"],highlightthickness=1); card.place(relx=.5,rely=.5,anchor="center")
        tk.Label(card,text="Create your account",bg="white",fg=COLORS["navy"],font=(FONT,22,"bold")).pack(anchor="w")
        tk.Label(card,text="Use a username and a strong password.",bg="white",fg=COLORS["muted"],font=(FONT,10)).pack(anchor="w",pady=(5,22))
        self.username=tk.StringVar(); self.password=tk.StringVar(); self.confirm=tk.StringVar()
        for label,var,secret in [("USERNAME",self.username,False),("PASSWORD (8 CHARACTERS MINIMUM)",self.password,True),("CONFIRM PASSWORD",self.confirm,True)]:
            tk.Label(card,text=label,bg="white",fg=COLORS["text"],font=(FONT,8,"bold")).pack(anchor="w")
            ttk.Entry(card,textvariable=var,show="•" if secret else "",width=39).pack(fill="x",pady=(7,15),ipady=3)
        ttk.Button(card,text="Create account",style="Primary.TButton",command=self.register).pack(fill="x",pady=(5,8))
        ttk.Button(card,text="Back to sign in",command=self.app.show_login).pack(fill="x")
    def register(self):
        try:
            username=validate_username(self.username.get()); password=validate_password(self.password.get())
            if password!=self.confirm.get(): raise ValueError("The passwords do not match.")
            digest,salt=make_password_hash(password); self.app.db.create_user(username,digest,salt)
        except ValueError as err: messagebox.showwarning("Check your details",str(err)); return
        except sqlite3.IntegrityError: messagebox.showwarning("Username unavailable","That username is already registered. Choose another."); return
        messagebox.showinfo("Account created","Your account is ready. Sign in to continue."); self.app.show_login()
