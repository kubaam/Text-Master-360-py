import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

# ---------- Processing Helper Functions ----------

def read_files(file_list):
    """Read lines from each file in the file list."""
    all_lines = []
    for filepath in file_list:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                all_lines.extend(line.rstrip("\n") for line in lines)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading {os.path.basename(filepath)}: {e}")
            return None
    return all_lines

def remove_duplicate_lines(lines):
    """Remove duplicate lines while preserving order."""
    return list(dict.fromkeys(lines))

def filter_lines(lines, filter_words):
    """Remove lines containing any of the filter words."""
    if not filter_words:
        return lines
    filtered_lines = []
    for line in lines:
        if not any(fw.lower() in line.lower() for fw in filter_words):
            filtered_lines.append(line)
    return filtered_lines

def remove_duplicate_words_in_line(line):
    """Remove duplicate words within a single line."""
    words = line.split()
    seen = set()
    unique_words = []
    for word in words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    return " ".join(unique_words)

def clean_lines(lines):
    """Remove duplicate words within each line for all lines."""
    return [remove_duplicate_words_in_line(line) for line in lines]

# ---------- Global Variables ----------
selected_files = []

# ---------- GUI Functions for File Selection Tab ----------

def select_files():
    files = filedialog.askopenfilenames(title="Select text files", filetypes=[("Text Files", "*.txt")])
    if files:
        for file in files:
            if file not in selected_files:
                selected_files.append(file)
                files_listbox.insert(tk.END, file)

def clear_file_list():
    selected_files.clear()
    files_listbox.delete(0, tk.END)

# ---------- Processing Functions for Each Tab ----------

def process_remove_duplicate_lines():
    if not selected_files:
        messagebox.showwarning("No Files", "Please select at least one text file in the 'TXT Files' tab.")
        return
    all_lines = read_files(selected_files)
    if all_lines is None:
        return

    unique_lines = remove_duplicate_lines(all_lines)

    save_processed_lines(unique_lines, "Duplicate Lines Removed")

def process_filter_lines():
    if not selected_files:
        messagebox.showwarning("No Files", "Please select at least one text file in the 'TXT Files' tab.")
        return
    filter_input = filter_entry.get()
    filter_words = [word.strip() for word in filter_input.split(",") if word.strip()]

    all_lines = read_files(selected_files)
    if all_lines is None:
        return

    filtered_lines = filter_lines(all_lines, filter_words)

    save_processed_lines(filtered_lines, "Filtered Lines")

def process_remove_duplicate_words():
    if not selected_files:
        messagebox.showwarning("No Files", "Please select at least one text file in the 'TXT Files' tab.")
        return
    all_lines = read_files(selected_files)
    if all_lines is None:
        return

    cleaned = clean_lines(all_lines)

    save_processed_lines(cleaned, "Duplicate Words Removed")

def save_processed_lines(lines, title="Save File"):
    output_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt")],
                                               title=f"Save {title} As")
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as out_file:
                for line in lines:
                    out_file.write(line + "\n")
            messagebox.showinfo("Success", f"File saved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error writing to file: {e}")

# ---------- GUI Setup ----------

root = tk.Tk()
root.title("Text Processing Tool")

# Use a modern theme.
style = ttk.Style(root)
if "clam" in style.theme_names():
    style.theme_use("clam")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ----- Tab 1: TXT Files -----
tab_files = ttk.Frame(notebook)
notebook.add(tab_files, text="TXT Files")

files_frame = ttk.Frame(tab_files, padding="10")
files_frame.pack(fill=tk.BOTH, expand=True)

files_listbox = tk.Listbox(files_frame, height=10)
scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=files_listbox.yview)
files_listbox['yscrollcommand'] = scrollbar.set
files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5), pady=5)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

buttons_frame = ttk.Frame(tab_files, padding="10")
buttons_frame.pack(fill=tk.X)

add_button = ttk.Button(buttons_frame, text="Add Files", command=select_files)
add_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

clear_button = ttk.Button(buttons_frame, text="Clear List", command=clear_file_list)
clear_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

# ----- Tab 2: Remove Duplicate Lines -----
tab_dup_lines = ttk.Frame(notebook)
notebook.add(tab_dup_lines, text="Remove Duplicate Lines")

dup_lines_frame = ttk.Frame(tab_dup_lines, padding="20")
dup_lines_frame.pack(fill=tk.BOTH, expand=True)

remove_dup_button = ttk.Button(dup_lines_frame, text="Remove Duplicate Lines", command=process_remove_duplicate_lines)
remove_dup_button.pack(expand=True)

# ----- Tab 3: Filter Lines by Words -----
tab_filter = ttk.Frame(notebook)
notebook.add(tab_filter, text="Filter Lines by Words")

filter_frame = ttk.Frame(tab_filter, padding="20")
filter_frame.pack(fill=tk.BOTH, expand=True)

filter_label = ttk.Label(filter_frame, text="Enter words (comma-separated) to filter out lines:")
filter_label.pack(pady=(0,5))
filter_entry = ttk.Entry(filter_frame, width=50)
filter_entry.pack(pady=(0,10))

filter_button = ttk.Button(filter_frame, text="Filter Lines", command=process_filter_lines)
filter_button.pack()

# ----- Tab 4: Remove Duplicate Words -----
tab_dup_words = ttk.Frame(notebook)
notebook.add(tab_dup_words, text="Remove Duplicate Words")

dup_words_frame = ttk.Frame(tab_dup_words, padding="20")
dup_words_frame.pack(fill=tk.BOTH, expand=True)

remove_dup_words_button = ttk.Button(dup_words_frame, text="Remove Duplicate Words", command=process_remove_duplicate_words)
remove_dup_words_button.pack(expand=True)

root.mainloop()
