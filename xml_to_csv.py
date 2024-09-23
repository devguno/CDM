import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from tqdm import tqdm

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = {}
    for elem in root.iter():
        # Skip 'HolterReport' and 'PatientInfo' tags
        if elem.tag in ['HolterReport', 'PatientInfo']:
            continue
        if elem.text:
            text = elem.text.strip()
            # Replace 'Unknown' with an empty string
            if text == 'Unknown':
                text = ''
            # Convert date format
            try:
                text = datetime.strptime(text, '%d-%b-%Y').strftime('%Y-%m-%d')
            except ValueError:
                pass
            data[elem.tag] = text
    
    return data

def extract_xml_data(directory):
    all_data = []
    xml_files = glob.glob(os.path.join(directory, '*.xml'))
    for file_path in tqdm(xml_files, desc=f"Processing files in {directory}"):
        data = parse_xml(file_path)
        data['filename'] = os.path.basename(file_path)  # Add filename to data
        all_data.append(data)
    return all_data

def main():
    xml_directory = '/workspace/nas1/Holter_new/Holter_xml'

    xml_data = extract_xml_data(xml_directory)

    # Create a DataFrame
    df = pd.DataFrame(xml_data)

    # Rename 'PID' to 'cdm_id'
    df = df.rename(columns={'PID': 'person_id'})

    # Reorder columns to place 'filename' as the second column
    cols = list(df.columns)
    cols.insert(1, cols.pop(cols.index('filename')))
    df = df[cols]

    # Count duplicates before removing
    initial_count = df.duplicated(subset=['person_id', 'HookupDate']).sum()
    print(f'Number of duplicate rows before removing: {initial_count}')

    # Remove duplicates based on 'cdm_id' and 'HookupDate'
    df = df.drop_duplicates(subset=['person_id', 'HookupDate'], keep='last')

    # Count duplicates after removing to confirm
    final_count = df.duplicated(subset=['person_id', 'HookupDate']).sum()
    print(f'Number of duplicate rows after removing: {final_count}')

    # Save DataFrame to CSV
    df.to_csv('/workspace/guno/holter_data.csv', index=False)

if __name__ == '__main__':
    main()
