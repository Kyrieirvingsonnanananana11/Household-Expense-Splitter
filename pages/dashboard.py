import tkinter as tk
from tkinter import ttk
from ui import COLORS,FONT,make_card,page_heading,money,build_tree

class DashboardPage(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent); self.app=app; uid=app.user["user_id"]
        header=page_heading(self,"Good to see you",f"Here is the latest overview for {app.user['username']}'s household.")
        ttk.Button(header,text="＋  Add expense",style="Primary.TButton",command=lambda:app.show_app_page("Add expense")).pack(side="right",anchor="e")
        metrics=tk.Frame(self,bg=COLORS["bg"]); metrics.pack(fill="x",pady=(0,18))
        cards=[("TOTAL SPENDING",money(app.db.total_expense(uid)),"Across all recorded expenses",COLORS["teal"]),("HOUSEHOLD MEMBERS",str(len(app.db.get_members(uid))),"People included in the split",COLORS["navy2"]),("RECORDED EXPENSES",str(app.db.expense_count(uid)),"Transactions saved",COLORS["amber"])]
        for title,value,caption,accent in cards:
            c=make_card(metrics,18); c.pack(side="left",fill="both",expand=True,padx=(0,12)); tk.Frame(c,bg=accent,height=3).pack(fill="x",pady=(0,14))
            tk.Label(c,text=title,bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).pack(anchor="w")
            tk.Label(c,text=value,bg="white",fg=COLORS["navy"],font=(FONT,21,"bold")).pack(anchor="w",pady=(7,2))
            tk.Label(c,text=caption,bg="white",fg=COLORS["muted"],font=(FONT,8)).pack(anchor="w")
        lower=tk.Frame(self,bg=COLORS["bg"]); lower.pack(fill="both",expand=True)
        recent=make_card(lower,16); recent.pack(side="left",fill="both",expand=True,padx=(0,12))
        tk.Label(recent,text="Recent activity",bg="white",fg=COLORS["navy"],font=(FONT,12,"bold")).pack(anchor="w",pady=(0,12))
        wrap,tree=build_tree(recent,("date","description","category","amount"),(95,180,120,115),7); wrap.pack(fill="both",expand=True)
        for r in app.db.recent_expenses(uid): tree.insert("","end",values=(r["expense_date"],r["description"],r["category_name"],f"{r['amount']:,.2f}"))
        if not app.db.expense_count(uid): tk.Label(recent,text="No expenses yet. Add your first expense to get started.",bg="white",fg=COLORS["muted"],font=(FONT,9)).pack(anchor="w",pady=10)
        side=make_card(lower,16); side.pack(side="left",fill="y")
        tk.Label(side,text="Spending by category",bg="white",fg=COLORS["navy"],font=(FONT,12,"bold")).pack(anchor="w")
        tk.Label(side,text="Your largest expense categories",bg="white",fg=COLORS["muted"],font=(FONT,8)).pack(anchor="w",pady=(3,12))
        totals=app.db.category_totals(uid); total=sum(float(x["total"]) for x in totals)
        if not totals: tk.Label(side,text="Category totals will appear\nafter you add expenses.",bg="white",fg=COLORS["muted"],font=(FONT,9),justify="left").pack(anchor="w",pady=12)
        else:
            palette=["#168C83","#416A9C","#D69B36","#8B78B8","#D47761","#5B9B78","#8494A8"]
            for i,row in enumerate(totals[:6]):
                line=tk.Frame(side,bg="white"); line.pack(fill="x",pady=5)
                tk.Label(line,text="●",fg=palette[i%len(palette)],bg="white",font=(FONT,12)).pack(side="left")
                tk.Label(line,text=row["category_name"],fg=COLORS["text"],bg="white",font=(FONT,9)).pack(side="left",padx=6)
                tk.Label(line,text=f"{float(row['total'])/total:.0%}",fg=COLORS["muted"],bg="white",font=(FONT,9,"bold")).pack(side="right")
                bar=tk.Frame(side,bg="#EDF1F6",height=5); bar.pack(fill="x",pady=(0,5)); bar.pack_propagate(False)
                tk.Frame(bar,bg=palette[i%len(palette)],width=max(2,int(180*float(row["total"])/total))).pack(side="left",fill="y")
        ttk.Button(side,text="View full summary →",command=lambda:app.show_app_page("Split summary")).pack(anchor="w",pady=(14,0))
