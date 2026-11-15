import tkinter as tk
from tkinter import ttk
from calculations import calculate_balances
from ui import COLORS,FONT,page_heading,make_card,build_tree,money

class SplitSummaryPage(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent); self.app=app; self.uid=app.user["user_id"]
        page_heading(self,"Split summary","See each person's fair share and whether they should receive or contribute money.")
        total=app.db.total_expense(self.uid); members=app.db.paid_per_member(self.uid)
        average=(total/len(members)) if members else 0
        cards=tk.Frame(self,bg=COLORS["bg"]); cards.pack(fill="x",pady=(0,18))
        for title,value,caption in [("HOUSEHOLD TOTAL",money(total),"All saved expenses"),("MEMBERS IN SPLIT",str(len(members)),"Every listed member is included"),("AVERAGE SHARE",money(average),"Equal share before cent adjustment")]:
            c=make_card(cards,16); c.pack(side="left",fill="both",expand=True,padx=(0,12))
            tk.Label(c,text=title,bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).pack(anchor="w")
            tk.Label(c,text=value,bg="white",fg=COLORS["navy"],font=(FONT,19,"bold")).pack(anchor="w",pady=(7,2))
            tk.Label(c,text=caption,bg="white",fg=COLORS["muted"],font=(FONT,8)).pack(anchor="w")
        panel=make_card(self,16); panel.pack(fill="both",expand=True)
        tk.Label(panel,text="Member settlement",bg="white",fg=COLORS["navy"],font=(FONT,12,"bold")).pack(anchor="w",pady=(0,5))
        tk.Label(panel,text="Positive balance = should receive money. Negative balance = should contribute money.",bg="white",fg=COLORS["muted"],font=(FONT,9)).pack(anchor="w",pady=(0,12))
        wrap,tree=build_tree(panel,("member","paid","share","balance","status"),(170,130,130,130,190),12); wrap.pack(fill="both",expand=True)
        self.tree=tree
        for name,paid,share,balance in calculate_balances(members,total):
            status="Receives money" if balance>0 else "Contributes money" if balance<0 else "Settled"
            tree.insert("","end",values=(name,money(paid),money(share),f"{'+' if balance>0 else ''}{money(balance)}",status))
        if not members:
            tk.Label(panel,text="Add household members to prepare a split summary.",bg="white",fg=COLORS["muted"],font=(FONT,10)).pack(anchor="w",pady=16)
        tk.Label(panel,text="Rounding note: when the total cannot be divided into exact cents, the extra cent(s) are assigned in member-list order so that all balances add up to zero.",bg="white",fg=COLORS["muted"],font=(FONT,8),wraplength=900,justify="left").pack(anchor="w",pady=(12,0))
