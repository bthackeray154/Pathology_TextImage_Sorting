# Semantic Filter
# Semantic Types to filter on 
target_types = {"T047", "T191", "T046", "T190", "T019", "T033", "T184", "T060", "T059"}

# Filter MRSTY.RRF and get relevant CUIs
with open("YOUR/PATH/TO/2025AA-full/FullInstall/2025AA/META/MRSTY.RRF", "r", encoding="utf-8") as fin, \
     open("YOUR/PATH/TO/2025AA-full/FullInstall/2025AA/META/filtered_cuis.txt", "w", encoding="utf-8") as fout:
    for line in fin:
        cols = line.strip().split("|")
        cui, sty = cols[0], cols[1]
        if sty in target_types:
            fout.write(f"{cui}\n")

# Place filtered CUIs into a set
with open("YOUR/PATH/TO/2025AA-full/FullInstall/2025AA/META/filtered_cuis.txt", "r", encoding="utf-8") as f:
    valid_cuis = set(line.strip() for line in f)

# Filter MRCONSO.RRF by CUIs and make new file
with open("YOUR/PATH/TO/2025AA-full/FullInstall/2025AA/META/MRCONSO.RRF", "r", encoding="utf-8") as fin, \
     open("YOUR/PATH/TO/2025AA-full/FullInstall/2025AA/META/MRCONSO_filtered.RRF", "w", encoding="utf-8") as fout:
    for line in fin:
        cols = line.strip().split("|")
        if cols[0] in valid_cuis:
            fout.write(line)