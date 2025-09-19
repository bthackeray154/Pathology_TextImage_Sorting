# Quality Sort

import os
import shutil
import re
import csv
from quickumls import QuickUMLS
from tqdm import tqdm

quickumls_fp = r"quickumls_data"

# Build the medical term matcher
matcher = QuickUMLS(
    quickumls_fp,
    threshold=0.99,
)

# Folder paths
folder_path = "INSERT folder to path report text from ocr"
flagged_rep_folder = "INSERT new folder path for flagged reports"
ready_rep_folder = "INSERT new folder path for reports above threshold"

# Create output folders if not already created
os.makedirs(flagged_rep_folder, exist_ok=True)
os.makedirs(ready_rep_folder, exist_ok=True)

# Extracts the A# from a file name
def extract_anum(filename):
    match = re.search(r'(A\d+)', filename)
    return match.group(1) if match else None

# Make new csv with file name and Terms/KB score headers
csv_path = "/home/thack053/PathSort.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["A# File", "Path Score", "Sort Group"])

# Process each text file (Using tqdm for progress bar)
for filename in tqdm(os.listdir(folder_path)):
    termCount = 0
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)   
        file_size = os.path.getsize(file_path) / 1024
        
        with open(file_path, "r", encoding="utf-8") as file:
            full_text = file.read()

        matches = matcher.match(full_text)
        for match in matches:
                termCount += 1
        if (termCount / file_size) < 5.56:
            flagged_file = os.path.join(flagged_rep_folder, filename)
            shutil.copy(file_path, flagged_file)
            with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([extract_anum(filename), (termCount / file_size), "Flagged"])
        else:
            ready_file = os.path.join(ready_rep_folder, filename)
            shutil.copy(file_path, ready_file)
            with open(csv_path, "a  ", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([extract_anum(filename), (termCount / file_size), "Approved"])



print(f"Sorting data exported to: {csv_path}")