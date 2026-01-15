import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import re
import csv
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from datetime import datetime

# -----------------------------
# Regex Patterns (updated and corrected)
# -----------------------------
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
phone_number_pattern = re.compile(r"(?:\+?92|0)3\d{2}[- ]?\d{7}")
cnic_number_pattern = re.compile(r"\d{5}[-_. ]?\d{7}[-_. ]?\d")
url_pattern = re.compile(r"\b(?:(?:https?|ftp):\/\/)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:\/[^\s]*)?\b")
date_pattern = re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\b")
password_pattern = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}")

# IPv4 (fixed non-capturing)
ipv4_pattern = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b"
)

# IPv6 (simplified non-capturing)
ipv6_pattern = re.compile(
    r"\b(?:[A-Fa-f0-9]{1,4}:){1,7}[A-Fa-f0-9]{1,4}\b"
)

patterns = {
    "Email": email_pattern,
    "Phone Number": phone_number_pattern,
    "CNIC Number": cnic_number_pattern,
    "URL": url_pattern,
    "Date": date_pattern,
    "Password": password_pattern,
    "IPv4": ipv4_pattern,
    "IPv6": ipv6_pattern,
}

# -----------------------------
# Helper Functions
# -----------------------------
def read_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == ".csv":
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                text = "\n".join([",".join(row) for row in reader])
        elif ext == ".xlsx":
            df = pd.read_excel(file_path)
            text = "\n".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
        elif ext == ".docx":
            doc = Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext == ".pdf":
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        else:
            messagebox.showerror("Error", f"Unsupported file type: {ext}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
    return text


def process_file(text=None, file_paths=None):
    operation = operation_var.get()

    if not file_paths and not text:
        messagebox.showwarning("Warning", "Please select or paste a file.")
        return
    if not operation:
        messagebox.showwarning("Warning", "Please select an operation.")
        return

    if file_paths:
        for file_path in file_paths:
            text = read_file_content(file_path)
            if not text:
                continue

            pattern = patterns[operation]
            matches = re.findall(pattern, text)

            clean_matches = []
            for m in matches:
                if isinstance(m, tuple):
                    flat = " ".join(filter(None, m))
                    if flat.strip():
                        clean_matches.append(flat.strip())
                elif isinstance(m, str):
                    clean_matches.append(m.strip())

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = f"{base_name}_{operation}_output_{timestamp}.txt"

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"File processed: {file_path}\n")
                f.write(f"Operation: {operation}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("---------------------------------\n\n")
                for match in clean_matches:
                    f.write(match + "\n")
                f.write("\n---------------------------------\n")
                f.write(f"Total {operation}s found: {len(clean_matches)}\n")

        messagebox.showinfo(
            "Success",
            f"Processed {len(file_paths)} file(s).\nCheck your directory for generated TXT outputs.",
        )

    elif text:
        pattern = patterns[operation]
        matches = re.findall(pattern, text)

        clean_matches = []
        for m in matches:
            if isinstance(m, tuple):
                flat = " ".join(filter(None, m))
                if flat.strip():
                    clean_matches.append(flat.strip())
            elif isinstance(m, str):
                clean_matches.append(m.strip())

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_path = f"clipboard_{operation}_output_{timestamp}.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Source: Clipboard Data\n")
            f.write(f"Operation: {operation}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("---------------------------------\n\n")
            for match in clean_matches:
                f.write(match + "\n")
            f.write("\n---------------------------------\n")
            f.write(f"Total {operation}s found: {len(clean_matches)}\n")

        messagebox.showinfo(
            "Success",
            f"Clipboard text processed.\nOutput saved as:\n{os.path.abspath(output_path)}",
        )


def browse_file():
    file_paths = filedialog.askopenfilenames(
        title="Select one or more files",
        filetypes=(
            ("All supported", "*.txt *.csv *.xlsx *.pdf *.docx"),
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx"),
        ),
    )
    if file_paths:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, "; ".join(file_paths))


def paste_clipboard():
    try:
        data = root.clipboard_get().strip()
        if os.path.isfile(data):
            file_entry.delete(0, tk.END)
            file_entry.insert(0, data)
            messagebox.showinfo("Clipboard", f"Loaded file path from clipboard:\n{data}")
        else:
            process_file(text=data)
    except Exception as e:
        messagebox.showerror("Error", f"Clipboard read failed: {e}")


# -----------------------------
# GUI Layout with global drag & drop + modern combobox
# -----------------------------
root = TkinterDnD.Tk()
root.title("Regex File Extractor")
root.geometry("600x350")

tk.Label(root, text="Select, Drop, or Paste File(s):").pack(pady=5)
file_frame = tk.Frame(root)
file_frame.pack()

file_entry = tk.Entry(file_frame, width=65)
file_entry.pack(side=tk.LEFT, padx=5)
tk.Button(file_frame, text="Browse", command=browse_file).pack(side=tk.LEFT)

# Enable global drag & drop
def on_drop(event):
    files = event.data.strip("{}").split()
    valid_files = [f for f in files if os.path.isfile(f)]
    if valid_files:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, "; ".join(valid_files))
    else:
        messagebox.showerror("Error", "Dropped item is not a valid file.")

# register entire window for drops
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

tk.Label(root, text="Select Operation:").pack(pady=5)
operation_var = tk.StringVar()

# modern combobox instead of option menu
operation_combo = ttk.Combobox(root, textvariable=operation_var, values=list(patterns.keys()), state="readonly", width=40)
operation_combo.pack(pady=5)
operation_combo.set("Select an operation")

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(button_frame, text="Process File(s)", bg="lightblue",
          command=lambda: process_file(file_paths=file_entry.get().split("; ") if file_entry.get() else None)).pack(side=tk.LEFT, padx=10)

tk.Button(button_frame, text="Paste from Clipboard", bg="lightgreen", command=paste_clipboard).pack(side=tk.LEFT, padx=10)

root.mainloop()
