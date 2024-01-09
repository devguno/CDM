import os
import xml.etree.ElementTree as ET
import csv

def parse_xml_and_save_to_csv_v5(root_directory, output_directory):
    fieldnames = ['file_path', 'hospital_id', 'lastname', 'firstname', 'date', 'datetime']
    output_file_path = os.path.join(output_directory, 'parsed_data.csv')

    with open(output_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for dirpath, dirs, files in os.walk(root_directory):
            for file in files:
                if file.endswith('.xml'):
                    file_path = os.path.join(dirpath, file)
                    with open(file_path, 'r', encoding='utf-8') as xml_file:
                        tree = ET.parse(xml_file)
                        xml_root = tree.getroot()

                        # 실제 데이터를 포함하는 <client> 태그만 선택적으로 찾기
                        for client in xml_root.findall('.//client[personnumber]'):
                            createdate = client.find('.//createdate').text if client.find('.//createdate') is not None else ''
                            personnumber = client.find('.//personnumber').text if client.find('.//personnumber') is not None else ''
                            firstname = client.find('.//firstname').text.strip() if client.find('.//firstname') is not None else ''
                            lastname = client.find('.//lastname').text if client.find('.//lastname') is not None else ''

                            date = createdate.split(' ')[0].replace('/', '-') if createdate else ''
                            datetime = createdate.replace('/', '-') if createdate else ''
                            hospital_id = personnumber.zfill(8) if personnumber else ''

                            writer.writerow({
                                'file_path': file_path, 
                                'hospital_id': hospital_id, 
                                'lastname': lastname, 
                                'firstname': firstname, 
                                'date': date, 
                                'datetime': datetime
                            })

    return output_file_path




# 파일 경로
root_directory = r'C:\Users\SNUH\Desktop\abr\abr_xml\어린이병원3F'
output_directory = r'C:\Users\SNUH\Desktop\abr\result'

# 함수 호출 및 결과 파일 경로 출력
parsed_file_path = parse_xml_and_save_to_csv_v5(root_directory, output_directory)
parsed_file_path
