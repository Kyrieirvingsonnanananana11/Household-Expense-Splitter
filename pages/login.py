import tkinter as tk
from tkinter import ttk,messagebox
from authentication import verify_password
from ui import COLORS,FONT

class LoginPage(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=COLORS["bg"]); self.app=app
        left=tk.Frame(self,bg=COLORS["navy"],width=470); left.pack(side="left",fill="y"); left.pack_propagate(False)
        tk.Label(left,text="◈  HOMEWISE",bg=COLORS["navy"],fg="white",font=(FONT,25,"bold")).pack(anchor="w",padx=48,pady=(75,18))
        tk.Label(left,text="Shared expenses.\nClearer decisions.",bg=COLORS["navy"],fg="white",font=(FONT,27,"bold"),justify="left").pack(anchor="w",padx=48,pady=(30,12))
        tk.Label(left,text="Keep track of household spending,\nsee who paid, and understand each\nperson's fair share.",bg=COLORS["navy"],fg="#B9C8D9",font=(FONT,12),justify="left",pady=4).pack(anchor="w",padx=48,pady=10)
        tk.Label(left,text="PRIVATE LOCAL ACCOUNTS  •  SIMPLE EQUAL SPLITS",bg=COLORS["navy"],fg="#91A8C1",font=(FONT,8,"bold")).pack(side="bottom",anchor="w",padx=48,pady=35)
        right=tk.Frame(self,bg=COLORS["bg"]); right.pack(side="left",fill="both",expand=True)
        card=tk.Frame(right,bg="white",padx=42,pady=40,highlightbackground=COLORS["line"],highlightthickness=1); card.place(relx=.5,rely=.5,anchor="center")
        tk.Label(card,text="Welcome back",bg="white",fg=COLORS["navy"],font=(FONT,23,"bold")).pack(anchor="w")
        tk.Label(card,text="Sign in to continue to your workspace.",bg="white",fg=COLORS["muted"],font=(FONT,10)).pack(anchor="w",pady=(5,26))
        self.username=tk.StringVar(); self.password=tk.StringVar()
        tk.Label(card,text="USERNAME",bg="white",fg=COLORS["text"],font=(FONT,8,"bold")).pack(anchor="w")
        u=ttk.Entry(card,textvariable=self.username,width=39); u.pack(fill="x",pady=(7,17),ipady=3)
        tk.Label(card,text="PASSWORD",bg="white",fg=COLORS["text"],font=(FONT,8,"bold")).pack(anchor="w")
        pw=ttk.Entry(card,textvariable=self.password,show="•",width=39); pw.pack(fill="x",pady=(7,22),ipady=3); pw.bind("<Return>",lambda _e:self.login())
        ttk.Button(card,text="Sign in",style="Primary.TButton",command=self.login).pack(fill="x")
        tk.Label(card,text="New to Homewise?",bg="white",fg=COLORS["muted"],font=(FONT,9)).pack(pady=(22,4))
        ttk.Button(card,text="Create an account",command=self.app.show_register).pack(fill="x")
        u.focus_set()
    def login(self):
        username=self.username.get().strip(); password=self.password.get()
        if not username or not password: messagebox.showwarning("Missing details","Enter your username and password."); return
        user=self.app.db.get_user(username)
        if not user or not verify_password(password,user["password_hash"],user["salt"]): messagebox.showerror("Sign-in failed","The username or password is incorrect."); return
        self.app.login_success(user)
