import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext

# Optional drag & drop support
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("⚠️ Drag & drop not installed. Run: pip install tkinterdnd2")

# ----------------------------
# REMOVE COMMENTS
# ----------------------------
def remove_comments_from_input():
    text = input_text.get("1.0", tk.END)
    if not text.strip():
        messagebox.showwarning("Warning", "Please paste your structure first.")
        return

    cleaned_text = re.sub(r'\s*#.*', '', text)
    cleaned_text = "\n".join([line for line in cleaned_text.splitlines() if line.strip()])

    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", cleaned_text)
    messagebox.showinfo("Done", "✅ Comments removed successfully!")

# ----------------------------
# PARSE STRUCTURE (DFS style)
# ----------------------------
def parse_structure(text):
    lines = [line.rstrip() for line in text.split('\n') if line.strip()]
    cleaned_lines = [re.sub(r'[│└├─]+', '', line).rstrip() for line in lines]

    structure = []
    stack = [(None, -1)]
    for line in cleaned_lines:
        indent = len(line) - len(line.lstrip(' '))
        name = line.strip()
        if not name:
            continue
        while stack and stack[-1][1] >= indent:
            stack.pop()
        parent = stack[-1][0]
        path = os.path.join(parent, name) if parent else name
        structure.append(path)
        stack.append((path, indent))
    return structure


# ----------------------------
# show_overwrite_checklist
# ----------------------------
def show_overwrite_checklist(existing_items):
    """Show one popup checklist for existing files/folders."""
    popup = tk.Toplevel()
    popup.title("Overwrite Existing Items")
    popup.geometry("420x450")
    popup.configure(bg="#2b2b2b")
    popup.grab_set()

    tk.Label(
        popup,
        text="These items already exist.\nSelect the ones you want to overwrite:",
        bg="#2b2b2b", fg="white", font=("Segoe UI", 10, "bold")
    ).pack(pady=8)

    frame = tk.Frame(popup, bg="#2b2b2b")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    canvas = tk.Canvas(frame, bg="#2b2b2b", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#2b2b2b")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    vars_dict = {}
    for item in existing_items:
        var = tk.BooleanVar(value=False)
        vars_dict[item] = var
        cb = tk.Checkbutton(
            scroll_frame, text=os.path.relpath(item, start=os.path.dirname(existing_items[0])),
            variable=var, bg="#2b2b2b", fg="white",
            selectcolor="#3a3d41", activebackground="#2b2b2b",
            anchor="w", padx=10
        )
        cb.pack(fill="x", padx=5, pady=2)

    # Toggle all selection checkbox
    toggle_all = tk.BooleanVar(value=False)

    def toggle_all_items():
        for var in vars_dict.values():
            var.set(toggle_all.get())

    tk.Checkbutton(
        popup,
        text="Select / Deselect All",
        variable=toggle_all,
        command=toggle_all_items,
        bg="#2b2b2b", fg="#bbbbbb",
        selectcolor="#3a3d41", activebackground="#2b2b2b",
        anchor="w"
    ).pack(pady=5, padx=10, anchor="w")

    result = []

    def confirm():
        nonlocal result
        result = [item for item, var in vars_dict.items() if var.get()]
        popup.destroy()

    def cancel():
        nonlocal result
        result = None
        popup.destroy()

    btn_frame = tk.Frame(popup, bg="#2b2b2b")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Confirm", command=confirm, bg="#007acc", fg="white", width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel", command=cancel, bg="#3a3d41", fg="white", width=10).pack(side="right", padx=5)

    popup.wait_window()
    return result


# ----------------------------
# CREATE STRUCTURE
# ----------------------------
def create_structure(base_path, structure):
    if not structure:
        return

    first = structure[0]
    root_name = first.split(os.sep)[0]
    root_path = os.path.join(base_path, root_name)
    os.makedirs(root_path, exist_ok=True)

    existing_items = []  # collect all existing files/folders first

    # First pass — find existing paths
    for rel_path in structure[1:]:
        full_path = os.path.join(base_path, rel_path)
        if os.path.exists(full_path):
            existing_items.append(full_path)

    # If there are existing items, show checklist popup
    overwrite_list = []
    if existing_items:
        result = show_overwrite_checklist(existing_items)
        if not result:  # cancelled
            messagebox.showinfo("Cancelled", "Operation cancelled by user.")
            return
        overwrite_list = result  # list of items to overwrite

    # Second pass — create everything
    for rel_path in structure[1:]:
        full_path = os.path.join(base_path, rel_path)
        item_name = os.path.basename(full_path)

        # --- File case ---
        if '.' in item_name:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            if os.path.exists(full_path) and full_path not in overwrite_list:
                continue  # skip if exists and not chosen to overwrite

            with open(full_path, 'w'):
                pass  # create or overwrite empty file

        # --- Folder case ---
        else:
            if os.path.exists(full_path) and full_path not in overwrite_list:
                continue
            os.makedirs(full_path, exist_ok=True)


# ----------------------------
# GENERATE FOLDER HIERARCHY
# ----------------------------
def generate_hierarchy():
    base_path = path_entry.get()
    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid folder path.")
        return

    # --- Step 1: Interactive lazy-loaded exclusion tree ---
    def ask_exclusions_tree():
        popup = tk.Toplevel(root)
        popup.title("Select Folders to Exclude")
        popup.geometry("650x520")
        popup.configure(bg="#1e1e1e")
        popup.grab_set()

        tk.Label(
            popup, text="📁 Double-click folders to toggle exclusion. Expand as needed.",
            fg="white", bg="#1e1e1e", font=("Segoe UI", 10, "bold")
        ).pack(pady=(8, 2), anchor="w", padx=15)

        tk.Label(
            popup, text="(Excluded folders will still appear but their contents will be skipped)",
            fg="#9cdcfe", bg="#1e1e1e", font=("Segoe UI", 9)
        ).pack(anchor="w", padx=15)

        # Treeview setup
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1e1e1e", foreground="#ffffff",
            fieldbackground="#1e1e1e", borderwidth=0,
            font=("Consolas", 10)
        )
        style.map("Treeview", background=[("selected", "#007acc")])

        tree = ttk.Treeview(popup, show="tree")
        tree.pack(fill="both", expand=True, padx=15, pady=8)

        node_data = {}

        # Insert dummy child for folders so they can be expanded later
        def insert_node(parent, path):
            try:
                entries = os.listdir(path)
            except (PermissionError, FileNotFoundError):
                return
            for entry in entries:
                full_path = os.path.join(path, entry)
                is_dir = os.path.isdir(full_path)
                node = tree.insert(parent, "end", text="☐ " + entry, open=False)
                node_data[node] = {"path": full_path, "excluded": False, "is_dir": is_dir, "loaded": False}
                if is_dir:
                    # Insert dummy so the expand arrow appears
                    tree.insert(node, "end", text="loading...")

        # Expand event (lazy load)
        def on_open(event):
            item = tree.focus()
            if item not in node_data:
                return
            node = node_data[item]
            if node["is_dir"] and not node["loaded"]:
                # Remove dummy
                for child in tree.get_children(item):
                    tree.delete(child)
                insert_node(item, node["path"])
                node["loaded"] = True

        tree.bind("<<TreeviewOpen>>", on_open)

        # Toggle exclusion
        def toggle_node(event):
            item = tree.focus()
            if item not in node_data:
                return
            node = node_data[item]
            node["excluded"] = not node["excluded"]
            mark = "☑" if node["excluded"] else "☐"
            name = os.path.basename(node["path"])
            tree.item(item, text=f"{mark} {name}")
            # Propagate to children if already loaded
            for child in tree.get_children(item):
                toggle_child(child, node["excluded"])

        def toggle_child(item, state):
            if item not in node_data:
                return
            node_data[item]["excluded"] = state
            mark = "☑" if state else "☐"
            name = os.path.basename(node_data[item]["path"])
            tree.item(item, text=f"{mark} {name}")
            for child in tree.get_children(item):
                toggle_child(child, state)

        tree.bind("<Double-1>", toggle_node)

        # Root node
        root_node = tree.insert("", "end", text=os.path.basename(base_path), open=False)
        node_data[root_node] = {"path": base_path, "excluded": False, "is_dir": True, "loaded": False}
        # Insert top-level items lazily
        tree.insert(root_node, "end", text="loading...")

        result = []

        def confirm():
            nonlocal result
            result = [d["path"] for d in node_data.values() if d["excluded"]]
            popup.destroy()

        def cancel():
            nonlocal result
            result = None
            popup.destroy()

        btn_frame = tk.Frame(popup, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Confirm", bg="#007acc", fg="white", width=10, command=confirm).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", bg="#3a3d41", fg="white", width=10, command=cancel).pack(side="left", padx=5)

        popup.wait_window()
        return result

    excluded_paths = ask_exclusions_tree()
    if excluded_paths is None:
        messagebox.showinfo("Cancelled", "Operation cancelled by user.")
        return

    # --- Step 2: Build hierarchy (fast DFS, skip excluded) ---
    result = []
    base_name = os.path.basename(base_path.rstrip(os.sep))
    result.append(f"{base_name}/")

    excluded_set = set(excluded_paths)

    def build_tree(dir_path, prefix=""):
        try:
            entries = sorted(os.listdir(dir_path))
        except PermissionError:
            result.append(prefix + "└── [Permission Denied]")
            return

        for i, entry in enumerate(entries):
            full_path = os.path.join(dir_path, entry)
            connector = "└── " if i == len(entries) - 1 else "├── "
            result.append(prefix + connector + entry)
            if os.path.isdir(full_path):
                if full_path in excluded_set:
                    result.append(prefix + ("    " if i == len(entries) - 1 else "│   ") + "└── [excluded]")
                    continue
                next_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
                build_tree(full_path, next_prefix)

    build_tree(base_path)

    hierarchy_text = "\n".join(result)
    preview_text.delete("1.0", tk.END)
    preview_text.insert("1.0", hierarchy_text)
    messagebox.showinfo("Done", "✅ Folder hierarchy generated successfully!")


# ----------------------------
# open_code_collector
# ----------------------------
def open_code_collector():
    base_path = path_entry.get()
    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid project folder first.")
        return

    popup = tk.Toplevel(root)
    popup.title("Select Files to Combine")
    popup.geometry("700x540")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    # --- Title + Info Label ---
    tk.Label(
        popup,
        text="📂 Select files to combine (Tree View):",
        fg="white", bg="#1e1e1e",
        font=("Segoe UI", 10, "bold")
    ).pack(pady=(10, 2), anchor="w", padx=15)

    tk.Label(
        popup,
        text="💡 Double-click any file or folder to select/deselect it.",
        fg="#9cdcfe", bg="#1e1e1e",
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=15)

    # --- Treeview styling ---
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#1e1e1e",
                    foreground="#ffffff",
                    fieldbackground="#1e1e1e",
                    borderwidth=0,
                    font=("Consolas", 10))
    style.map("Treeview", background=[("selected", "#007acc")])

    tree = ttk.Treeview(popup, show="tree")
    tree.pack(fill="both", expand=True, padx=15, pady=5)

    file_vars = {}

    # --- Recursive function to add items ---
    def insert_node(parent, path):
        for entry in sorted(os.listdir(path)):
            full_path = os.path.join(path, entry)
            node = tree.insert(parent, "end", text="☐ " + entry, open=False)
            file_vars[node] = {"path": full_path, "checked": False}

            if os.path.isdir(full_path):
                insert_node(node, full_path)

    root_node = tree.insert("", "end", text=os.path.basename(base_path), open=False)
    file_vars[root_node] = {"path": base_path, "checked": False}
    insert_node(root_node, base_path)

    # --- Helper: recursively set children checked/unchecked ---
    def set_children_checked(item, checked):
        if item not in file_vars:
            return
        file_vars[item]["checked"] = checked
        name = os.path.basename(file_vars[item]["path"])
        tree.item(item, text=("☑ " if checked else "☐ ") + name)
        for child in tree.get_children(item):
            set_children_checked(child, checked)

    # --- On double click toggle ---
    def on_double_click(event):
        item = tree.focus()
        if item not in file_vars:
            return

        data = file_vars[item]
        new_state = not data["checked"]
        set_children_checked(item, new_state)

    tree.bind("<Double-1>", on_double_click)

    # --- Combine Selected Files ---
    def combine_selected_files():
        combined = ""
        for data in file_vars.values():
            if data["checked"] and os.path.isfile(data["path"]):
                try:
                    with open(data["path"], "r", encoding="utf-8", errors="ignore") as f:
                        combined += f"\n\n# ===== {os.path.relpath(data['path'], base_path)} =====\n"
                        combined += f.read()
                except Exception as e:
                    combined += f"\n\n# [Error reading {data['path']}: {e}]"

        if not combined.strip():
            messagebox.showwarning("No Selection", "Please select at least one file.")
            return

        input_text.delete("1.0", tk.END)
        input_text.insert("1.0", combined)
        popup.destroy()
        messagebox.showinfo("Done", "✅ Selected code combined into input editor!")

    # --- Bottom buttons ---
    btn_frame = tk.Frame(popup, bg="#1e1e1e")
    btn_frame.pack(pady=10)

    def expand_all():
        for item in tree.get_children():
            tree.item(item, open=True)
            expand_children(item)

    def expand_children(item):
        tree.item(item, open=True)
        for child in tree.get_children(item):
            expand_children(child)

    def collapse_all():
        for item in tree.get_children():
            tree.item(item, open=False)

    tk.Button(btn_frame, text="Expand All", bg="#3a3d41", fg="white", width=12,
              command=expand_all).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Collapse All", bg="#3a3d41", fg="white", width=12,
              command=collapse_all).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Combine & View", command=combine_selected_files,
              bg="#007acc", fg="white", width=15).pack(side=tk.LEFT, padx=5)


# ----------------------------
# GENERATE FILES FROM COMBINED CODE
# ----------------------------
def generate_files_from_combined_code():
    base_path = path_entry.get().strip()
    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid target folder path first.")
        return

    text = input_text.get("1.0", tk.END)
    if not text.strip():
        messagebox.showwarning("Empty", "Please paste the combined code in the left box first.")
        return

    # Regex pattern to find file headers like "# ===== path/to/file.ext ====="
    pattern = r"#\s*={2,}\s*(.*?)\s*={2,}\s*"
    parts = re.split(pattern, text)
    if len(parts) < 3:
        messagebox.showerror("Invalid Format", "No file headers found. Use format:\n# ===== relative\\path\\file.ext =====")
        return

    # Split result: [before first header, path1, content1, path2, content2, ...]
    created, skipped = [], []
    for i in range(1, len(parts), 2):
        rel_path = parts[i].strip().replace("\\", os.sep).replace("/", os.sep)
        content = parts[i + 1] if i + 1 < len(parts) else ""

        full_path = os.path.join(base_path, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if os.path.exists(full_path):
            answer = messagebox.askyesno("File Exists", f"File already exists:\n{rel_path}\n\nOverwrite?")
            if not answer:
                skipped.append(rel_path)
                continue

        try:
            with open(full_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(content.strip() + "\n")
            created.append(rel_path)
        except Exception as e:
            skipped.append(f"{rel_path} (error: {e})")

    summary = f"✅ Created: {len(created)} file(s)\n⚠️ Skipped: {len(skipped)} file(s)"
    if created:
        summary += "\n\nCreated Files:\n" + "\n".join(created[:10])
        if len(created) > 10:
            summary += f"\n...and {len(created) - 10} more"

    messagebox.showinfo("Generation Complete", summary)



# ----------------------------
# GUI FUNCTIONS
# ----------------------------
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

def make_structure():
    base_path = path_entry.get()
    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid folder path.")
        return

    structure_text = input_text.get("1.0", tk.END).strip()
    if not structure_text:
        messagebox.showerror("Error", "Please paste your project structure.")
        return

    structure = parse_structure(structure_text)
    try:
        create_structure(base_path, structure)
        messagebox.showinfo("Done", "✅ Project structure created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed: {e}")

def preview_structure():
    user_text = input_text.get("1.0", tk.END).strip()
    current_preview = preview_text.get("1.0", tk.END).strip()
    if user_text == current_preview and user_text != "":
        messagebox.showinfo("Match", "✅ Structure Matched — No Changes Needed.")
        return
    preview_text.delete("1.0", tk.END)
    preview_text.insert("1.0", user_text)

def paste_from_clipboard():
    try:
        clipboard_content = root.clipboard_get()
        if clipboard_content:
            input_text.delete("1.0", tk.END)
            input_text.insert("1.0", clipboard_content)
    except tk.TclError:
        messagebox.showerror("Clipboard", "❌ Clipboard is empty or unavailable.")

def handle_drop(event):
    data = event.data.strip("{}")
    if os.path.isdir(data):
        path_entry.delete(0, tk.END)
        path_entry.insert(0, data)
    else:
        messagebox.showerror("Invalid", "Please drag a valid folder.")

# ----------------------------
# UI SETUP
# ----------------------------
AppClass = TkinterDnD.Tk if DND_AVAILABLE else tk.Tk
root = AppClass()
root.title("Project Structure Creator (DFS + Drag & Drop + Hierarchy Generator)")
root.geometry("850x600")
root.configure(bg="#1e1e1e")

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

# Folder selection
tk.Label(frame, text="Target Folder Path:", fg="white", bg="#1e1e1e", font=("Segoe UI", 10, "bold")).pack(anchor="w")
path_frame = tk.Frame(frame, bg="#1e1e1e")
path_frame.pack(fill=tk.X, pady=5)

path_entry = tk.Entry(path_frame, bg="#2d2d2d", fg="white", insertbackground="white", font=("Consolas", 10))
path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
tk.Button(path_frame, text="Browse", command=browse_folder, bg="#007acc", fg="white", font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT, padx=5)

# ----------------------------
# TEXT AREAS + BUTTONS (NEW)
# ----------------------------
text_frame = tk.Frame(frame, bg="#1e1e1e")
text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# ==== Left: Paste Structure ====
left_frame = tk.Frame(text_frame, bg="#1e1e1e")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

tk.Label(left_frame, text="📋 Paste Your Structure:", fg="white", bg="#1e1e1e",
         font=("Segoe UI", 10, "bold")).pack(anchor="w")

input_text = scrolledtext.ScrolledText(
    left_frame, width=40, height=25,
    bg="#252526", fg="white", insertbackground="white",
    font=("Consolas", 10)
)
input_text.pack(fill=tk.BOTH, expand=True)

left_btns = tk.Frame(left_frame, bg="#1e1e1e")
left_btns.pack(fill="x", pady=5)

tk.Button(left_btns, text="📋 Copy", bg="#3a3d41", fg="white", width=10,
           command=lambda: root.clipboard_clear() or root.clipboard_append(input_text.get("1.0", tk.END).strip())
           ).pack(side=tk.LEFT, padx=5)

tk.Button(left_btns, text="🗑️ Clear", bg="#3a3d41", fg="white", width=10,
           command=lambda: input_text.delete("1.0", tk.END)
           ).pack(side=tk.LEFT, padx=5)

# ==== Right: Preview Structure ====
right_frame = tk.Frame(text_frame, bg="#1e1e1e")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(right_frame, text="👁️ Preview Structure:", fg="white", bg="#1e1e1e",
         font=("Segoe UI", 10, "bold")).pack(anchor="w")

preview_text = scrolledtext.ScrolledText(
    right_frame, width=40, height=25,
    bg="#252526", fg="white", insertbackground="white",
    font=("Consolas", 10)
)
preview_text.pack(fill=tk.BOTH, expand=True)

right_btns = tk.Frame(right_frame, bg="#1e1e1e")
right_btns.pack(fill="x", pady=5)

tk.Button(right_btns, text="📋 Copy", bg="#3a3d41", fg="white", width=10,
           command=lambda: root.clipboard_clear() or root.clipboard_append(preview_text.get("1.0", tk.END).strip())
           ).pack(side=tk.LEFT, padx=5)

tk.Button(right_btns, text="🗑️ Clear", bg="#3a3d41", fg="white", width=10,
           command=lambda: preview_text.delete("1.0", tk.END)
           ).pack(side=tk.LEFT, padx=5)

# ----------------------------
# MAIN BUTTONS SECTION
# ----------------------------
btn_frame = tk.Frame(frame, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="📥 Paste Clipboard", command=paste_from_clipboard, bg="#3a3d41", fg="white", width=16).pack(side=tk.LEFT, padx=6)
tk.Button(btn_frame, text="🧹 Remove Comments", command=remove_comments_from_input, bg="#e07b39", fg="white", width=18).pack(side=tk.LEFT, padx=6)
tk.Button(btn_frame, text="🪄 Generate Hierarchy", command=generate_hierarchy, bg="#6a9e2f", fg="white", width=20).pack(side=tk.LEFT, padx=6)
tk.Button(btn_frame, text="🧩 Collect Code", command=open_code_collector, bg="#9b59b6", fg="white", width=16).pack(side=tk.LEFT, padx=6)
tk.Button(btn_frame, text="👁️ Preview", command=preview_structure, bg="#3a3d41", fg="white", width=12).pack(side=tk.LEFT, padx=6)
tk.Button(btn_frame, text="🏗️ Make It", command=make_structure, bg="#007acc", fg="white", width=12).pack(side=tk.LEFT, padx=6)
tk.Button(btn_frame, text="🧩 Generate Files", command=generate_files_from_combined_code,
          bg="#2e8b57", fg="white", width=16).pack(side=tk.LEFT, padx=6)


# Drag & drop
if DND_AVAILABLE:
    for widget in [root, frame, path_entry, input_text, preview_text]:
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind("<<Drop>>", handle_drop)

root.mainloop()
