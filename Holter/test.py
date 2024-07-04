import os
import fitz  # PyMuPDF
import csv
from tqdm import tqdm
import re

def extract_headings_from_page(page_text):
    headings = {
        "General": [],
        "Heart Rates": [],
        "Ventriculars (V, F, E, I)": [],
        "Supraventriculars (S, J, A)": []
    }

    lines = page_text.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()
        if "General" in line:
            current_section = "General"
        elif "Heart Rates" in line:
            current_section = "Heart Rates"
        elif "Ventriculars (V, F, E, I)" in line:
            current_section = "Ventriculars (V, F, E, I)"
        elif "Supraventriculars (S, J, A)" in line:
            current_section = "Supraventriculars (S, J, A)"
        elif current_section:
            if line and not line[0].isdigit():  # skip lines that start with numbers
                if line.startswith('ST Lead') or line.startswith('Date') or line.startswith('Signed') or line.startswith('Page') or line.startswith('Version'):
                    current_section = None
                else:
                    headings[current_section].append(line)
            elif current_section and re.match(r'^\d+', line):
                # Remove the numeric part at the beginning and clean the text
                subheading = re.sub(r'^\d+ ', '', line)
                subheading = re.sub(r' at.*', '', subheading)  # Remove "at ..." parts
                subheading = re.sub(r',.*', '', subheading)    # Remove ", ..." parts
                subheading = re.sub(r' \(\d+% total\)', '', subheading)  # Remove percentage parts
                subheading = re.sub(r' \d+ bpm.*', '', subheading)  # Remove "bpm ..." parts
                subheading = re.sub(r' \d+\.\d+ Seconds', ' Seconds', subheading)  # Standardize "Seconds Max R-R"
                subheading = re.sub(r' Runs totaling \d+ beats', 'Runs totaling beats', subheading)  # Standardize "Runs totaling beats"
                if subheading not in headings[current_section]:  # Add only if it's not already in the list
                    headings[current_section].append(subheading)

    return headings

def process_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        first_page = doc[0]
        first_page_text = first_page.get_text("text")
        return extract_headings_from_page(first_page_text)
    except fitz.EmptyFileError:
        print(f"Error: Cannot open empty document: {file_path}")
        return None

def save_to_csv(data, output_file):
    unique_rows = set()
    for sections in data.values():
        for section, subheadings in sections.items():
            for subheading in subheadings:
                unique_rows.add((section, subheading))

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Section", "Subheading"])
        for row in unique_rows:
            writer.writerow(row)

def main():
    input_dirs = ["Z:\\Holter\\extract\\Holter_gangnam_extract", "Z:\\Holter\\extract\\Holter_main_extract"]
    output_file = "Z:\\Holter\\extracted_holter_data.csv"

    extracted_data = {}

    for input_dir in input_dirs:
        pdf_files = [os.path.join(root, file)
                     for root, _, files in os.walk(input_dir)
                     for file in files if file.endswith(".pdf")]

        for file_path in tqdm(pdf_files, desc=f"Processing directory {input_dir}"):
            headings = process_pdf(file_path)
            if headings:  # Only add to extracted_data if headings are not None
                extracted_data[os.path.basename(file_path)] = headings  

    save_to_csv(extracted_data, output_file)
    print(f"Data has been extracted and saved to {output_file}")

if __name__ == "__main__":
    main()
