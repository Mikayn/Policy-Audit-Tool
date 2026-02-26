import tkinter as tk
from tkinter import ttk, messagebox
import main as m  

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("College Policy Audit Tool")
root.geometry("800x450")

tree = ttk.Treeview(root, columns=("ID", "Type", "Policy"), show="headings")

tree.heading("ID", text="ID")
tree.heading("Type", text="Type")
tree.heading("Policy", text="Policy")

tree.column("ID", width=10)
tree.column("Type", width=140)
tree.column("Policy", width=500)

tree.pack(fill=tk.BOTH, expand=True)

# =========================
# POLICY FUNCTIONS
# =========================

def refresh_list():
    for row in tree.get_children():
        tree.delete(row)
    for policy_id, policy in m.policies.items():
        tree.insert(
            "",
            tk.END,
            iid=policy_id,
            values=(policy_id, policy["type"], str(policy))
        )


def delete_policy():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "No policy selected")
        return
    policy_id = selected[0]
    confirm = messagebox.askyesno("Confirm", f"Delete policy '{policy_id}'?")
    if confirm:
        del m.policies[policy_id]
        m.save_policies(m.policies)
        refresh_list()


def evaluate_policy_gui():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "No policy selected")
        return
    policy_id = selected[0]
    result = m.evaluate_policy(m.policies[policy_id])
    status = "ALLOWED" if result else "DENIED"
    messagebox.showinfo("Evaluation Result", f"Policy {policy_id} → {status}")


# =========================
# ADD POLICY WINDOW
# =========================

def open_add_window():
    add_win = tk.Toplevel(root)
    add_win.title("Add Policy")

    tk.Label(add_win, text="Policy ID").grid(row=0, column=0)
    id_entry = tk.Entry(add_win)
    id_entry.grid(row=0, column=1)

    tk.Label(add_win, text="Type").grid(row=1, column=0)
    type_combo = ttk.Combobox(add_win, values=["SIS", "Exam", "Lab", "Privacy"], state="readonly")
    type_combo.grid(row=1, column=1)

    fields_frame = tk.Frame(add_win)
    fields_frame.grid(row=2, column=0, columnspan=2, pady=10)

    field_widgets = {}

    def load_fields(event=None):
        for widget in fields_frame.winfo_children():
            widget.destroy()
        field_widgets.clear()

        selected_type = type_combo.get()
        if not selected_type:
            return

        schema = m.policy_schemas[selected_type]["vars"]
        row = 0

        for name, type_name in schema.items():
            tk.Label(fields_frame, text=name).grid(row=row, column=0)
            if type_name == "Bool":
                var = tk.BooleanVar()
                tk.Checkbutton(fields_frame, variable=var).grid(row=row, column=1)
            elif name in ["role", "action", "system", "status"]:
                # dropdowns for other types
                values_map = {
                    "role": ["student","faculty","admin","registrar"],
                    "action": ["view","edit","delete"],
                    "system": ["lab_pc","server"],
                    "status": ["enrolled","graduated"]
                }
                var = tk.StringVar()
                combo = ttk.Combobox(fields_frame, values=values_map.get(name, []), textvariable=var, state="readonly")
                combo.grid(row=row, column=1)
            else:
                var = tk.StringVar()
                tk.Entry(fields_frame, textvariable=var).grid(row=row, column=1)
            field_widgets[name] = var
            row += 1

    type_combo.bind("<<ComboboxSelected>>", load_fields)

    def save_policy():
        policy_id = id_entry.get()
        policy_type = type_combo.get()
        if not policy_id or not policy_type:
            messagebox.showerror("Error", "Policy ID and Type required")
            return
        if policy_id in m.policies:
            messagebox.showerror("Error", "Policy ID already exists")
            return

        policy = {"type": policy_type}

        for name, var in field_widgets.items():
            val = var.get() if not isinstance(var, tk.BooleanVar) else var.get()
            policy[name] = val

        m.policies[policy_id] = policy
        m.save_policies(m.policies)
        refresh_list()
        add_win.destroy()

    tk.Button(add_win, text="Save", command=save_policy).grid(row=3, column=0, columnspan=2, pady=10)


# =========================
# BUTTONS
# =========================

btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X)

tk.Button(btn_frame, text="Add Policy", command=open_add_window).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="Delete Policy", command=delete_policy).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Evaluate Policy", command=evaluate_policy_gui).pack(side=tk.LEFT, padx=5)

refresh_list()
root.mainloop()