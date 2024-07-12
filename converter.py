import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re
from datetime import datetime
import json
import os

# 初始化转换历史记录列表
conversion_history = []

# 日志文件路径
log_file_path = "conversion_history.log"

def load_history():
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            global conversion_history
            conversion_history = json.load(file)

def save_history():
    with open(log_file_path, "w") as file:
        json.dump(conversion_history, file)

def clear_history(history_window):
    global conversion_history
    conversion_history = []
    save_history()
    messagebox.showinfo("Info", "History cleared successfully.")
    history_window.destroy()

def extract_ieee_parts(ieee_citation):
    author = re.search(r'author={(.*?)}', ieee_citation).group(1)
    title = re.search(r'title={(.*?)}', ieee_citation).group(1)
    booktitle = re.search(r'booktitle={(.*?)}', ieee_citation).group(1)
    year = re.search(r'year={(.*?)}', ieee_citation).group(1)
    pages = re.search(r'pages={(.*?)}', ieee_citation).group(1)
    doi = re.search(r'doi={(.*?)}', ieee_citation).group(1)
    return author, title, booktitle, year, pages, doi

def format_authors(authors, format_type):
    names = authors.split(' and ')
    if format_type == "gb":
        return ', '.join(names)
    elif format_type == "apa":
        return ', '.join(names)
    elif format_type == "mla":
        return ', and '.join(names)
    return authors

def ieee_to_gb(author, title, booktitle, year, pages, doi):
    formatted_authors = format_authors(author, "gb")
    return f"{formatted_authors}. {title}[C]//{booktitle}, {year}: {pages}. DOI: {doi}."

def ieee_to_apa(author, title, booktitle, year, pages, doi):
    formatted_authors = format_authors(author, "apa")
    return f"{formatted_authors}. ({year}). {title}. In {booktitle} (pp. {pages.split('-')[0]}-{pages.split('-')[1]}). DOI: {doi}."

def ieee_to_mla(author, title, booktitle, year, pages, doi):
    formatted_authors = format_authors(author, "mla")
    return f"{formatted_authors}. \"{title}.\" {booktitle}, {year}, pp. {pages}. DOI: {doi}."

def convert_ieee_citation(ieee_citation, format_type):
    author, title, booktitle, year, pages, doi = extract_ieee_parts(ieee_citation)
    if format_type == "gb":
        return ieee_to_gb(author, title, booktitle, year, pages, doi)
    elif format_type == "apa":
        return ieee_to_apa(author, title, booktitle, year, pages, doi)
    elif format_type == "mla":
        return ieee_to_mla(author, title, booktitle, year, pages, doi)
    return "Unsupported format type"

def convert_citation():
    ieee_citation = ieee_entry.get("1.0", tk.END).strip()
    format_type = format_var.get()
    if not ieee_citation or not format_type:
        messagebox.showerror("Error", "Please enter IEEE citation and select a format.")
        return
    try:
        converted_citation = convert_ieee_citation(ieee_citation, format_type)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, converted_citation)
        # 添加到转换历史记录
        conversion_history.append({
            "citation": ieee_citation,
            "title": re.search(r'title={(.*?)}', ieee_citation).group(1),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_history()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Conversion History")
    history_window.geometry("600x600")

    history_listbox = tk.Listbox(history_window, height=15, width=80)
    history_listbox.pack(pady=10)

    for record in conversion_history:
        history_listbox.insert(tk.END, f"{record['title']} (Used on: {record['time']})")

    def copy_selected_citation():
        selected_index = history_listbox.curselection()
        if selected_index:
            selected_citation = conversion_history[selected_index[0]]['citation']
            ieee_entry.delete("1.0", tk.END)
            ieee_entry.insert(tk.END, selected_citation)
            history_window.destroy()

    copy_button = tk.Button(history_window, text="Reuse Citation", command=copy_selected_citation)
    copy_button.pack(pady=5)

    clear_button = tk.Button(history_window, text="Clear History", command=lambda: clear_history(history_window))
    clear_button.pack(pady=5)

    close_button = tk.Button(history_window, text="Close Window", command=history_window.destroy)
    close_button.pack(pady=5)

# 加载历史记录
load_history()

# Create main window
root = tk.Tk()
root.title("IEEE Citation Converter")
root.geometry("600x600")

# Load and resize the icon
icon = Image.open("converter.icns")
icon = icon.resize((100, 100), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon)

# Create a label to display the icon
icon_label = tk.Label(root, image=icon)
icon_label.pack(pady=10)

# IEEE Citation input
ieee_label = tk.Label(root, text="IEEE Citation:")
ieee_label.pack(pady=5)
ieee_entry = tk.Text(root, height=5, width=50)
ieee_entry.pack(pady=5)

# Format selection
format_label = tk.Label(root, text="Select Format:")
format_label.pack(pady=5)
format_var = tk.StringVar(value="gb")  # Set default value to "gb"
format_combobox = ttk.Combobox(root, textvariable=format_var)
format_combobox['values'] = ("gb", "apa", "mla")
format_combobox.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert_citation)
convert_button.pack(pady=10)

# Result display
result_label = tk.Label(root, text="Converted Citation:")
result_label.pack(pady=5)
result_text = tk.Text(root, height=5, width=50)
result_text.pack(pady=5)

# History button
history_button = tk.Button(root, text="History", command=show_history)
history_button.pack(pady=10)

# Start the main loop
root.mainloop()