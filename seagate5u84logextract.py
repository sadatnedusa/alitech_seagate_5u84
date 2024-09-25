# ----------------------------
# Problem Statement:
#   The Seagate “store_2022_07_18__15_45_31.logs” log is huge in size
#   It contains approx 20 lakhs lines
#
# Use case:
#   In general, notepad++, cat, grep, awk etc used to extract data.
#   It is time consuming and mundane task
#
# Variables:
#   log_file --> Provide path of Seagate log file --> store_2022_07_18__15_45_31.logs
#   keyword_file --> seagate_5u84_keywords.yaml
#   seagate_5u84_keywords.yaml contents sample shown below
#
#       - start: "# show enclosures"
#         end: "Success: Command"
#       - start: "# show advanced-settings"
#         end: "Success: Command"
#       - start: "# show redundancy-mode"
#         end: "Success: Command"
#   
# Output:
#
#
#       # show redundancy-mode
#       System Redundancy
#       -----------------
#       Controller Redundancy Mode: Active-Active ULP
#       Controller Redundancy Status: Redundant
#       Controller A Status: Operational
#       Controller A Serial Number: DHSIFGD-2145651DBB
#       Controller B Status: Operational
#       Controller B Serial Number: DHSIFGD-2145651DE7
#       Other MC Status: Operational
#
#       Success: Command completed successfully. (2022-07-18 15:46:28)
#
#
# ------------------
# How to run program
# ------------------
#  ❯ python3 seagate_log_extract_v13.py
#
#
# ---------------------------
# Author : Syed Sadat Ali
# Dated  : 12-Sept-2022
# Ver    : v.01
# Dated  : 06-Mar-2023
# Ver    : v.02
# Dated  : 23-May-2023
# Ver    : v.03
# Dated  : 01-Nov-2023
# Ver    : v.06
# ---------------------------
import yaml
import os
from datetime import datetime

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%d-%m-%Y-%H-%M-%S")

def validate_log_file(log_file):
    if not os.path.exists(log_file):
        print("Error: The log file does not exist.")
        return False
    if os.path.getsize(log_file) == 0:
        print("Error: The log file is empty.")
        return False
    return True

def validate_keyword_file(keyword_file):
    try:
        with open(keyword_file, 'r') as file:
            keyword_sets = yaml.safe_load(file)
            if not isinstance(keyword_sets, list):
                print("Error: The keyword file does not contain a valid YAML list.")
                return False
            return True
    except Exception as e:
        print(f"Error: An error occurred while parsing the keyword file: {str(e)}")
        return False

def validate_number_sequence(log_data):
    found_numbers = set()
    in_show_disks_section = False

    for line in log_data:
        if "# show disks" in line:
            in_show_disks_section = True
        elif in_show_disks_section:
            tokens = line.split()
            if len(tokens) >= 1:
                number = tokens[0]
                if number.startswith("0.") and is_valid_number(number):
                    found_numbers.add(number)

    missing_numbers = find_missing_numbers(found_numbers)
    return missing_numbers

def is_valid_number(number):
    try:
        num = float(number)
        return 0.0 <= num <= 0.83
    except ValueError:
        return False

def find_missing_numbers(found_numbers):
    all_numbers = set(f"0.{i:01}" for i in range(84))
    missing_numbers = sorted(all_numbers - found_numbers)
    return missing_numbers

def extract_data_from_log(log_file, keyword_sets, output_folder):
    if not validate_log_file(log_file):
        return
    if not validate_keyword_file('seagate_5u84_keywords.yaml'):
        return

    current_datetime = get_current_datetime()
    output_file = os.path.join(output_folder, f"extracted_data_{current_datetime}.txt")

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
        log_data = file.readlines()

    with open(output_file, 'a', encoding='utf-8', errors='ignore') as output:
        for keyword_set in keyword_sets:
            start_keyword, end_keyword = keyword_set['start'], keyword_set['end']
            extracting = False
            extracted_data = []

            for line in log_data:
                if start_keyword in line:
                    extracting = True
                    #extracted_data.append(line)
                    #extracted_data.append(">>Begin>>\n\n")

                if extracting:
                    extracted_data.append(line)

                if end_keyword in line:
                    if extracting:
                        extracting = False
                        output.writelines(extracted_data)
                        #output.writelines("\n\n<<End<<\n")
                        # Log portion seperator
                        #output.write('\n--- Separator ---\n\n')
                        extracted_data = []

            if start_keyword == "# show disks":
                missing_numbers = validate_number_sequence(extracted_data)
                if missing_numbers:
                    output.write(f"Missing numbers in the section starting with {start_keyword}:\n")
                    output.write(', '.join(missing_numbers))
                    output.write('\n')

if __name__ == "__main__":
    #log_file = '/Users/syed.ali/Documents/scripts/seagate_debug/store_2022_07_18__15_45_31.logs'  # Replace with the path to your log file
    log_file = '.\store_2024_01_22__10_35_30.logs'
    if validate_log_file(log_file):
        with open('seagate_5u84_keywords.yaml', 'r') as keyword_file:
            keyword_sets = yaml.safe_load(keyword_file)
            if validate_keyword_file(keyword_file.name):
                # output folder variable 
                output_folder = 'output'  

                os.makedirs(output_folder, exist_ok=True)
                extract_data_from_log(log_file, keyword_sets, output_folder)
