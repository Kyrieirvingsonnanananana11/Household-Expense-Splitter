import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3
from validators import validate_member_name
from ui import COLORS,FONT,page_heading,make_card,build_tree

class MembersPage(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent); self.app=app; self.uid=app.user["user_id"]
        page_heading(self,"Household members","Add the people whose shared expenses will be included in the split.")
        panel=make_card(self,18); panel.pack(fill="x",pady=(0,16))
        tk.Label(panel,text="Add a member",bg="white",fg=COLORS["navy"],font=(FONT,12,"bold")).pack(anchor="w",pady=(0,10))
        row=tk.Frame(panel,bg="white"); row.pack(fill="x")
        self.name=tk.StringVar(); entry=ttk.Entry(row,textvariable=self.name,width=38); entry.pack(side="left",ipady=3); entry.bind("<Return>",lambda _e:self.add())
        ttk.Button(row,text="＋  Add member",style="Primary.TButton",command=self.add).pack(side="left",padx=10)
        tk.Label(row,text="Use one entry for each person in the household.",bg="white",fg=COLORS["muted"],font=(FONT,8)).pack(side="left",padx=8)
        panel2=make_card(self,16); panel2.pack(fill="both",expand=True)
        tk.Label(panel2,text="Your household",bg="white",fg=COLORS["navy"],font=(FONT,12,"bold")).pack(anchor="w",pady=(0,12))
        wrap,self.tree=build_tree(panel2,("name","status"),(420,180),12); wrap.pack(fill="both",expand=True)
        self.tree.heading("name",text="MEMBER NAME"); self.tree.heading("status",text="RECORD STATUS")
        ttk.Button(panel2,text="Remove selected member",style="Danger.TButton",command=self.remove).pack(anchor="w",pady=(12,0))
        self.refresh()
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.app.db.get_members(self.uid): self.tree.insert("","end",iid=str(row["member_id"]),values=(row["name"],"Included in split"))
    def add(self):
        try: self.app.db.add_member(self.uid,validate_member_name(self.name.get()))
        except ValueError as e: messagebox.showwarning("Check member name",str(e)); return
        except sqlite3.IntegrityError: messagebox.showwarning("Already added","That member is already in this household."); return
        self.name.set(""); self.refresh()
    def remove(self):
        selected=self.tree.selection()
        if not selected: messagebox.showinfo("Select a member","Choose a member from the list first."); return
        member_id=int(selected[0]); name=self.tree.item(selected[0],"values")[0]
        if not messagebox.askyesno("Remove member",f"Remove {name} from this household? A member with recorded expenses cannot be removed."): return
        try: self.app.db.delete_member(self.uid,member_id)
        except sqlite3.IntegrityError: messagebox.showerror("Member is in use","This member has recorded expenses. Delete or reassign those expenses before removing the member."); return
        self.refresh()
