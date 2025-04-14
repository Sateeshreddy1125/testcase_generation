#!/usr/bin/env python3
import os
import re
import json
import sys

def extract_testcase_info(folder_name):
    """
    Given a test case folder name like:
    "370-TC03-03-API-Sanity_20250206104046"
    extract the test case base name and timestamp.
    """
    parts = folder_name.split("_")
    if len(parts) == 2:
        testcase_name = parts[0]
        timestamp = parts[1]
    else:
        testcase_name = folder_name
        timestamp = "unknown"
    return testcase_name, timestamp

def parse_verdict_file(verdict_path):
    """
    Parses a verdict file with lines like:
    
      Cell0 DL Throughput = 1220.43 Mbps [Range:750.0-950.0] -  Fail  
      Cell0 UL Throughput = 27.52 Mbps [Range:0.0-40.0] - Pass  
      INVITE: 64 [Range: 44.0-84.0] -- Pass  
      ACK: 64 [Range: 44.0-84.0] -- Pass

    Returns a dictionary where each key is a parameter name and
    its value includes "value", "min", "max", and "status".
    """
    verdict_data = {}
    # Regular expression to extract parameter details
    pattern = re.compile(
        r'(.+?)\s*[:=]\s*([\d\.]+\s*\w*)?\s*\[Range:\s*([\d\.\-]+)\s*-\s*([\d\.\-]+)\]\s*[-]+?\s*(Pass|Fail)', 
        re.IGNORECASE)
    
    with open(verdict_path, "r") as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                parameter, value, min_val, max_val, status = match.groups()
                verdict_data[parameter.strip()] = {
                    "value": value.strip() if value else "N/A",
                    "min": min_val.strip(),
                    "max": max_val.strip(),
                    "status": status.strip()
                }
    return verdict_data

def process_build_folder(build_path):
    """
    Process the main build folder and return a dictionary with:
      - build name
      - test_cases: a dictionary where each key is a test case name and
        its value includes a timestamp and verdict details from the verdict file.
    """
    build_name = os.path.basename(build_path.rstrip(os.sep))
    build_data = {"build": build_name, "test_cases": {}}
    
    # Optionally, process the summary file if needed.
    summary_file = os.path.join(build_path, "summary_buildname.txt")
    if os.path.exists(summary_file):
        with open(summary_file, "r") as sf:
            build_data["summary_info"] = sf.read().strip()

    # Process each test case folder
    for item in os.listdir(build_path):
        item_path = os.path.join(build_path, item)
        # Identify test case folders – in this example, we check they start with "370-"
        if os.path.isdir(item_path) and item.startswith("370-"):
            testcase_name, timestamp = extract_testcase_info(item)
            # Assume verdict file naming: "verdict-<testcase_name>.txt"
            verdict_filename = f"verdict-{testcase_name}.txt"
            verdict_file_path = os.path.join(item_path, verdict_filename)
            if os.path.exists(verdict_file_path):
                verdict_details = parse_verdict_file(verdict_file_path)
            else:
                verdict_details = {}
            build_data["test_cases"][testcase_name] = {
                "timestamp": timestamp,
                "verdict": verdict_details
            }
    return build_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 jsonconverter.py <path_to_build_folder>")
        sys.exit(1)
    
    build_path = sys.argv[1]
    if not os.path.isdir(build_path):
        print(f"Provided path {build_path} is not a directory.")
        sys.exit(1)
    
    data = process_build_folder(build_path)
    # Write the JSON file into the current working directory as jsonfile.json
    output_path = os.path.join(os.getcwd(), "jsonfile.json")
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Successfully created summary JSON at {output_path}")

if __name__ == "__main__":
    main()
