import tkinter as tk
from tkinter import ttk,messagebox
from datetime import date
from validators import validate_description,validate_amount,validate_date
from ui import COLORS,FONT,page_heading,make_card

class AddExpensePage(ttk.Frame):
    def __init__(self,parent,app,expense_id=None):
        super().__init__(parent); self.app=app; self.uid=app.user["user_id"]; self.expense_id=expense_id
        editing=expense_id is not None
        page_heading(self,"Edit expense" if editing else "Add an expense","Record what was purchased, when it happened, and who paid.")
        panel=make_card(self,24); panel.pack(fill="x",anchor="n")
        tk.Label(panel,text="Expense details",bg="white",fg=COLORS["navy"],font=(FONT,13,"bold")).grid(row=0,column=0,columnspan=2,sticky="w",pady=(0,18))
        self.desc=tk.StringVar(); self.amount=tk.StringVar(); self.category=tk.StringVar(); self.payer=tk.StringVar(); self.expense_date=tk.StringVar(value=date.today().isoformat())
        members=app.db.get_members(self.uid); cats=app.db.get_categories()
        self.member_ids={r["name"]:r["member_id"] for r in members}; self.category_ids={r["category_name"]:r["category_id"] for r in cats}
        self.fields=[]
        self._field(panel,"DESCRIPTION",ttk.Entry(panel,textvariable=self.desc,width=48),1,0)
        self._field(panel,"AMOUNT (Nu.)",ttk.Entry(panel,textvariable=self.amount,width=48),1,1)
        self._field(panel,"CATEGORY",ttk.Combobox(panel,textvariable=self.category,values=list(self.category_ids),state="readonly",width=45),2,0)
        self._field(panel,"PAID BY",ttk.Combobox(panel,textvariable=self.payer,values=list(self.member_ids),state="readonly",width=45),2,1)
        self._field(panel,"EXPENSE DATE (YYYY-MM-DD)",ttk.Entry(panel,textvariable=self.expense_date,width=48),3,0)
        if self.category_ids: self.category.set(next(iter(self.category_ids)))
        if self.member_ids: self.payer.set(next(iter(self.member_ids)))
        if editing:
            row=app.db.get_expense(self.uid,expense_id)
            if row:
                self.desc.set(row["description"]); self.amount.set(f"{row['amount']:.2f}"); self.expense_date.set(row["expense_date"])
                self.category.set(next((n for n,i in self.category_ids.items() if i==row["category_id"]),""))
                self.payer.set(next((n for n,i in self.member_ids.items() if i==row["paid_by"]),""))
        buttons=tk.Frame(panel,bg="white"); buttons.grid(row=8,column=0,columnspan=2,sticky="w",pady=(20,0))
        ttk.Button(buttons,text="Save changes" if editing else "Save expense",style="Primary.TButton",command=self.save).pack(side="left")
        ttk.Button(buttons,text="Cancel",command=lambda:app.show_app_page("Expense history" if editing else "Dashboard")).pack(side="left",padx=8)
        panel.grid_columnconfigure(0,weight=1); panel.grid_columnconfigure(1,weight=1)
        if not members: tk.Label(self,text="Tip: add household members before recording an expense.",bg=COLORS["bg"],fg=COLORS["amber"],font=(FONT,9)).pack(anchor="w",pady=12)
    def _field(self,parent,label,widget,row,col):
        pad=(0,24 if col==0 else 0)
        tk.Label(parent,text=label,bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).grid(row=row*2-1,column=col,sticky="w",padx=pad,pady=(9,4))
        widget.grid(row=row*2,column=col,sticky="ew",padx=pad,pady=(0,7))
    def save(self):
        try:
            desc=validate_description(self.desc.get()); amount=validate_amount(self.amount.get()); when=validate_date(self.expense_date.get())
            if not self.member_ids: raise ValueError("Add at least one household member before saving an expense.")
            if self.category.get() not in self.category_ids: raise ValueError("Choose a category.")
            if self.payer.get() not in self.member_ids: raise ValueError("Choose who paid for this expense.")
            args=(self.uid,desc,amount,self.category_ids[self.category.get()],self.member_ids[self.payer.get()])
            if self.expense_id:
                self.app.db.update_expense(self.uid,self.expense_id,desc,amount,self.category_ids[self.category.get()],self.member_ids[self.payer.get()],when)
            else:
                self.app.db.add_expense(*args,when)
        except ValueError as e: messagebox.showwarning("Check expense details",str(e)); return
        messagebox.showinfo("Saved","Expense details have been saved.")
        self.app.show_app_page("Expense history" if self.expense_id else "Dashboard")
