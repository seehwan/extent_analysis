# extract_extents_by_dir.py

import os
import sys
import subprocess
import re
import hashlib

BLOCK_SIZE = 4096

def debug(msg):
    with open("debug_extract.log", "a") as log:
        log.write(f"{msg}\n")

def extract_extents(file_path):
    if os.path.islink(file_path):
        return []
    try:
        subprocess.check_output(['df', file_path], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return []
    try:
        result = subprocess.check_output(['filefrag', '-v', file_path], stderr=subprocess.DEVNULL).decode()
        extents = []
        for line in result.splitlines():
            line = line.strip()
            if re.match(r'^\d+:', line):
                parts = line.split(":")
                if len(parts) >= 4:
                    try:
                        length_str = parts[3].strip()
                        length = int(length_str)
                        extents.append(length)
                    except ValueError:
                        continue
        return extents
    except Exception as e:
        debug(f"Error processing {file_path}: {e}")
        return []

if len(sys.argv) != 3:
    print("Usage: python3 extract_extents_by_dir.py <directory> <output_csv>")
    sys.exit(1)

target_dir = sys.argv[1]
output_csv = sys.argv[2]

with open(output_csv, "w") as out:
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            path = os.path.join(root, name)
            extents = extract_extents(path)
            for i, blocks in enumerate(extents):
                out.write(f"{path},{i},{blocks}\n")
