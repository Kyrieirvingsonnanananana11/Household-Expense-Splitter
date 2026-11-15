import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import csv
from validators import validate_date
from ui import COLORS,FONT,page_heading,make_card,build_tree,money

class ExpenseHistoryPage(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent); self.app=app; self.uid=app.user["user_id"]
        page_heading(self,"Expense history","Search, review, edit, and export your household transactions.",ttk.Button(self,text="＋  Add expense",style="Primary.TButton",command=lambda:app.show_app_page("Add expense")))
        filters=make_card(self,14); filters.pack(fill="x",pady=(0,14))
        tk.Label(filters,text="SEARCH",bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).grid(row=0,column=0,sticky="w",padx=(0,8))
        self.search=tk.StringVar(); ttk.Entry(filters,textvariable=self.search,width=24).grid(row=1,column=0,sticky="ew",padx=(0,14),pady=(5,0))
        tk.Label(filters,text="CATEGORY",bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).grid(row=0,column=1,sticky="w",padx=(0,8))
        self.category=tk.StringVar(value="All"); cats=["All"]+[r["category_name"] for r in app.db.get_categories()]
        ttk.Combobox(filters,textvariable=self.category,values=cats,state="readonly",width=17).grid(row=1,column=1,sticky="ew",padx=(0,14),pady=(5,0))
        tk.Label(filters,text="FROM DATE",bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).grid(row=0,column=2,sticky="w")
        self.date_from=tk.StringVar(); ttk.Entry(filters,textvariable=self.date_from,width=14).grid(row=1,column=2,sticky="ew",padx=(0,14),pady=(5,0))
        tk.Label(filters,text="TO DATE",bg="white",fg=COLORS["muted"],font=(FONT,8,"bold")).grid(row=0,column=3,sticky="w")
        self.date_to=tk.StringVar(); ttk.Entry(filters,textvariable=self.date_to,width=14).grid(row=1,column=3,sticky="ew",padx=(0,14),pady=(5,0))
        ttk.Button(filters,text="Apply filters",style="Primary.TButton",command=self.refresh).grid(row=1,column=4,pady=(5,0))
        ttk.Button(filters,text="Clear",command=self.clear_filters).grid(row=1,column=5,padx=(7,0),pady=(5,0))
        filters.grid_columnconfigure(0,weight=2); filters.grid_columnconfigure(1,weight=1)
        panel=make_card(self,14); panel.pack(fill="both",expand=True)
        top=tk.Frame(panel,bg="white"); top.pack(fill="x",pady=(0,10))
        tk.Label(top,text="All transactions",bg="white",fg=COLORS["navy"],font=(FONT,12,"bold")).pack(side="left")
        self.count=tk.StringVar(value="0 records"); tk.Label(top,textvariable=self.count,bg="white",fg=COLORS["muted"],font=(FONT,9)).pack(side="right")
        wrap,self.tree=build_tree(panel,("date","description","category","amount","payer"),(105,220,130,130,150),12); wrap.pack(fill="both",expand=True)
        bar=tk.Frame(panel,bg="white"); bar.pack(fill="x",pady=(12,0))
        ttk.Button(bar,text="Edit selected",command=self.edit).pack(side="left")
        ttk.Button(bar,text="Delete selected",style="Danger.TButton",command=self.delete).pack(side="left",padx=8)
        ttk.Button(bar,text="Export CSV",command=self.export).pack(side="right")
        self.total=tk.StringVar(value="Filtered total: Nu. 0.00"); tk.Label(bar,textvariable=self.total,bg="white",fg=COLORS["navy"],font=(FONT,10,"bold")).pack(side="right",padx=15)
        self.refresh()
    def _rows(self):
        start=self.date_from.get().strip(); end=self.date_to.get().strip()
        if start: start=validate_date(start)
        if end: end=validate_date(end)
        if start and end and start>end: raise ValueError("The From Date cannot be later than the To Date.")
        return self.app.db.get_expenses(self.uid,self.search.get(),self.category.get(),start,end)
    def refresh(self):
        try: rows=self._rows()
        except ValueError as e: messagebox.showwarning("Invalid filter",str(e)); return
        self.tree.delete(*self.tree.get_children()); total=0
        for r in rows:
            total+=float(r["amount"]); self.tree.insert("","end",iid=str(r["expense_id"]),values=(r["expense_date"],r["description"],r["category_name"],f"{r['amount']:,.2f}",r["name"]))
        self.count.set(f"{len(rows)} record(s)"); self.total.set(f"Filtered total: {money(total)}")
    def clear_filters(self):
        self.search.set(""); self.category.set("All"); self.date_from.set(""); self.date_to.set(""); self.refresh()
    def edit(self):
        selected=self.tree.selection()
        if not selected: messagebox.showinfo("Select a transaction","Choose an expense to edit."); return
        self.app.show_app_page("Add expense",int(selected[0]))
    def delete(self):
        selected=self.tree.selection()
        if not selected: messagebox.showinfo("Select a transaction","Choose an expense to delete."); return
        if messagebox.askyesno("Delete expense","Permanently delete the selected expense?"):
            self.app.db.delete_expense(self.uid,int(selected[0])); self.refresh()
    def export(self):
        try: rows=self._rows()
        except ValueError as e: messagebox.showwarning("Invalid filter",str(e)); return
        if not rows: messagebox.showinfo("Nothing to export","There are no transactions in the current filtered view."); return
        path=filedialog.asksaveasfilename(title="Export expense history",defaultextension=".csv",filetypes=[("CSV files","*.csv")],initialfile="household_expenses.csv")
        if not path: return
        try:
            with open(path,"w",newline="",encoding="utf-8-sig") as f:
                writer=csv.writer(f); writer.writerow(["Date","Description","Category","Amount (Nu.)","Paid by"])
                for r in rows: writer.writerow([r["expense_date"],r["description"],r["category_name"],f"{float(r['amount']):.2f}",r["name"]])
        except OSError as e: messagebox.showerror("Export failed",f"Could not save the file.\n{e}"); return
        messagebox.showinfo("Export complete",f"Your CSV file was saved to:\n{path}")
