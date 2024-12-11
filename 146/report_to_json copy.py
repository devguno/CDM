import os
import re
import json
import fitz  # PyMuPDF
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import numpy as np
import tabula

def extract_match(pattern, text, default="Unknown", flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1) if match else default

def extract_grouped_matches(pattern, text, groups, default="Unknown"):
    match = re.search(pattern, text)
    if match:
        return [match.group(i + 1) for i in range(groups)]
    return [default] * groups

def parse_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%d-%b-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return date_string

def parse_general_section(text):
    general_section = re.search(r"General\n(.+?)Heart Rates", text, re.DOTALL)
    if general_section:
        general_text = general_section.group(1)
        qrs_complexes = extract_match(r"(\d+) QRS complexes", general_text)
        ventricular_beats = extract_match(r"(\d+) Ventricular beats", general_text)
        supraventricular_beats = extract_match(r"(\d+) Supraventricular beats", general_text)
        noise_percentage = extract_match(r"(<\s*\d+|\d+) % of total time classified as noise", general_text, "0")
        paced_beats = extract_match(r"(\d+) Paced beats", general_text)
        af_afl_percentage = extract_match(r"(<\s*\d+|\d+) % of total time in AF/AFL", general_text)
        bb_beats = extract_match(r"(\d+) BB beats", general_text)
        junctional_beats = extract_match(r"(\d+) Junctional beats", general_text)
        aberrant_beats = extract_match(r"(\d+) Aberrant beats", general_text)
    else:
        qrs_complexes = ventricular_beats = supraventricular_beats = noise_percentage = "Unknown"
        paced_beats = af_afl_percentage = bb_beats = junctional_beats = aberrant_beats = "Unknown"
    return {
        'QRScomplexes': qrs_complexes,
        'VentricularBeats': ventricular_beats,
        'SupraventricularBeats': supraventricular_beats,
        'NoisePercentage': noise_percentage,
        'PacedBeats': paced_beats,
        'AFAFLPercentage': af_afl_percentage,
        'BBBeats': bb_beats,
        'JunctionalBeats': junctional_beats,
        'AberrantBeats': aberrant_beats
    }

def parse_heart_rates_section(text):
    heart_rates_data = {}
    patterns = [
        (r"(\d+) Minimum at ([\d:]+ \d+-\w+)", 'MinimumRate', 'Timestamp'),
        (r"(\d+) Average", 'AverageRate', None),
        (r"(\d+) Maximum at ([\d:]+ \d+-\w+)", 'MaximumRate', 'Timestamp'),
        (r"(\d+)\s*Beats in tachycardia \(>=?\d+\s*bpm\),\s*(\d+)% total", 'TachycardiaBeats', 'TachycardiaPercentage'),
        (r"(\d+)\s*Beats in bradycardia \(<=?\d+\s*bpm\),\s*(\d+)% total", 'BradycardiaBeats', 'BradycardiaPercentage')
    ]
    for pattern, main_tag, sub_tag in patterns:
        match = re.search(pattern, text)
        if match:
            if sub_tag:
                heart_rates_data[main_tag] = {'Value': match.group(1), sub_tag: match.group(2)}
            else:
                heart_rates_data[main_tag] = {'Value': match.group(1)}
        else:
            heart_rates_data[main_tag] = {'Value': "Unknown", sub_tag: "Unknown"} if sub_tag else {'Value': "Unknown"}
    return heart_rates_data

def parse_section(section_text, patterns):
    section_data = {}
    for pattern, tags in patterns:
        matches = extract_grouped_matches(pattern, section_text, len(tags))
        for tag_index, tag in enumerate(tags):
            section_data[tag] = matches[tag_index]
    return section_data

def create_json(holter_report):
    combined_data = {
        "Holter Report": holter_report,
    }
    return json.dumps(combined_data, indent=4)

def process_pdf_files(file_dirs, json_dir):
    pdf_files = []
    for file_dir in file_dirs:
        for root, _, files in os.walk(file_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
    
    failed_files = []
    skipped_files = []

    for pdf_path in tqdm(pdf_files, desc="Processing PDF Files"):
        try:
            filename = os.path.basename(pdf_path)
            pdf_doc = fitz.open(pdf_path)
            page = pdf_doc.load_page(0)
            extracted_text = page.get_text()

            # 먼저 hookup_date를 추출하여 파일명 생성
            hookup_date = extract_match(r"Medications:?\n(\d+-\w+-\d+)\nHookup Date:?", extracted_text, "Unknown")
            formatted_hookup_date = parse_date(hookup_date)
            base_name = os.path.splitext(filename)[0]
            hookup_date_for_filename = formatted_hookup_date.replace('-', '')
            new_filename = f"{base_name}_{hookup_date_for_filename}.json"
            json_path = os.path.join(json_dir, new_filename)

            # 파일이 이미 존재하는지 확인
            if os.path.exists(json_path):
                skipped_files.append(filename)
                continue

            # 기존 코드 계속 진행
            patient_info = {
                'PID': extract_match(r"Patient Name.*?\n(.*?)\nID", extracted_text),
                'HookupDate': formatted_hookup_date,
                'HookupTime': extract_match(r"Hookup Date:?\n(\d+:\d+:\d+)\nHookup Time:?", extracted_text, "Unknown"),
                'Duration': extract_match(r"Hookup Time:?\n(\d+:\d+:\d+)\nDuration:?", extracted_text, "Unknown"),
                'Age': extract_match(r"ID.*?\n(\d+)\s*(?:yr)?\s*\nAge", extracted_text),
                'Gender': extract_match(r"Age.*?\n(Male|Female)\s*\nGender", extracted_text),
            }

            general_data = parse_general_section(extracted_text)
            heart_rates_data = parse_heart_rates_section(extracted_text)

            ventriculars_section = extract_match(r"Ventriculars \(V, F, E, I\)\n([\s\S]+?)\nSupraventriculars \(S, J, A\)", extracted_text, "")
            supraventriculars_section = extract_match(r"Supraventriculars \(S, J, A\)\n([\s\S]+?)Interpretation", extracted_text, "")

            ventriculars_patterns = [
                (r"(\d+) Isolated", ['Isolated']),
                (r"(\d+) Couplets", ['Couplets']),
                (r"(\d+) Bigeminal cycles", ['BigeminalCycles']),
                (r"(\d+) Runs totaling (\d+) beats", ['Runs', 'TotalBeats']),
                (r"(\d+) Beats longest run (\d+) bpm ([\d:]+ \d+-\w+)", ['LongestRunBeats', 'LongestRunBPM', 'LongestRunTimestamp']),
                (r"(\d+) Beats fastest run (\d+) bpm ([\d:]+ \d+-\w+)", ['FastestRunBeats', 'FastestRunBPM', 'FastestRunTimestamp'])
            ]

            supraventriculars_patterns = [
                (r"(\d+) Isolated", ['Isolated']),
                (r"(\d+) Couplets", ['Couplets']),
                (r"(\d+) Bigeminal cycles", ['BigeminalCycles']),
                (r"(\d+) Runs totaling (\d+) beats", ['Runs', 'TotalBeats']),
                (r"(\d+) Beats longest run (\d+) bpm ([\d:]+ \d+-\w+)", ['LongestRunBeats', 'LongestRunBPM', 'LongestRunTimestamp']),
                (r"(\d+) Beats fastest run (\d+) bpm ([\d:]+ \d+-\w+)", ['FastestRunBeats', 'FastestRunBPM', 'FastestRunTimestamp'])
            ]

            ventriculars_data = parse_section(ventriculars_section, ventriculars_patterns)
            supraventriculars_data = parse_section(supraventriculars_section, supraventriculars_patterns)

            holter_report = {
                'PatientInfo': patient_info,
                'General': general_data,
                'HeartRates': heart_rates_data,
                'Ventriculars': ventriculars_data,
                'Supraventriculars': supraventriculars_data
            }

            json_content = create_json(holter_report)
            
            with open(json_path, "w") as json_file:
                json_file.write(json_content)

        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            failed_files.append(filename)

    return failed_files, skipped_files

def main():
    base_dirs = [
        r'D:\exx'    # pdf 파일이 존재하는 경로
    ]
    json_dir = r'D:\json'  # json 파일로 저장할 경로

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    print("Starting to process PDF files...")
    failed_files_record, skipped_files_record = process_pdf_files(base_dirs, json_dir)

    if skipped_files_record:
        print("\nSkipped the following existing files:")
        for skipped_file in skipped_files_record:
            print(skipped_file)

    if failed_files_record:
        print("\nFailed to process the following files:")
        for failed_file in failed_files_record:
            print(failed_file)
    else:
        print("\nAll PDF files processed successfully.")

    print(f"\nCompleted processing all files.")
    print(f"Total skipped files: {len(skipped_files_record)}")
    print(f"Total failed files: {len(failed_files_record)}")

if __name__ == "__main__":
    main()