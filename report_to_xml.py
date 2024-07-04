import os
import re
import fitz  # PyMuPDF
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from tqdm import tqdm

def process_pdf_files(file_dirs, xml_dir):
    pdf_files = []
    for file_dir in file_dirs:
        for root, _, files in os.walk(file_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
    
    failed_files = []

    for pdf_path in tqdm(pdf_files, desc="Processing PDF Files"):
        try:
            filename = os.path.basename(pdf_path)
            pdf_doc = fitz.open(pdf_path)
            print(f"Processing file: {filename}, Total Pages: {pdf_doc.page_count}")

            page = pdf_doc.load_page(0)
            extracted_text = page.get_text()

            # XML root element creation
            root = Element('HolterReport')

            # Parsing the text
            try:
                patient_id = re.findall(r"Patient Name:?\n(\d+)\nID:?", extracted_text)[0]
            except IndexError:
                patient_id = filename.split('_')[-1].replace('.pdf', '')

            try:
                hookup_date = re.findall(r"Medications:?\n(\d+-\w+-\d+)\nHookup Date:?", extracted_text)[0]
            except IndexError:
                hookup_date = "Unknown"

            try:
                hookup_time = re.findall(r"Hookup Date:?\n(\d+:\d+:\d+)\nHookup Time:?", extracted_text)[0]
            except IndexError:
                hookup_time = "Unknown"

            try:
                duration = re.findall(r"Hookup Time:?\n(\d+:\d+:\d+)\nDuration:?", extracted_text)[0]
            except IndexError:
                duration = "Unknown"
            
            try:
                age = re.findall(r"(\d+)\s*yr\s*Age:", extracted_text)[0]
            except IndexError:
                age = "Unknown"

            try:
                gender = re.findall(r"(Male|Female)\s*Gender:", extracted_text)[0]
            except IndexError:
                gender = "Unknown"


            # Parsing General section
            general_section = re.search(r"General\n(.+?)Heart Rates", extracted_text, re.DOTALL)
            if general_section:
                general_section = general_section.group(1)
                qrs_complexes = re.search(r"(\d+) QRS complexes", general_section)
                qrs_complexes = qrs_complexes.group(1) if qrs_complexes else "Unknown"

                ventricular_beats = re.search(r"(\d+) Ventricular beats", general_section)
                ventricular_beats = ventricular_beats.group(1) if ventricular_beats else "Unknown"

                supraventricular_beats = re.search(r"(\d+) Supraventricular beats", general_section)
                supraventricular_beats = supraventricular_beats.group(1) if supraventricular_beats else "Unknown"

                noise_percentage_match = re.search(r"(<\s*\d+|\d+) % of total time classified as noise", general_section)
                noise_percentage = noise_percentage_match.group(1) if noise_percentage_match else "0"
            else:
                qrs_complexes = ventricular_beats = supraventricular_beats = noise_percentage = "Unknown"

            # Constructing the XML
            patient_info = SubElement(root, 'PatientInfo')
            SubElement(patient_info, 'PID').text = patient_id
            SubElement(patient_info, 'HookupDate').text = hookup_date
            SubElement(patient_info, 'HookupTime').text = hookup_time
            SubElement(patient_info, 'Duration').text = duration
            SubElement(patient_info, 'Age').text = age
            SubElement(patient_info, 'Gender').text = gender

            # General
            general = SubElement(root, 'General')
            SubElement(general, 'QRScomplexes').text = qrs_complexes
            SubElement(general, 'VentricularBeats').text = ventricular_beats
            SubElement(general, 'SupraventricularBeats').text = supraventricular_beats
            SubElement(general, 'NoisePercentage').text = noise_percentage

            # Heart Rates section
            heart_rates = SubElement(root, 'HeartRates')
            patterns_hr = [
                (r"(\d+) Minimum at ([\d:]+ \d+-\w+)", 'MinimumRate', 'Timestamp'),
                (r"(\d+) Average", 'AverageRate', None),
                (r"(\d+) Maximum at ([\d:]+ \d+-\w+)", 'MaximumRate', 'Timestamp'),
                (r"(\d+) Beats in tachycardia \(>=\d+ bpm\), (\d+)% total", 'TachycardiaBeats', 'TachycardiaPercentage'),
                (r"(\d+) Beats in bradycardia \(<=\d+ bpm\), (\d+)% total", 'BradycardiaBeats', 'BradycardiaPercentage'),
            ]

            for pattern, main_tag, sub_tag in patterns_hr:
                match = re.search(pattern, extracted_text)
                if match:
                    if sub_tag:
                        element = SubElement(heart_rates, main_tag)
                        SubElement(element, sub_tag).text = match.group(2)
                        element.text = match.group(1)
                    else:
                        SubElement(heart_rates, main_tag).text = match.group(1)

            max_rr_match = re.search(r"(\d+\.\d+) Seconds Max R-R at ([\d:]+ \d+-\w+)", extracted_text)
            if max_rr_match:
                max_rr = SubElement(heart_rates, 'SecondsMaxRR')
                SubElement(max_rr, 'Seconds').text = max_rr_match.group(1)
                SubElement(max_rr, 'Timestamp').text = max_rr_match.group(2)

            # Ventriculars section extraction
            ventriculars_match = re.search(r"Ventriculars \(V, F, E, I\)\n([\s\S]+?)\nSupraventriculars \(S, J, A\)", extracted_text)
            ventriculars_section = ventriculars_match.group(1) if ventriculars_match else ""

            # Supraventriculars section extraction
            supraventriculars_match = re.search(r"Supraventriculars \(S, J, A\)\n([\s\S]+?)Interpretation", extracted_text)
            supraventriculars_section = supraventriculars_match.group(1) if supraventriculars_match else ""

            # Regex patterns for Ventriculars and Supraventriculars
            ventriculars_patterns = [
                (r"(\d+) Isolated", ['Isolated']),
                (r"(\d+) Couplets", ['Couplets']),
                (r"(\d+) Bigeminal cycles", ['BigeminalCycles']),
                (r"(\d+) Runs totaling (\d+) beats", ['Runs', ('RunsDetails', 'TotalBeats')]),
                (r"(\d+) Beats longest run (\d+) bpm ([\d:]+ \d+-\w+)", [('LongestRun', 'Beats'), ('LongestRun', 'BPM'), ('LongestRun', 'Timestamp')]),
                (r"(\d+) Beats fastest run (\d+) bpm ([\d:]+ \d+-\w+)", [('FastestRun', 'Beats'), ('FastestRun', 'BPM'), ('FastestRun', 'Timestamp')])
            ]

            supraventriculars_patterns = [
                (r"(\d+) Isolated", ['Isolated']),
                (r"(\d+) Couplets", ['Couplets']),
                (r"(\d+) Bigeminal cycles", ['BigeminalCycles']),
                (r"(\d+) Runs totaling (\d+) beats", ['Runs', ('RunsDetails', 'TotalBeats')]),
                (r"(\d+) Beats longest run (\d+) bpm ([\d:]+ \d+-\w+)", [('LongestRun', 'Beats'), ('LongestRun', 'BPM'), ('LongestRun', 'Timestamp')]),
                (r"(\d+) Beats fastest run (\d+) bpm ([\d:]+ \d+-\w+)", [('FastestRun', 'Beats'), ('FastestRun', 'BPM'), ('FastestRun', 'Timestamp')])
            ]

            # Ventriculars section to add xml
            ventriculars_xml = SubElement(root, "Ventriculars")
            for pattern, tags in ventriculars_patterns:
                match = re.search(pattern, ventriculars_section)
                if match:
                    for tag_index, tag in enumerate(tags):
                        if isinstance(tag, tuple):
                            parent_tag = SubElement(ventriculars_xml, tag[0])
                            SubElement(parent_tag, tag[1]).text = match.group(tag_index + 1)
                        else:
                            SubElement(ventriculars_xml, tag).text = match.group(tag_index + 1)

            # Supraventriculars section to add xml
            supraventriculars_xml = SubElement(root, "Supraventriculars")
            for pattern, tags in supraventriculars_patterns:
                match = re.search(pattern, supraventriculars_section)
                if match:
                    for tag_index, tag in enumerate(tags):
                        if isinstance(tag, tuple):
                            parent_tag = SubElement(supraventriculars_xml, tag[0])
                            SubElement(parent_tag, tag[1]).text = match.group(tag_index + 1)
                        else:
                            SubElement(supraventriculars_xml, tag).text = match.group(tag_index + 1)

            xml_str = tostring(root, 'utf-8')
            parsed_str = parseString(xml_str)
            pretty_xml_str = parsed_str.toprettyxml(indent="   ")

            xml_filename = os.path.splitext(filename)[0] + '.xml'
            xml_file_path = os.path.join(xml_dir, xml_filename)

            with open(xml_file_path, "w") as xml_file:
                xml_file.write(pretty_xml_str)

            print(f"Processed {filename}, Saved XML file: {xml_file_path}")

        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            failed_files.append(filename)

    return failed_files

def main():
    base_dirs = [
        'Z:\\Holter\\extract\\Holter_gangnam_extract',
        'Z:\\Holter\\extract\\Holter_main_extract'
    ]  # 기본 디렉토리들
    xml_dir = 'Z:\\Holter\\xml\\adult'

    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    print("Starting to process PDF files...")
    failed_files_record = process_pdf_files(base_dirs, xml_dir)

    if failed_files_record:
        print("\nFailed to process the following files:")
        for failed_file in failed_files_record:
            print(failed_file)
    else:
        print("\nAll PDF files processed successfully.")

    print("Completed processing all files.")

if __name__ == "__main__":
    main()
