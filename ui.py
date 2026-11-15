"""Shared UI helpers and visual design tokens."""
import tkinter as tk
from tkinter import ttk

COLORS={"navy":"#172B4D","navy2":"#203A5F","teal":"#168C83","teal_dark":"#10736C","bg":"#F4F7FB","surface":"#FFFFFF","text":"#243247","muted":"#718096","line":"#E4EAF1","green":"#16845B","red":"#C44747","amber":"#B7791F","pale_teal":"#E8F5F3","pale_blue":"#EDF3FA"}
FONT="Segoe UI"

def configure_styles(root):
    style=ttk.Style(root)
    try: style.theme_use("clam")
    except tk.TclError: pass
    style.configure("TFrame",background=COLORS["bg"])
    style.configure("TLabel",background=COLORS["bg"],foreground=COLORS["text"],font=(FONT,10))
    style.configure("PageTitle.TLabel",font=(FONT,23,"bold"),foreground=COLORS["navy"])
    style.configure("Subtitle.TLabel",font=(FONT,10),foreground=COLORS["muted"])
    style.configure("Section.TLabel",font=(FONT,12,"bold"),foreground=COLORS["navy"])
    style.configure("CardValue.TLabel",font=(FONT,21,"bold"),foreground=COLORS["navy"])
    style.configure("CardCaption.TLabel",font=(FONT,9),foreground=COLORS["muted"])
    style.configure("TButton",font=(FONT,10,"bold"),padding=(13,9),background=COLORS["surface"])
    style.map("TButton",background=[("active","#EAF0F7")])
    style.configure("Primary.TButton",background=COLORS["teal"],foreground="white",padding=(14,10),borderwidth=0)
    style.map("Primary.TButton",background=[("active",COLORS["teal_dark"]),("disabled","#A8C9C5")],foreground=[("disabled","#F4F7F6")])
    style.configure("Danger.TButton",background="#FCEEEE",foreground=COLORS["red"],padding=(12,8))
    style.configure("Nav.TButton",background=COLORS["navy"],foreground="#D6E0EC",anchor="w",padding=(16,12),borderwidth=0,font=(FONT,10))
    style.map("Nav.TButton",background=[("active",COLORS["navy2"])],foreground=[("active","white")])
    style.configure("NavActive.TButton",background=COLORS["teal"],foreground="white",anchor="w",padding=(16,12),borderwidth=0,font=(FONT,10,"bold"))
    style.configure("TEntry",padding=9,fieldbackground="white")
    style.configure("TCombobox",padding=8,fieldbackground="white")
    style.configure("Treeview",background="white",fieldbackground="white",foreground=COLORS["text"],rowheight=34,font=(FONT,9),borderwidth=0)
    style.configure("Treeview.Heading",background="#EEF2F7",foreground=COLORS["navy"],font=(FONT,9,"bold"),padding=9)
    style.map("Treeview",background=[("selected", "#D9EFEB")],foreground=[("selected",COLORS["navy"])])
    style.configure("TLabelframe",background=COLORS["surface"],bordercolor=COLORS["line"])
    style.configure("TLabelframe.Label",background=COLORS["surface"],foreground=COLORS["navy"],font=(FONT,10,"bold"))

def make_card(parent,padding=18):
    return tk.Frame(parent,bg=COLORS["surface"],highlightbackground=COLORS["line"],highlightthickness=1,padx=padding,pady=padding)

def page_heading(parent,title,subtitle=None,action=None):
    header=tk.Frame(parent,bg=COLORS["bg"]); header.pack(fill="x",pady=(0,20))
    left=tk.Frame(header,bg=COLORS["bg"]); left.pack(side="left",fill="x",expand=True)
    ttk.Label(left,text=title,style="PageTitle.TLabel").pack(anchor="w")
    if subtitle: ttk.Label(left,text=subtitle,style="Subtitle.TLabel").pack(anchor="w",pady=(4,0))
    if action: action.pack(side="right",anchor="e")
    return header

def money(value): return f"Nu. {float(value):,.2f}"

def build_tree(parent,columns,widths,height=10,headings=None):
    wrapper=tk.Frame(parent,bg=COLORS["surface"])
    tree=ttk.Treeview(wrapper,columns=columns,show="headings",height=height)
    headings=headings or [col.replace("_"," ").title() for col in columns]
    for col,heading,width in zip(columns,headings,widths):
        tree.heading(col,text=heading); tree.column(col,width=width,minwidth=70,anchor="w")
    scroll=ttk.Scrollbar(wrapper,orient="vertical",command=tree.yview); tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
    return wrapper,tree
