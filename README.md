# Python Utility Toolkit 🧰

A collection of small but powerful Python “life-saving” scripts focused on automation, security, file management, regular expressions, backups, monitoring, and GUI-based developer utilities. Each script solves a real-world problem and can be used independently.

---

## 🔐 1. Message Encoder & Decoder

**Description:**  
A simple Python-based text encoding and decoding tool that converts user messages into obfuscated strings using random characters and reversible logic.

**Key Features:**
- Encode messages with random characters
- Decode messages back to original text
- Lightweight and beginner-friendly
- Uses `random` and `string` modules

---

## 📂 2. Automatic File Organizer

**Description:**  
Automatically organizes files in a directory based on their file extensions to keep folders clean and manageable.

**Key Features:**
- Organizes files by extension
- Creates folders automatically
- Handles duplicate filenames safely
- Uses current working directory by default

---

## 🔐 3. File Encryption & Decryption Tool

**Description:**  
A secure file encryption and decryption tool that protects sensitive files using strong cryptographic techniques.

**Key Features:**
- Symmetric encryption (Fernet-based)
- Secure key generation and storage
- Deletes original file after encryption
- Menu-driven CLI interface

---

## ✏️ 4. Batch File Renamer (Regex-Based)

**Description:**  
A batch renaming tool that renames multiple files using patterns, prefixes, suffixes, numbering, and regular expressions.

**Key Features:**
- Regex-based renaming
- Add prefixes and suffixes
- Optional sequential numbering
- Filter by extension or rename all files

---

## 📊 5. Folder Size Analyzer

**Description:**  
Analyzes directories, calculates folder sizes recursively, and saves the results in a readable report.

**Key Features:**
- Recursive folder size calculation
- Sorted size output
- Progress indicator
- Saves results to `folder_sizes.txt`

---

## 🕵️ 6. Hidden Files & Folders Scanner

**Description:**  
Scans directories to detect hidden files and folders across Windows, Linux, and macOS.

**Key Features:**
- Cross-platform hidden file detection
- Recursive directory scanning
- Execution time tracking
- Saves results to `hidden_files.txt`

---

## 📧 7. Email, Phone & Link Extractor (Regex)

**Description:**  
A regular-expression–heavy text analysis tool that extracts sensitive and structured data from files.

**Key Features:**
- Extracts emails, phone numbers, URLs, CNICs, IPs, dates & passwords
- Advanced regex patterns
- Removes duplicate entries
- Supports TXT, CSV, XLSX, DOCX & PDF
- Timestamped output files

---

## 🌳 8. Directory Structure Generator

**Description:**  
Generates a tree-style directory structure representation and saves it as a text report.

**Key Features:**
- Tree-style visualization
- Recursive traversal
- Handles permission errors gracefully
- Outputs to `directory_report.txt`

---

## 📁 9. File Extension Copy Tool

**Description:**  
Copies files from a source directory to a destination directory based on file extension with preview and confirmation.

**Key Features:**
- Copy files by extension (pdf, jpg, mp4, etc.)
- File preview before execution
- User confirmation for safety
- Uses `pathlib` and `shutil`

---

## 🌳 10. Advanced Directory Reporter (Email Support)

**Description:**  
Performs deep directory scans and generates detailed reports, then emails them automatically.

**Key Features:**
- Recursive directory scanning
- Human-readable file sizes
- Hidden file detection
- Timestamped reports
- SMTP email delivery

---

## 👁️ 11. Real-Time File & Folder Activity Monitor

**Description:**  
Monitors file system activity in real time for auditing and tracking changes.

**Key Features:**
- Real-time monitoring using `watchdog`
- Tracks creation, deletion, modification, renaming
- Excludes system and junk files
- Persistent log file

---

## ⚡ 12. High-Speed Folder Size Analyzer (Multiprocessing)

**Description:**  
A performance-optimized folder size analyzer that uses multiprocessing for faster execution.

**Key Features:**
- Utilizes all CPU cores
- Recursive scanning
- Live progress display
- Handles permission errors safely

---

## 🔄 13. Smart Incremental Backup System (ZIP + Excel)

**Description:**  
An intelligent incremental backup system that updates a ZIP backup only when changes occur and logs activity.

**Key Features:**
- Real-time monitoring
- Incremental backup logic
- Single ZIP archive
- Excel-based backup logs
- JSON backup state tracking
- Excludes junk folders (.git, node_modules, etc.)

---

## 🧩 14. Project Structure Creator & Code Generator (GUI)

**Description:**  
A powerful Tkinter-based GUI application to visualize, generate, and manage project structures, collect code, and regenerate full projects from combined sources.

### Key Features:
- Paste tree-style folder structures (DFS)
- Preview structure before creation
- Auto-create folders and files
- Smart overwrite checklist
- Interactive directory hierarchy explorer
- Selective folder exclusion
- Code collector with path preservation
- File regeneration from merged source
- Clipboard and drag-and-drop support
- Clean dark-themed UI

---

## 🧠 Core Technologies Used

- Python Regular Expressions (Regex)
- Tkinter GUI
- File system traversal (DFS)
- Binary file handling
- Excel automation
- Multiprocessing
- Real-time file monitoring
- Document automation (PDF, DOCX, XLSX, PPTX)

---

## 👨‍💻 Author

**Muhammad Bilal**

A collection of real-world Python hacks built to solve practical problems efficiently.

---

## 📜 License

MIT License – free to use, modify, and share.
