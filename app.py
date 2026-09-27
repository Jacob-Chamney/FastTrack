import customtkinter as ctk
from storage import read_json, write_json


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -----------SETTINGS & DATA----------#

        self.geometry("800x600")
        self.title("Progress Tracker")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grplist = {}
        self.grpempty = {}
        self.grpcomplete = {}
        self.tasklist = []
        self.selectedtask = None
        self.currentfile = None

        # -----------BUILD GUI----------#

        # title bar - add group - note
        self.titlebarframe = ctk.CTkFrame(self, height=50)
        self.titlebarframe.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )
        self.btnaddgroup = ctk.CTkButton(
            self.titlebarframe,
            text="+ Group",
            height=35,
            width=45,
            command=self.add_group_dialog,
        )
        self.btnaddgroup.grid(row=0, column=0, padx=10, pady=10)
        self.btnaddtask = ctk.CTkButton(
            self.titlebarframe,
            text="+ Task",
            height=35,
            width=45,
            command=self.add_task_dialog,
        )
        self.btnaddtask.grid(row=0, column=1, padx=(0, 10), pady=10)
        self.btnopenfile = ctk.CTkButton(
            self.titlebarframe,
            text="Open File",
            height=35,
            width=45,
            command=self.open_file,
        )
        self.btnopenfile.grid(row=0, column=2, padx=(0, 10), pady=10)
        self.btnsavefile = ctk.CTkButton(
            self.titlebarframe,
            text="Save File",
            height=35,
            width=45,
            command=self.save_file,
        )
        self.btnsavefile.grid(row=0, column=3, padx=(0, 10), pady=10)

        # sidebar - for detail view
        self.sidebarframe = ctk.CTkFrame(self, width=380)
        self.sidebarframe.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=(0, 10))
        self.sidebarframe.grid_propagate(False)
        self.lblsidebartitle = ctk.CTkLabel(self.sidebarframe, text="")
        self.lblsidebartitle.grid(row=0, column=0, sticky="w", padx=10)
        self.lblsidebargroup = ctk.CTkLabel(self.sidebarframe, text="")
        self.lblsidebargroup.grid(row=1, column=0, sticky="w", padx=20)
        self.txtnotes = ctk.CTkTextbox(self.sidebarframe, state="disabled")
        self.txtnotes.grid(row=2, column=0, sticky="nesw", padx=10, pady=10)
        self.sidebarframe.grid_columnconfigure(0, weight=1)
        self.sidebarframe.grid_rowconfigure(2, weight=1)
        self.sidebarbtnframe = ctk.CTkFrame(self.sidebarframe, fg_color="transparent")
        self.sidebarbtnframe.grid(row=3, column=0, sticky="ew", padx=35, pady=10)
        self.btneditnote = ctk.CTkButton(
            self.sidebarbtnframe, text="Edit", state="disabled", command=self.edit_task
        )
        self.btneditnote.pack(side="left")
        self.btnsavenote = ctk.CTkButton(
            self.sidebarbtnframe,
            text="Save",
            state="disabled",
            command=self.update_task_details,
        )
        self.btnsavenote.pack(side="right")

        # progress bar - updates based on totalitems/itemschecked - tab independent
        self.progbarframe = ctk.CTkFrame(
            self, height=75, width=380, fg_color="transparent"
        )
        self.progbarframe.grid(row=2, column=1, sticky="s", padx=(0, 10), pady=(0, 10))
        self.progbarframe.grid_propagate(False)
        self.progbarframe.grid_columnconfigure(0, weight=1)
        self.progbarframe.grid_rowconfigure(0, weight=1)
        self.prgbartab = ctk.CTkProgressBar(self.progbarframe)
        self.prgbartab.grid(row=1, column=0, sticky="sew", padx=(10, 10), pady=(10, 0))
        self.lblprogress = ctk.CTkLabel(self.progbarframe, text="progress")
        self.lblprogress.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # tab container - holds scrollable frames
        self.tabs = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabs.grid(row=1, column=0, sticky="nesw", padx=10, pady=(0, 10))

        self.update_progress()

    # -----------FUNCTIONS----------#

    # group functions
    def add_group_dialog(self):
        dialog = ctk.CTkInputDialog(text="Group Name:", title="New Group")
        name = dialog.get_input()
        self.add_group((name or "").strip())

    def add_group(self, name, select=True):
        if not name or name in self.grplist:
            return
        tab = self.tabs.add(name)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nesw")
        message = ctk.CTkFrame(tab, fg_color="transparent")
        message.grid(row=0, column=0, sticky="nesw")
        emptydel = ctk.CTkLabel(
            message, text="Uh Oh! This group appears to be empty!", anchor="center"
        )
        emptydel.grid(row=1, column=0)
        message.grid_columnconfigure(0, weight=1)
        message.grid_rowconfigure(0, weight=1)
        message.grid_rowconfigure(3, weight=1)
        btnemptydel = ctk.CTkButton(
            message,
            text="Click Here To Delete!",
            fg_color="transparent",
            command=self.delete_group,
        )
        btnemptydel.grid(row=2, column=0, sticky="ew")
        message.grid_remove()
        message1 = ctk.CTkFrame(tab, fg_color="transparent")
        message1.grid(row=0, column=0, sticky="nesw")
        fulldel = ctk.CTkLabel(
            message1, text="Congrats! This group appears to be full!"
        )
        fulldel.grid(row=1, column=0)
        message1.grid_columnconfigure(0, weight=1)
        message1.grid_rowconfigure(0, weight=1)
        message1.grid_rowconfigure(3, weight=1)
        btnfulldel = ctk.CTkButton(
            message1,
            text="Click Here to Delete!",
            fg_color="transparent",
            command=self.delete_group,
        )
        btnfulldel.grid(row=2, column=0, sticky="ew")
        message1.grid_remove()
        self.grpcomplete[name] = message1
        self.grpempty[name] = message
        self.grplist[name] = scroll
        if select:
            self.tabs.set(name)
            self.on_tab_change()

    def delete_group(self):
        name = self.tabs.get()
        if name not in self.grplist:
            return
        self.clear_task_details()
        self.tabs.delete(name)
        self.grplist.pop(name)
        self.grpempty.pop(name)
        self.grpcomplete.pop(name)
        self.tasklist = [t for t in self.tasklist if t["group"] != name]
        self.update_progress()

    # task functions
    def add_task_dialog(self):
        if not self.grplist:
            return
        dialog = ctk.CTkInputDialog(text="Task Name", title="New Task")
        name = dialog.get_input()
        self.add_task((name or "").strip())

    def delete_task(self, task):
        if task is self.selectedtask:
            self.clear_task_details()
        task["row"].destroy()
        self.tasklist.remove(task)
        self.update_progress()

    def add_task(self, name, group=None, done=False, notes=""):
        if not name:
            return
        if not group:
            group = self.tabs.get()
        scroll = self.grplist[group]
        task = {"title": name, "notes": notes, "done": done, "group": group}
        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.pack(fill="x", padx=4, pady=2)
        row.grid_columnconfigure(1, weight=1)
        chk = ctk.CTkCheckBox(
            row, text="", width=24, command=lambda: self.toggle_done(task, chk)
        )
        chk.grid(row=0, column=0, padx=(6, 0), pady=4)
        if done:
            chk.select()
        lbl = ctk.CTkLabel(row, text=name, anchor="w")
        lbl.grid(row=0, column=1, sticky="ew", padx=6)
        for w in (row, lbl):
            w.bind("<Button-1>", lambda e: self.select_task(task))
        btndel = ctk.CTkButton(
            row,
            text="X",
            text_color="red",
            width=28,
            fg_color="transparent",
            command=lambda: self.delete_task(task),
        )
        btndel.grid(row=0, column=2, padx=6)
        btndel.grid_remove()
        task["row"] = row
        task["btndel"] = btndel
        self.tasklist.append(task)
        self.update_progress()

    def select_task(self, task):
        if self.selectedtask:
            self.selectedtask["row"].configure(fg_color="transparent")
            self.selectedtask["btndel"].grid_remove()
        self.selectedtask = task
        self.selectedtask["row"].configure(fg_color=("gray75", "gray50"))
        self.lblsidebartitle.configure(text=task["title"])
        self.lblsidebargroup.configure(text=task["group"])
        self.txtnotes.configure(state="normal")
        self.txtnotes.delete("1.0", "end")
        self.txtnotes.insert("1.0", task["notes"])
        self.txtnotes.configure(state="disabled")
        self.btneditnote.configure(state="normal")
        self.btnsavenote.configure(state="disabled")

    def edit_task(self):
        if not self.selectedtask:
            return
        self.txtnotes.configure(state="normal")
        self.btneditnote.configure(state="disabled")
        self.btnsavenote.configure(state="normal")
        self.selectedtask["btndel"].grid()

    def update_task_details(self):
        if not self.selectedtask:
            return
        self.selectedtask["notes"] = self.txtnotes.get("1.0", "end-1c")
        self.btnsavenote.configure(state="disabled")
        self.btneditnote.configure(state="normal")
        self.txtnotes.configure(state="disabled")
        self.selectedtask["btndel"].grid_remove()

    def clear_task_details(self):
        if self.selectedtask:
            self.selectedtask["row"].configure(fg_color="transparent")
            self.selectedtask["btndel"].grid_remove()
        self.selectedtask = None
        self.lblsidebartitle.configure(text="")
        self.lblsidebargroup.configure(text="")
        self.txtnotes.configure(state="normal")
        self.txtnotes.delete("1.0", "end")
        self.txtnotes.configure(state="disabled")
        self.btneditnote.configure(state="disabled")
        self.btnsavenote.configure(state="disabled")

    # utility functions
    def toggle_done(self, task, chk):
        task["done"] = bool(chk.get())
        self.update_progress()

    def update_progress(self):
        group = self.tabs.get()
        tasks = [t for t in self.tasklist if t["group"] == group]
        total = len(tasks)
        done = sum(t["done"] for t in tasks)
        percent = done / total if total else 0
        self.prgbartab.set(percent)
        if total == 0:
            self.lblprogress.configure(text="No Tasks Found")
            if group in self.grplist:
                self.grpempty[group].grid()
                self.grplist[group].grid_remove()
                self.grpcomplete[group].grid_remove()
        elif done == total:
            self.lblprogress.configure(
                text=f"{done}/{total} All Tasks Complete!\n{percent * 100:.0f}%"
            )
            self.grpcomplete[group].grid()
            self.grplist[group].grid_remove()
            self.grpempty[group].grid_remove()
        else:
            self.lblprogress.configure(
                text=f"{done}/{total} Tasks Complete\n{percent * 100:.0f}%"
            )
            self.grplist[group].grid()
            self.grpempty[group].grid_remove()
            self.grpcomplete[group].grid_remove()

    def on_tab_change(self):
        self.clear_task_details()
        self.update_progress()

    def get_save_data(self):
        groups = list(self.grplist)
        tasks = [
            {
                "title": t["title"],
                "notes": t["notes"],
                "done": t["done"],
                "group": t["group"],
            }
            for t in self.tasklist
        ]
        return {"groups": groups, "tasks": tasks}

    def save_data(self, path):
        write_json(path, self.get_save_data())

    def load_data(self, path):
        data = read_json(path)
        if data is None:
            return
        self.clear_all()
        for g in data["groups"]:
            self.add_group(g, select=False)
        if data["groups"]:
            self.tabs.set(data["groups"][0])
        for t in data["tasks"]:
            self.add_task(
                t["title"], group=t["group"], done=t["done"], notes=t["notes"]
            )
        self.update_progress()

    def open_file(self):
        path = ctk.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        self.load_data(path)
        self.currentfile = path

    def save_as_file(self):
        path = ctk.filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return
        self.save_data(path)
        self.currentfile = path

    def save_file(self):
        if not self.currentfile:
            self.save_as_file()
            return
        self.save_data(self.currentfile)

    def clear_all(self):
        self.clear_task_details()
        for g in self.grplist:
            self.tabs.delete(g)
        self.grplist.clear()
        self.grpempty.clear()
        self.grpcomplete.clear()
        self.tasklist.clear()
        self.update_progress()
