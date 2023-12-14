import os
import csv
import xml.etree.ElementTree as ET

# Directory containing the XML files
#directory = 'Z:/child_tmt/Child TMT Device #1/2018.7-2019.2'
directory = r'C:\Users\SNUH\Desktop\test'

# Function to parse an XML file and extract the required data
def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extracting ObservationDateTime
        observation_date_time = root.find('ObservationDateTime')
        date_str = '-'.join([observation_date_time.find(tag).text.zfill(2) for tag in ['Year', 'Month', 'Day']])
        time_str = ':'.join([observation_date_time.find(tag).text.zfill(2) for tag in ['Hour', 'Minute', 'Second']])
        datetime_str = f"{date_str} {time_str}"

        # Extracting PID, FamilyName, and GivenName
        patient_info = root.find('PatientInfo')
        pid = patient_info.find('PID').text
        family_name = patient_info.find('Name/FamilyName').text
        given_name = patient_info.find('Name/GivenName').text

        return file_path, pid, family_name, given_name, date_str, datetime_str
    except ET.ParseError:
        return None

# CSV file to store the extracted data
csv_file_path = os.path.join(directory, 'extracted_data.csv')

# Extracting data from all XML files in the directory and writing to the CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['FilePath', 'PID', 'FamilyName', 'GivenName', 'Date', 'DateTime'])

    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            data = parse_xml(file_path)
            if data:
                writer.writerow(data)
