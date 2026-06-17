import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
from datetime import date

# ─── Data ───────────────────────────────────────────────────────────────────
DATA_FILE = "task_data.json"
UPLOADS_DIR = "uploaded_projects"
os.makedirs(UPLOADS_DIR, exist_ok=True)

USERS = {
    "manager@task.com":  {"password": "mgr123",    "name": "Rajesh Kumar",  "role": "manager"},
    "arjun@task.com":    {"password": "arjun123",  "name": "Arjun Sharma",  "role": "subordinate"},
    "priya@task.com":    {"password": "priya123",  "name": "Priya Singh",   "role": "subordinate"},
    "rahul@task.com":    {"password": "rahul123",  "name": "Rahul Verma",   "role": "subordinate"},
    "neha@task.com":     {"password": "neha123",   "name": "Neha Patel",    "role": "subordinate"},
}

def load_projects():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return [
        {"id": 1, "title": "Website Redesign",  "desc": "Redesign company homepage with new branding",   "file": "redesign_v2.pdf",   "owner": "Arjun Sharma", "email": "arjun@task.com", "status": "reviewed",  "remark": "Good structure, please add mobile responsiveness section.", "date": "2025-06-10"},
        {"id": 2, "title": "Sales Report Q2",   "desc": "Quarterly sales data analysis and projections", "file": "sales_q2.xlsx",     "owner": "Priya Singh",  "email": "priya@task.com", "status": "approved",  "remark": "Excellent work! Well structured and insightful.",           "date": "2025-06-12"},
        {"id": 3, "title": "App Architecture",  "desc": "Proposed architecture for new mobile app",      "file": "arch_doc.pdf",      "owner": "Rahul Verma",  "email": "rahul@task.com", "status": "pending",   "remark": "",                                                          "date": "2025-06-14"},
        {"id": 4, "title": "Marketing Plan",    "desc": "Q3 marketing strategy and budget allocation",   "file": "marketing_q3.pptx", "owner": "Neha Patel",   "email": "neha@task.com",  "status": "pending",   "remark": "",                                                          "date": "2025-06-15"},
    ]

def save_projects(projects):
    with open(DATA_FILE, "w") as f:
        json.dump(projects, f, indent=2)

# ─── Colours ─────────────────────────────────────────────────────────────────
BG          = "#F5F4FB"
CARD        = "#FFFFFF"
PRIMARY     = "#3C3489"
PRIMARY_H   = "#26215C"
SUCCESS     = "#0F6E56"
DANGER      = "#993C1D"
MUTED       = "#6B6A65"
BORDER      = "#D3D1C7"
TEXT        = "#1A1A18"

REVIEWED_BG = "#CECBF6"; REVIEWED_FG = "#26215C"
APPROVED_BG = "#C0DD97"; APPROVED_FG = "#173404"
REJECTED_BG = "#F7C1C1"; REJECTED_FG = "#501313"
PENDING_BG  = "#FAEEDA"; PENDING_FG  = "#633806"

STATUS_COLORS = {
    "pending":  (PENDING_BG,  PENDING_FG),
    "reviewed": (REVIEWED_BG, REVIEWED_FG),
    "approved": (APPROVED_BG, APPROVED_FG),
    "rejected": (REJECTED_BG, REJECTED_FG),
}

# ─── Helpers ─────────────────────────────────────────────────────────────────
def btn(parent, text, cmd, bg=PRIMARY, fg="white", width=None, font_size=10):
    kw = dict(text=text, command=cmd, bg=bg, fg=fg, relief="flat",
              font=("Segoe UI", font_size), cursor="hand2",
              padx=14, pady=6, activebackground=PRIMARY_H, activeforeground="white")
    if width:
        kw["width"] = width
    return tk.Button(parent, **kw)

def label(parent, text, size=10, color=TEXT, bold=False, wrap=0):
    f = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
    kw = dict(text=text, font=f, fg=color, bg=parent.cget("bg"))
    if wrap:
        kw["wraplength"] = wrap
        kw["justify"] = "left"
    return tk.Label(parent, **kw)

def scrollable_frame(parent):
    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg=BG)
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    win_id = canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    # FIX: bind scroll only to this canvas, not globally
    def _on_enter(e):
        canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units"))
    def _on_leave(e):
        canvas.unbind_all("<MouseWheel>")
    canvas.bind("<Enter>", _on_enter)
    canvas.bind("<Leave>", _on_leave)

    # Keep frame width in sync with canvas
    def _resize(e):
        canvas.itemconfig(win_id, width=e.width)
    canvas.bind("<Configure>", _resize)

    return frame

# ─── App ─────────────────────────────────────────────────────────────────────
class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Management System")
        self.geometry("780x620")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.projects = load_projects()
        self.current_user = None
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ── Login ────────────────────────────────────────────────────────────────
    def show_login(self):
        self.clear()
        self.geometry("440x500")

        outer = tk.Frame(self, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(outer, bg=CARD, relief="flat", bd=0,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=20, pady=20, ipadx=30, ipady=20)

        label(card, "TASK MANAGEMENT", 16, PRIMARY, bold=True).pack(pady=(20, 4))
        label(card, "Sign in to your workspace", 10, MUTED).pack(pady=(0, 16))

        # Role toggle — FIX: initialize colors after both buttons are created
        role_var = tk.StringVar(value="subordinate")
        rf = tk.Frame(card, bg=CARD)
        rf.pack(fill="x", padx=24, pady=(0, 12))
        role_btns = []

        def refresh_role_btns(*_):
            for rb in role_btns:
                active = role_var.get() == rb._val
                rb.config(bg=PRIMARY if active else "#E8E8EE",
                          fg="white" if active else MUTED)

        for t, v in [("Manager", "manager"), ("Subordinate", "subordinate")]:
            rb = tk.Button(rf, text=t, font=("Segoe UI", 10), relief="flat",
                           cursor="hand2", pady=7,
                           command=lambda val=v: [role_var.set(val), refresh_role_btns()])
            rb._val = v
            rb.pack(side="left", expand=True, fill="x", padx=3)
            role_btns.append(rb)

        # Initialize colors correctly after all buttons exist
        refresh_role_btns()
        role_var.trace_add("write", refresh_role_btns)

        # Fields
        self._login_email_var = tk.StringVar()
        self._login_pwd_var   = tk.StringVar()
        for lbl_text, var, show in [("Email", self._login_email_var, ""),
                                     ("Password", self._login_pwd_var, "*")]:
            label(card, lbl_text, 9, MUTED).pack(anchor="w", padx=24)
            tk.Entry(card, textvariable=var, font=("Segoe UI", 11),
                     relief="solid", bd=1, show=show,
                     highlightthickness=1, highlightbackground=BORDER
                     ).pack(fill="x", padx=24, pady=(2, 10), ipady=6)

        err_lbl = label(card, "", 9, DANGER)
        err_lbl.pack(pady=(0, 4))

        def do_login():
            email = self._login_email_var.get().strip().lower()
            pwd   = self._login_pwd_var.get()
            user  = USERS.get(email)
            if not user or user["password"] != pwd:
                err_lbl.config(text="Invalid email or password.")
                return
            if user["role"] != role_var.get():
                err_lbl.config(text=f"This account is a {user['role']}, not a {role_var.get()}.")
                return
            self.current_user = {"email": email, **user}
            if user["role"] == "manager":
                self.show_manager()
            else:
                self.show_subordinate()

        # Allow Enter key to submit
        self.bind("<Return>", lambda e: do_login())
        btn(card, "Sign In", do_login, width=20).pack(pady=(4, 8))

        hint_f = tk.Frame(card, bg="#F5F4FB")
        hint_f.pack(fill="x", padx=24, pady=(4, 16))
        label(hint_f, "Demo credentials", 8, MUTED, bold=True).pack(anchor="w")
        hints = ("manager@task.com / mgr123\narjun@task.com / arjun123\n"
                 "priya@task.com / priya123\nrahul@task.com / rahul123\nneha@task.com / neha123")
        label(hint_f, hints, 8, MUTED, wrap=320).pack(anchor="w")

    # ── Manager Dashboard ────────────────────────────────────────────────────
    def show_manager(self):
        self.clear()
        self.unbind("<Return>")
        self.geometry("900x660")

        top = tk.Frame(self, bg=PRIMARY, height=54)
        top.pack(fill="x")
        top.pack_propagate(False)
        label(top, "  Task Management — Manager", 13, "white", bold=True).pack(side="left", padx=12, pady=14)
        label(top, f"  {self.current_user['name']}", 10, "#CECBF6").pack(side="left")
        btn(top, "Sign Out", self.show_login, bg="#534AB7", fg="white").pack(side="right", padx=12, pady=10)

        # Filter bar
        fb = tk.Frame(self, bg=BG)
        fb.pack(fill="x", padx=20, pady=(14, 6))
        label(fb, "Filter:", 10, MUTED).pack(side="left")
        self._mgr_filter = tk.StringVar(value="all")
        for text, val in [("All","all"),("Pending","pending"),("Reviewed","reviewed"),
                          ("Approved","approved"),("Rejected","rejected")]:
            tk.Radiobutton(fb, text=text, variable=self._mgr_filter, value=val,
                           font=("Segoe UI", 10), bg=BG, fg=TEXT,
                           activebackground=BG, selectcolor=BG,
                           command=self._refresh_manager).pack(side="left", padx=6)

        # Stats row — FIX: now includes "reviewed" count
        self._stat_frame = tk.Frame(self, bg=BG)
        self._stat_frame.pack(fill="x", padx=20, pady=(0, 8))
        self._draw_stats()

        self._mgr_list_outer = tk.Frame(self, bg=BG)
        self._mgr_list_outer.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        self._refresh_manager()

    def _draw_stats(self):
        for w in self._stat_frame.winfo_children():
            w.destroy()
        counts = {s: 0 for s in ["pending", "reviewed", "approved", "rejected"]}
        for p in self.projects:
            if p["status"] in counts:
                counts[p["status"]] += 1
        total = len(self.projects)

        # FIX: added "Reviewed" stat card
        for lbl_text, val, clr in [
            ("Total",    total,               PRIMARY),
            ("Pending",  counts["pending"],   PENDING_FG),
            ("Reviewed", counts["reviewed"],  REVIEWED_FG),
            ("Approved", counts["approved"],  SUCCESS),
            ("Rejected", counts["rejected"],  DANGER),
        ]:
            c = tk.Frame(self._stat_frame, bg=CARD, relief="flat",
                         highlightthickness=1, highlightbackground=BORDER)
            c.pack(side="left", padx=(0, 8), ipadx=14, ipady=8)
            label(c, lbl_text, 9, MUTED).pack()
            label(c, str(val), 18, clr, bold=True).pack()

    def _refresh_manager(self):
        for w in self._mgr_list_outer.winfo_children():
            w.destroy()
        filt = self._mgr_filter.get()
        projects = [p for p in self.projects if filt == "all" or p["status"] == filt]

        scroll_outer = tk.Frame(self._mgr_list_outer, bg=BG)
        scroll_outer.pack(fill="both", expand=True)
        inner = scrollable_frame(scroll_outer)

        if not projects:
            label(inner, "No projects match this filter.", 11, MUTED).pack(pady=40)
            return
        for p in projects:
            self._draw_manager_project(inner, p)

    def _draw_manager_project(self, parent, p):
        card_f = tk.Frame(parent, bg=CARD, relief="flat",
                          highlightthickness=1, highlightbackground=BORDER)
        card_f.pack(fill="x", pady=6, ipady=10, ipadx=14)

        hf = tk.Frame(card_f, bg=CARD)
        hf.pack(fill="x", padx=14, pady=(10, 2))
        label(hf, p["title"], 12, TEXT, bold=True).pack(side="left")
        st_bg, st_fg = STATUS_COLORS.get(p["status"], (BORDER, TEXT))
        tk.Label(hf, text=p["status"].upper(), font=("Segoe UI", 8, "bold"),
                 bg=st_bg, fg=st_fg, relief="flat", padx=8, pady=3).pack(side="left", padx=8)

        label(card_f, f"By {p['owner']}  ·  {p['date']}  ·  File: {p['file']}", 9, MUTED).pack(anchor="w", padx=14)
        label(card_f, p["desc"], 10, TEXT, wrap=720).pack(anchor="w", padx=14, pady=(4, 4))

        if p["remark"]:
            rf = tk.Frame(card_f, bg="#F5F4FB", highlightthickness=1, highlightbackground=BORDER)
            rf.pack(fill="x", padx=14, pady=(0, 6), ipadx=10, ipady=6)
            label(rf, "Remark: " + p["remark"], 10, TEXT, wrap=700).pack(anchor="w", padx=8, pady=4)

        if p["status"] == "pending":
            af = tk.Frame(card_f, bg=BG, highlightthickness=1, highlightbackground=BORDER)
            af.pack(fill="x", padx=14, pady=(2, 8), ipadx=10, ipady=8)
            label(af, "Add remark & action", 9, MUTED, bold=True).pack(anchor="w", padx=10, pady=(6, 2))
            rm_var = tk.StringVar()
            tk.Entry(af, textvariable=rm_var, font=("Segoe UI", 10),
                     relief="solid", bd=1, highlightthickness=1,
                     highlightbackground=BORDER).pack(padx=10, pady=(0, 8), fill="x")

            bf = tk.Frame(af, bg=BG)
            bf.pack(anchor="w", padx=10, pady=(0, 6))

            def make_action(proj, action, rv):
                def do():
                    # FIX: confirmation dialog before approve/reject
                    if action in ("approved", "rejected"):
                        word = "approve" if action == "approved" else "reject"
                        if not messagebox.askyesno("Confirm", f"Are you sure you want to {word} '{proj['title']}'?"):
                            return
                    remark = rv.get().strip()
                    proj["status"] = action
                    if remark:
                        proj["remark"] = remark
                    elif action == "approved":
                        proj["remark"] = "Approved."
                    elif action == "rejected":
                        proj["remark"] = "Rejected."
                    save_projects(self.projects)
                    self._draw_stats()
                    self._refresh_manager()
                return do

            btn(bf, "✓  Approve",      make_action(p, "approved", rm_var), bg=SUCCESS).pack(side="left", padx=(0, 6))
            btn(bf, "✗  Reject",       make_action(p, "rejected", rm_var), bg=DANGER).pack(side="left", padx=(0, 6))
            btn(bf, "💬  Save Remark", make_action(p, "reviewed", rm_var), bg="#534AB7").pack(side="left")

    # ── Subordinate Dashboard ────────────────────────────────────────────────
    def show_subordinate(self):
        self.clear()
        self.unbind("<Return>")
        self.geometry("780x620")

        top = tk.Frame(self, bg=SUCCESS, height=54)
        top.pack(fill="x")
        top.pack_propagate(False)
        label(top, "  Task Management — Subordinate", 13, "white", bold=True).pack(side="left", padx=12, pady=14)
        label(top, f"  {self.current_user['name']}", 10, "#9FE1CB").pack(side="left")
        btn(top, "Sign Out", self.show_login, bg="#0F6E56", fg="white").pack(side="right", padx=12, pady=10)

        tab_f = tk.Frame(self, bg=BG)
        tab_f.pack(fill="x", padx=20, pady=(12, 0))
        self._sub_tab = tk.StringVar(value="projects")

        self._tab_btns = {}
        self._sub_content = tk.Frame(self, bg=BG)
        self._sub_content.pack(fill="both", expand=True, padx=20, pady=10)

        def switch(val):
            self._sub_tab.set(val)
            for v, b in self._tab_btns.items():
                b.config(bg=CARD if v == val else BG,
                         fg=PRIMARY if v == val else MUTED,
                         relief="solid" if v == val else "flat")
            if val == "projects":
                self._show_my_projects()
            else:
                self._show_upload_form()

        for text, val in [("📁  My Projects", "projects"), ("⬆  Upload Project", "upload")]:
            b = tk.Button(tab_f, text=text, font=("Segoe UI", 10),
                          relief="flat", cursor="hand2", padx=18, pady=8,
                          command=lambda v=val: switch(v))
            b.pack(side="left", padx=(0, 4))
            self._tab_btns[val] = b

        switch("projects")

    def _clear_sub_content(self):
        for w in self._sub_content.winfo_children():
            w.destroy()

    def _show_my_projects(self):
        self._clear_sub_content()
        email = self.current_user["email"]
        mine  = [p for p in self.projects if p["email"] == email]

        if not mine:
            label(self._sub_content, "No projects yet. Upload your first project!", 12, MUTED).pack(pady=40)
            return

        scroll_outer = tk.Frame(self._sub_content, bg=BG)
        scroll_outer.pack(fill="both", expand=True)
        inner = scrollable_frame(scroll_outer)

        for p in mine:
            card_f = tk.Frame(inner, bg=CARD, relief="flat",
                              highlightthickness=1, highlightbackground=BORDER)
            card_f.pack(fill="x", pady=6, ipady=8, ipadx=12)

            hf = tk.Frame(card_f, bg=CARD)
            hf.pack(fill="x", padx=14, pady=(10, 2))
            label(hf, p["title"], 12, TEXT, bold=True).pack(side="left")
            st_bg, st_fg = STATUS_COLORS.get(p["status"], (BORDER, TEXT))
            tk.Label(hf, text=p["status"].upper(), font=("Segoe UI", 8, "bold"),
                     bg=st_bg, fg=st_fg, relief="flat", padx=8, pady=3).pack(side="left", padx=8)

            label(card_f, f"Submitted: {p['date']}  ·  File: {p['file']}", 9, MUTED).pack(anchor="w", padx=14)
            label(card_f, p["desc"], 10, TEXT, wrap=680).pack(anchor="w", padx=14, pady=(4, 4))

            if p["remark"]:
                rf = tk.Frame(card_f, bg="#F5F4FB", highlightthickness=1, highlightbackground=BORDER)
                rf.pack(fill="x", padx=14, pady=(0, 8), ipadx=10, ipady=4)
                label(rf, "Manager's remark: " + p["remark"], 10, TEXT, wrap=660).pack(anchor="w", padx=8, pady=6)
            elif p["status"] == "pending":
                label(card_f, "⏳  Awaiting manager review", 9, MUTED).pack(anchor="w", padx=14, pady=(0, 8))

    def _show_upload_form(self):
        self._clear_sub_content()
        card_f = tk.Frame(self._sub_content, bg=CARD, relief="flat",
                          highlightthickness=1, highlightbackground=BORDER)
        card_f.pack(fill="x", pady=6, ipadx=20, ipady=16)

        label(card_f, "Submit a new project", 13, TEXT, bold=True).pack(anchor="w", padx=20, pady=(16, 10))

        label(card_f, "Project title", 9, MUTED).pack(anchor="w", padx=20)
        title_var = tk.StringVar()
        tk.Entry(card_f, textvariable=title_var, font=("Segoe UI", 11),
                 relief="solid", bd=1, highlightthickness=1,
                 highlightbackground=BORDER).pack(fill="x", padx=20, pady=(2, 10), ipady=6)

        label(card_f, "Description", 9, MUTED).pack(anchor="w", padx=20)
        desc_box = tk.Text(card_f, font=("Segoe UI", 10), height=4, relief="solid",
                           bd=1, wrap="word", highlightthickness=1, highlightbackground=BORDER)
        desc_box.pack(fill="x", padx=20, pady=(2, 10))

        file_var = tk.StringVar()
        file_lbl = label(card_f, "No file selected", 9, MUTED)
        file_lbl.pack(anchor="w", padx=20)

        def pick_file():
            path = filedialog.askopenfilename(
                title="Select project file",
                filetypes=[("All files","*.*"),("PDF","*.pdf"),
                           ("Word","*.docx"),("Excel","*.xlsx"),
                           ("PowerPoint","*.pptx"),("Text","*.txt")]
            )
            if path:
                file_var.set(path)
                file_lbl.config(text="📎  " + os.path.basename(path), fg=SUCCESS)

        btn(card_f, "📂  Choose File", pick_file, bg="#534AB7").pack(anchor="w", padx=20, pady=(4, 10))

        err_lbl     = label(card_f, "", 9, DANGER)
        err_lbl.pack(anchor="w", padx=20)
        success_lbl = label(card_f, "", 10, SUCCESS)
        success_lbl.pack(anchor="w", padx=20)

        def do_submit():
            title = title_var.get().strip()
            desc  = desc_box.get("1.0", "end").strip()
            fpath = file_var.get().strip()
            err_lbl.config(text="")
            success_lbl.config(text="")
            if not title:
                err_lbl.config(text="Please enter a project title.")
                return
            if not desc:
                err_lbl.config(text="Please add a description.")
                return
            if not fpath:
                err_lbl.config(text="Please choose a file.")
                return
            # FIX: check duplicate title for same user
            email = self.current_user["email"]
            if any(p["title"].lower() == title.lower() and p["email"] == email for p in self.projects):
                err_lbl.config(text="You already submitted a project with this title.")
                return
            fname = os.path.basename(fpath)
            try:
                shutil.copy2(fpath, os.path.join(UPLOADS_DIR, fname))
            except Exception:
                pass
            new_proj = {
                "id":     max((p["id"] for p in self.projects), default=0) + 1,
                "title":  title,
                "desc":   desc,
                "file":   fname,
                "owner":  self.current_user["name"],
                "email":  email,
                "status": "pending",
                "remark": "",
                "date":   str(date.today()),
            }
            self.projects.append(new_proj)
            save_projects(self.projects)
            success_lbl.config(text="✅  Project submitted successfully!")
            title_var.set("")
            desc_box.delete("1.0", "end")
            file_var.set("")
            file_lbl.config(text="No file selected", fg=MUTED)

        btn(card_f, "⬆  Submit Project", do_submit, width=22).pack(anchor="w", padx=20, pady=(8, 16))


if __name__ == "__main__":
    app = TaskApp()
    app.mainloop()
    