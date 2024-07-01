import os
import wfdb
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from tqdm import tqdm

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
                # Load existing XML and check if <data> already exists
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                if root.find('data') is not None:
                    print(f"Skipping {xml_file_path} as it already contains <data>")
                    continue

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
    xml_dir = 'E:\\Holter_xml\\new'

    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

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
