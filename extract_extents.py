import sys
import subprocess
import re
import os

BLOCK_SIZE = 4096
file_path = sys.argv[1]

# 분석 제외: df 실패하는 파일
try:
    subprocess.check_output(['df', file_path], stderr=subprocess.DEVNULL)
except:
    sys.exit(0)

try:
    result = subprocess.check_output(['filefrag', '-v', file_path], stderr=subprocess.DEVNULL).decode()
    extents = []
    for line in result.splitlines():
        match = re.search(r'^\s*\d+\s+\d+\s+\d+\s+\d*\s+(\d+)', line)
        if match:
            length = int(match.group(1))
            extents.append(length * BLOCK_SIZE)

    if extents:
        tag = file_path.replace("/", "_").strip("_")
        output_dir = "extent_output"
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/{tag}.csv", "w") as f:
            for i, size in enumerate(extents):
                f.write(f"{file_path},{i},{size}\n")

except:
    pass  # 무시
