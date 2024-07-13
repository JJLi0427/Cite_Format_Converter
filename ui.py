import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import func as fn

def convert_citation():
    ieee_citation = ieee_entry.get("1.0", tk.END).strip()
    format_type = format_var.get()
    if not ieee_citation or not format_type:
        messagebox.showerror("Error", "Please enter IEEE citation and select a format.")
        return
    try:
        converted_citation = fn.convert_ieee_citation(ieee_citation, format_type)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, converted_citation)
        # Add the conversion to the history
        fn.conversion_history.append({
            "citation": ieee_citation,
            "title": re.search(r'title={(.*?)}', ieee_citation).group(1),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        fn.save_history()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_history():
    main_frame.pack_forget()
    history_frame.pack(fill="both", expand=True)

    history_listbox.delete(0, tk.END)
    for record in fn.conversion_history:
        history_listbox.insert(tk.END, f"{record['title']} (Used on: {record['time']})")

def show_main_frame():
    history_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def copy_selected_citation():
    selected_index = history_listbox.curselection()
    if selected_index:
        selected_citation = fn.conversion_history[selected_index[0]]['citation']
        ieee_entry.delete("1.0", tk.END)
        ieee_entry.insert(tk.END, selected_citation)
        show_main_frame()

def clear_history():
    fn.clear_history()
    messagebox.showinfo("Info", "History cleared successfully.")
    show_main_frame()

# Create main window
root = tk.Tk()
root.title("IEEE Citation Converter")
root.geometry("560x560")

# Create frames
main_frame = tk.Frame(root)
history_frame = tk.Frame(root)

# Load icon
icon = Image.open("./photos/converter.icns")
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
format_var = tk.StringVar(value="GB")
format_combobox = ttk.Combobox(main_frame, textvariable=format_var)
format_combobox['values'] = ("GB", "APA", "MLA")
format_combobox.pack(pady=5)

convert_button = tk.Button(main_frame, text="Convert", command=convert_citation)
convert_button.pack(pady=10)

history_button = tk.Button(main_frame, text="History", command=show_history)
history_button.pack(pady=10)

# History frame widgets
icon_label_history = tk.Label(history_frame, image=icon)
icon_label_history.pack(pady=10)

history_listbox = tk.Listbox(history_frame, height=15, width=80)
history_listbox.pack(pady=20, padx=40)

copy_button = tk.Button(history_frame, text="Reuse Citation", command=copy_selected_citation)
copy_button.pack(pady=5)

clear_button = tk.Button(history_frame, text="Clear History", command=clear_history)
clear_button.pack(pady=5)

close_button = tk.Button(history_frame, text="Back to Home", command=show_main_frame)
close_button.pack(pady=5)

# Pack the main frame initially
main_frame.pack(fill="both", expand=True)