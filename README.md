# Seagate 5U84 Storage Debug Log Analyzer

This Python script is designed to extract meaningful diagnostic data from Seagate 5U84 storage system debug log files. Specifically, it automates the parsing and analysis of the large log files generated from the Seagate Debug ZIP files, streamlining the troubleshooting and data extraction process.

## Overview

When troubleshooting Seagate 5U84 storage systems, a significant amount of diagnostic data is contained within compressed debug log files. These ZIP files are typically around 30 MB, but after decompression, the primary log file (`store_yyyy_mm_dd__hh_mm_ss.log`) can be upwards of 130 to 150 MB, containing approximately 2 million lines of information.

Manually parsing through this data can be challenging. This script simplifies the process by allowing users to define search parameters in an external YAML configuration file, which the script then uses to extract relevant information from the logs. By externalizing the search logic, the script provides flexibility and avoids the need for complex regular expressions or manual pattern matching.

### Key Features

- **Efficient Log Parsing**: Processes large log files (2 million+ lines) quickly and accurately.
- **Customizable**: Input parameters, such as start and end keywords for data extraction, are defined in an external YAML file, allowing easy customization without modifying the core script.
- **Targeted Extraction**: Filters the log data based on the defined keywords, ensuring only relevant information is extracted for analysis.

### How It Works

1. **Input**: 
   - Uncompress the Seagate Debug ZIP file before using the script. The key log file to be analyzed is typically named in the format `store_yyyy_mm_dd__hh_mm_ss.log`.
   - Define your search keywords and extraction rules in a YAML configuration file.

2. **Execution**:
   - The script reads the log file and extracts data based on the keywords defined in the YAML file. It uses start and end patterns for data extraction, ensuring that no complex regular expressions are needed.

3. **Output**: 
   - Extracted data is organized and presented in a readable format for further analysis or reporting.


---

# Seagate 5U84 Storage Log Analyzer

### Problem Statement:
The Seagate log file (`store_2022_07_18__15_45_31.logs`) is significantly large, containing around 200,000 entries. Manually extracting useful data from these logs using tools like Notepad++, TextPad, `cat`, `grep`, or `awk` can be extremely time-consuming and tedious.

### Use Case:
This Python script automates the process of extracting key information from the log files, eliminating the need for manual filtering and saving significant time. Instead of relying on standard text manipulation tools, this script uses defined start and end keywords for efficient data extraction.

### Variables:
- **log_file**: Path to the Seagate log file (e.g., `store_2022_07_18__15_45_31.logs`).
- **keyword_file**: Path to the YAML configuration file (e.g., `seagate_5u84_keywords.yaml`).

#### Sample Content of `seagate_5u84_keywords.yaml`:
```yaml
- start: "# show enclosures"
  end: "Success: Command"
- start: "# show advanced-settings"
  end: "Success: Command"
- start: "# show redundancy-mode"
  end: "Success: Command"
```

### Expected Output:
Upon running the script, the following format will be used to display extracted log entries between the start and end keywords:

```
>>Begin>>

# show redundancy-mode
System Redundancy
-----------------
Controller Redundancy Mode: Active-Active ULP
Controller Redundancy Status: Redundant
Controller A Status: Operational
Controller A Serial Number: DHSIFGD-2145651DBB
Controller B Status: Operational
Controller B Serial Number: DHSIFGD-2145651DE7
Other MC Status: Operational

Success: Command completed successfully. (2022-07-18 15:46:28)

<<End<<
```

### How to Run the Program:
```bash
python3 seagate_log_extract_v13.py
```

### Version History:
- **Author**: Syed Sadat Ali
- **Version 1.0**: 12-Sept-2022
- **Version 2.0**: 06-Mar-2023
- **Version 3.0**: 23-May-2023
- **Version 6.0**: 01-Nov-2023

---

### References

For more detailed information on Seagate Debug Log formats and diagnostic information, please refer to the official Seagate guide:  
[Seagate G250 Storage Management Guide - Page 136](https://www.seagate.com/files/dothill-content/support/documentation/83-00007047-10-01_G250_SMG.pdf)
