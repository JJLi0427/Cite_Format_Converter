import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re
from datetime import datetime
import json
import os

# Initialize the conversion history
conversion_history = []

# Load and save the conversion history
log_file_path = "conversion_history.log"

def load_history():
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            global conversion_history
            conversion_history = json.load(file)

def save_history():
    with open(log_file_path, "w") as file:
        json.dump(conversion_history, file)

def clear_history():
    global conversion_history
    conversion_history = []
    save_history()
    messagebox.showinfo("Info", "History cleared successfully.")
    show_main_frame()

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
        # Add the conversion to the history
        conversion_history.append({
            "citation": ieee_citation,
            "title": re.search(r'title={(.*?)}', ieee_citation).group(1),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_history()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_history():
    main_frame.pack_forget()
    history_frame.pack(fill="both", expand=True)

    history_listbox.delete(0, tk.END)
    for record in conversion_history:
        history_listbox.insert(tk.END, f"{record['title']} (Used on: {record['time']})")

def show_main_frame():
    history_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def copy_selected_citation():
    selected_index = history_listbox.curselection()
    if selected_index:
        selected_citation = conversion_history[selected_index[0]]['citation']
        ieee_entry.delete("1.0", tk.END)
        ieee_entry.insert(tk.END, selected_citation)
        show_main_frame()

# Load log file
load_history()

# Create main window
root = tk.Tk()
root.title("IEEE Citation Converter")
root.geometry("600x600")

# Create frames
main_frame = tk.Frame(root)
history_frame = tk.Frame(root)

# Load icon
icon = Image.open("converter.icns")
icon = icon.resize((100, 100), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon)

# Main frame widgets
icon_label = tk.Label(main_frame, image=icon)
icon_label.pack(pady=10)

ieee_label = tk.Label(main_frame, text="IEEE Citation:")
ieee_label.pack(pady=5)
ieee_entry = tk.Text(main_frame, height=5, width=50)
ieee_entry.pack(pady=5)

result_label = tk.Label(main_frame, text="Converted Citation:")
result_label.pack(pady=5)
result_text = tk.Text(main_frame, height=5, width=50)
result_text.pack(pady=5)

format_label = tk.Label(main_frame, text="Select Format:")
format_label.pack(pady=5)
format_var = tk.StringVar(value="gb")
format_combobox = ttk.Combobox(main_frame, textvariable=format_var)
format_combobox['values'] = ("gb", "apa", "mla")
format_combobox.pack(pady=5)

convert_button = tk.Button(main_frame, text="Convert", command=convert_citation)
convert_button.pack(pady=10)

history_button = tk.Button(main_frame, text="History", command=show_history)
history_button.pack(pady=10)

# History frame widgets
icon_label_history = tk.Label(history_frame, image=icon)
icon_label_history.pack(pady=10)

history_listbox = tk.Listbox(history_frame, height=15, width=80)
history_listbox.pack(pady=10)

copy_button = tk.Button(history_frame, text="Reuse Citation", command=copy_selected_citation)
copy_button.pack(pady=5)

clear_button = tk.Button(history_frame, text="Clear History", command=clear_history)
clear_button.pack(pady=5)

close_button = tk.Button(history_frame, text="Back", command=show_main_frame)
close_button.pack(pady=5)

# Pack the main frame initially
main_frame.pack(fill="both", expand=True)

# Start the main loop
root.mainloop()