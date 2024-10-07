import os
import re
import csv
from datetime import datetime
import fitz  # PyMuPDF
from tqdm import tqdm

def extract_match(pattern, text, default=""):
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else default

def parse_date(date_string):
    if date_string == "Unknown":
        return date_string
    try:
        parsed_date = datetime.strptime(date_string, "%d-%b-%Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown"

def extract_info_from_pdf(pdf_path):
    filename = os.path.basename(pdf_path)
    pdf_doc = fitz.open(pdf_path)
    page = pdf_doc.load_page(0)
    extracted_text = page.get_text()

    hookup_date = extract_match(r"Medications:?\n(\d+-\w+-\d+)\nHookup Date:?", extracted_text, "Unknown")
    formatted_hookup_date = parse_date(hookup_date)

    return {
        'PID': extract_match(r"Patient Name.*?\n(.*?)\nID", extracted_text),
        'HookupDate': formatted_hookup_date,
        'HookupTime': extract_match(r"Hookup Date:?\n(\d+:\d+:\d+)\nHookup Time:?", extracted_text, "Unknown"),
        'Duration': extract_match(r"Hookup Time:?\n(\d+:\d+:\d+)\nDuration:?", extracted_text, "Unknown"),
        'Age': extract_match(r"ID.*?\n(\d+)\s*(?:yr)?\s*\nAge", extracted_text),
        'Gender': extract_match(r"Age.*?\n(Male|Female)\s*\nGender", extracted_text),
    }

def process_pdfs_to_csv(input_dir, output_path):
    all_data = []
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return

    for filename in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        pdf_path = os.path.join(input_dir, filename)
        pdf_data = extract_info_from_pdf(pdf_path)
        all_data.append(pdf_data)
    
    if all_data:
        keys = all_data[0].keys()
        with open(output_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(all_data)
        print(f"CSV file saved to {output_path}")
    else:
        print("No data extracted from PDF files.")

if __name__ == "__main__":
    input_directory = r"D:\extract"
    output_csv_path = r"C:\Users\SNUH\Desktop\extracted_data.csv"
    process_pdfs_to_csv(input_directory, output_csv_path)