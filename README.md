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

### Example Usage

```bash
python seagate_log_analyzer.py --logfile path_to_store_yyyy_mm_dd__hh_mm_ss.log --config keywords.yaml
```

- `logfile`: Path to the decompressed log file.
- `config`: Path to the YAML configuration file where the extraction rules are defined.

### References

For more detailed information on Seagate Debug Log formats and diagnostic information, please refer to the official Seagate guide:  
[Seagate G250 Storage Management Guide - Page 136](https://www.seagate.com/files/dothill-content/support/documentation/83-00007047-10-01_G250_SMG.pdf)
