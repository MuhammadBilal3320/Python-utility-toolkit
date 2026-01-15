import os
import re
import csv
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from datetime import datetime

# -----------------------------
# Regex Patterns
# -----------------------------
patterns = {
    "1": ("Email", re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")),
    "2": ("Phone", re.compile(r"(?:\+?92|0)3\d{2}[- ]?\d{7}")),
    "3": ("CNIC", re.compile(r"\d{5}[-_. ]?\d{7}[-_. ]?\d")),
    "4": ("URL", re.compile(r"\b(?:(?:https?|ftp):\/\/)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:\/[^\s]*)?\b")),
    "5": ("Date", re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\b")),
    "6": ("Password", re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}")),
    "7": ("IPv4", re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b"
    )),
    "8": ("IPv6", re.compile(
        r"\b(?:[A-Fa-f0-9]{1,4}:){1,7}[A-Fa-f0-9]{1,4}\b"
    )),
}

# -----------------------------
# Read File Content
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
            print(f"[Error] Unsupported file type: {ext}")
    except Exception as e:
        print(f"[Error] Could not read file: {e}")
    return text


# -----------------------------
# Process File
# -----------------------------
def process_file(file_path, operation_name, pattern):
    text = read_file_content(file_path)
    if not text:
        print("[Error] File could not be read or is empty.")
        return

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
    output_path = f"{base_name}_{operation_name}_output_{timestamp}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"File processed: {file_path}\n")
        f.write(f"Operation: {operation_name}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("---------------------------------\n\n")
        for match in clean_matches:
            f.write(match + "\n")
        f.write("\n---------------------------------\n")
        f.write(f"Total {operation_name}s found: {len(clean_matches)}\n")

    print(f"\n[+] {len(clean_matches)} {operation_name}(s) found.")
    print(f"[+] Output saved as: {os.path.abspath(output_path)}\n")


# -----------------------------
# CLI Menu
# -----------------------------
def main():
    print("=== Regex Extractor CLI ===")
    file_path = input("Enter the input file name (with extension): ").strip()

    if not os.path.isfile(file_path):
        print("[Error] File not found.")
        return

    print("\nSelect an operation:")
    for key, (name, _) in patterns.items():
        print(f"{key}. {name}")

    choice = input("\nEnter your choice number: ").strip()

    if choice not in patterns:
        print("[Error] Invalid choice.")
        return

    operation_name, pattern = patterns[choice]
    process_file(file_path, operation_name, pattern)


if __name__ == "__main__":
    main()
