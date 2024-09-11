import os
from tqdm import tqdm

def replace_filename_in_hea_files(directory):
    converted_files_count = 0
    
    # Traverse the directory and find .hea files
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.hea'):
            file_path = os.path.join(directory, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                # Modify the line
                base_filename = filename.replace('.hea', '')
                lines[0] = lines[0].replace(lines[0].split()[0], base_filename)
                
                for i in range(1, len(lines)):
                    lines[i] = lines[i].replace(lines[i].split()[0], f"{base_filename}.SIG")
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(lines)
                
                converted_files_count += 1
            
            except Exception as e:
                print(f"Error processing file: {filename}. Error: {e}")
    
    print(f"Total number of converted files: {converted_files_count}")

directory_path = r'C:\Holter_sig'
replace_filename_in_hea_files(directory_path)
