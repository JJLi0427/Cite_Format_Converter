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
    if format_type == "GB":
        return ', '.join(names)
    elif format_type == "APA":
        return ', '.join(names)
    elif format_type == "MLA":
        return ', and '.join(names)
    return authors

def ieee_to_gb(author, title, booktitle, year, pages, doi):
    formatted_authors = format_authors(author, "GB")
    return f"{formatted_authors}. {title}[C]//{booktitle}, {year}: {pages}. DOI: {doi}."

def ieee_to_apa(author, title, booktitle, year, pages, doi):
    formatted_authors = format_authors(author, "APA")
    return f"{formatted_authors}. ({year}). {title}. In {booktitle} (pp. {pages.split('-')[0]}-{pages.split('-')[1]}). DOI: {doi}."

def ieee_to_mla(author, title, booktitle, year, pages, doi):
    formatted_authors = format_authors(author, "MLA")
    return f"{formatted_authors}. \"{title}.\" {booktitle}, {year}, pp. {pages}. DOI: {doi}."

def convert_ieee_citation(ieee_citation, format_type):
    author, title, booktitle, year, pages, doi = extract_ieee_parts(ieee_citation)
    if format_type == "GB":
        return ieee_to_gb(author, title, booktitle, year, pages, doi)
    elif format_type == "APA":
        return ieee_to_apa(author, title, booktitle, year, pages, doi)
    elif format_type == "MLA":
        return ieee_to_mla(author, title, booktitle, year, pages, doi)
    return "Unsupported format type"