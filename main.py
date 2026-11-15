"""Household Expense Splitter - application entry point."""
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from ui import COLORS, configure_styles, FONT
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.dashboard import DashboardPage
from pages.members import MembersPage
from pages.add_expense import AddExpensePage
from pages.expense_history import ExpenseHistoryPage
from pages.split_summary import SplitSummaryPage

class HouseholdExpenseApp:
    PAGES={"Dashboard":("dashboard",DashboardPage),"Members":("members",MembersPage),"Add expense":("add_expense",AddExpensePage),"Expense history":("expense_history",ExpenseHistoryPage),"Split summary":("split_summary",SplitSummaryPage)}
    def __init__(self,root):
        self.root=root; self.db=Database(); self.user=None; self.current_page=None
        root.title("Household Expense Splitter | Shared finances, made clear")
        root.geometry("1280x820"); root.minsize(1050,700); root.configure(bg=COLORS["bg"])
        root.protocol("WM_DELETE_WINDOW",self.on_close)
        configure_styles(root)
        self.container=ttk.Frame(root); self.container.pack(fill="both",expand=True)
        self.show_auth("login")

    def clear(self):
        for widget in self.container.winfo_children(): widget.destroy()

    def show_auth(self,kind):
        self.user=None; self.current_page=None; self.clear()
        page=(LoginPage if kind=="login" else RegisterPage)(self.container,self)
        page.pack(fill="both",expand=True)

    def show_login(self): self.show_auth("login")
    def show_register(self): self.show_auth("register")

    def login_success(self,user):
        self.user=user; self.show_app_page("Dashboard")

    def show_app_page(self,name,expense_id=None):
        if not self.user: self.show_login(); return
        self.current_page=name; self.clear()
        shell=tk.Frame(self.container,bg=COLORS["bg"]); shell.pack(fill="both",expand=True)
        sidebar=tk.Frame(shell,bg=COLORS["navy"],width=230); sidebar.pack(side="left",fill="y"); sidebar.pack_propagate(False)
        brand=tk.Frame(sidebar,bg=COLORS["navy"],padx=20,pady=24); brand.pack(fill="x")
        tk.Label(brand,text="◈  HOMEWISE",bg=COLORS["navy"],fg="white",font=(FONT,17,"bold")).pack(anchor="w")
        tk.Label(brand,text="HOUSEHOLD EXPENSES",bg=COLORS["navy"],fg="#9FB2C9",font=(FONT,8,"bold")).pack(anchor="w",pady=(5,0))
        tk.Frame(sidebar,bg="#344B69",height=1).pack(fill="x",padx=18,pady=(8,18))
        tk.Label(sidebar,text="WORKSPACE",bg=COLORS["navy"],fg="#8297B0",font=(FONT,8,"bold")).pack(anchor="w",padx=20,pady=(0,8))
        for label,(key,_klass) in self.PAGES.items():
            ttk.Button(sidebar,text=("▦   " if label=="Dashboard" else "♙   " if label=="Members" else "＋   " if label=="Add expense" else "≡   " if label=="Expense history" else "◫   ")+label,
                style="NavActive.TButton" if label==name else "Nav.TButton",command=lambda n=label:self.show_app_page(n)).pack(fill="x",padx=10,pady=2)
        spacer=tk.Frame(sidebar,bg=COLORS["navy"]); spacer.pack(fill="both",expand=True)
        tk.Frame(sidebar,bg="#344B69",height=1).pack(fill="x",padx=18,pady=(10,12))
        tk.Label(sidebar,text=f"SIGNED IN AS\n{self.user['username']}",bg=COLORS["navy"],fg="#D6E0EC",font=(FONT,9),justify="left").pack(anchor="w",padx=20,pady=(0,12))
        ttk.Button(sidebar,text="↪   Log out",style="Nav.TButton",command=self.logout).pack(fill="x",padx=10,pady=(0,16))
        main=tk.Frame(shell,bg=COLORS["bg"]); main.pack(side="left",fill="both",expand=True)
        top=tk.Frame(main,bg="white",height=58,highlightbackground=COLORS["line"],highlightthickness=1); top.pack(fill="x"); top.pack_propagate(False)
        tk.Label(top,text=f"{name}",bg="white",fg=COLORS["navy"],font=(FONT,11,"bold")).pack(side="left",padx=28)
        tk.Label(top,text="LOCAL WORKSPACE  •  BHUTAN NGULTRUM (Nu.)",bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).pack(side="right",padx=25)
        content=tk.Frame(main,bg=COLORS["bg"],padx=28,pady=24); content.pack(fill="both",expand=True)
        _key,klass=self.PAGES[name]
        page=klass(content,self,expense_id) if name=="Add expense" else klass(content,self); page.pack(fill="both",expand=True)

    def refresh_current(self):
        self.show_app_page(self.current_page or "Dashboard")

    def logout(self):
        if messagebox.askyesno("Log out","Are you sure you want to log out of this account?"):
            self.show_login()

    def on_close(self):
        self.db.close(); self.root.destroy()

if __name__=="__main__":
    root=tk.Tk(); app=HouseholdExpenseApp(root); root.mainloop()
