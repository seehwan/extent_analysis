import os
import sys
import subprocess
import re
import hashlib

BLOCK_SIZE = 4096

def debug(msg):
    pass
    # with open("debug_extract.log", "a") as log:
    #     log.write(f"{msg}\n")

def extract_extents(file_path):
    # 1) 심볼릭 링크 건너뛰기
    if os.path.islink(file_path):
        debug(f"symlink: {file_path}")
        return []

    # 2) df 실패 여부
    try:
        subprocess.check_output(['df', file_path], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        debug(f"df failed: {file_path}")
        return []

    # 3) filefrag 실행
    try:
        result = subprocess.check_output(['filefrag', '-v', file_path], stderr=subprocess.DEVNULL).decode()
    except Exception as e:
        debug(f"filefrag error: {file_path} - {e}")
        return []

    # 4) extent 파싱
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
                    debug(f"failed to parse length: {file_path} -> {parts}")
                    continue

    # 5) 결과 반환 + 로깅
    if not extents:
        debug(f"no extents: {file_path}")
    else:
        debug(f"wrote {len(extents)} extents: {file_path}")

    return extents

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
