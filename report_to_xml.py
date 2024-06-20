import os
import re
import wfdb
import pandas as pd
import fitz  # PyMuPDF
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
from tqdm import tqdm

def process_pdf_files(file_dir, xml_dir):
    pdf_files = [f for f in os.listdir(file_dir) if f.endswith('.pdf')]
    failed_files = []

    for filename in tqdm(pdf_files, desc="Processing PDF Files"):
        try:
            pdf_path = os.path.join(file_dir, filename)
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
            ventriculars_xml = ET.SubElement(root, "Ventriculars")
            for pattern, tags in ventriculars_patterns:
                match = re.search(pattern, ventriculars_section)
                if match:
                    for tag_index, tag in enumerate(tags):
                        if isinstance(tag, tuple):
                            parent_tag = ET.SubElement(ventriculars_xml, tag[0])
                            ET.SubElement(parent_tag, tag[1]).text = match.group(tag_index + 1)
                        else:
                            ET.SubElement(ventriculars_xml, tag).text = match.group(tag_index + 1)

            # Supraventriculars section to add xml
            supraventriculars_xml = ET.SubElement(root, "Supraventriculars")
            for pattern, tags in supraventriculars_patterns:
                match = re.search(pattern, supraventriculars_section)
                if match:
                    for tag_index, tag in enumerate(tags):
                        if isinstance(tag, tuple):
                            parent_tag = ET.SubElement(supraventriculars_xml, tag[0])
                            ET.SubElement(parent_tag, tag[1]).text = match.group(tag_index + 1)
                        else:
                            ET.SubElement(supraventriculars_xml, tag).text = match.group(tag_index + 1)

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

def add_record_data_to_xml(file_dir, xml_dir):
    record_files = [f for f in os.listdir(file_dir) if f.endswith('.hea')]
    failed_files = []

    for record_file in tqdm(record_files, desc="Adding Record Data to XML"):
        try:
            record_path = os.path.join(file_dir, record_file[:-4])  # Remove .hea extension
            record = wfdb.rdrecord(record_path)
            df = pd.DataFrame(record.p_signal, columns=record.sig_name)
            df_transposed = df.T

            # Prepare XML elements
            data_element = ET.Element('data')
            for channel, values in enumerate(df_transposed.values, start=1):
                signal_data = ','.join(map(str, values))
                wave_form_data = ET.SubElement(data_element, 'WaveformData', lead=str(channel))
                wave_form_data.text = signal_data

            # Convert to string and add newline for formatting
            xml_string = ET.tostring(data_element, 'utf-8')
            pretty_xml_str = parseString(xml_string).toprettyxml(indent="  ")

            # Adjust formatting to add newline after <data> and before each <WaveformData>
            pretty_xml_str = pretty_xml_str.replace('><WaveformData', '>\n<WaveformData')
            pretty_xml_str = pretty_xml_str.replace('</WaveformData><', '</WaveformData>\n<')

            xml_filename = os.path.splitext(record_file)[0] + '.xml'
            xml_file_path = os.path.join(xml_dir, xml_filename)

            if os.path.exists(xml_file_path):
                # Load existing XML and append new data
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Parse the newly created XML string and append it
                new_data_element = ET.fromstring(pretty_xml_str)
                root.append(new_data_element)

                # Save back to file
                tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
                print(f"Added record data to {xml_file_path}")
            else:
                print(f"Warning: {xml_file_path} does not exist.")
        except Exception as e:
            print(f"Failed to add record data for {record_file}: {e}")
            failed_files.append(record_file)

    return failed_files


def main():
    base_dir = 'Z:\\Holter\\extract\\child_cd' # 기본 디렉토리
    #base_dir = 'C:\\Users\\SNUH\\Desktop\\export' 
    xml_dir = 'E:\\Holter_xml'

    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    print("Starting to process PDF files...")
    failed_files_pdf = process_pdf_files(base_dir, xml_dir)

    if failed_files_pdf:
        print("\nFailed to process the following PDF files:")
        for failed_file in failed_files_pdf:
            print(failed_file)
    else:
        print("\nAll PDF files processed successfully.")

    print("Starting to add record data to XML...")
    failed_files_record = add_record_data_to_xml(base_dir, xml_dir)

    if failed_files_record:
        print("\nFailed to add record data for the following files:")
        for failed_file in failed_files_record:
            print(failed_file)
    else:
        print("\nAll record data added successfully.")

    print("Completed processing all files.")


if __name__ == "__main__":
    main()