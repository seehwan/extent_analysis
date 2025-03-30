import sys
import subprocess
import re
import os
import hashlib

BLOCK_SIZE = 4096
file_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv) > 2 else "extent_output"

def debug(msg):
    with open("debug_extract.log", "a") as log:
        log.write(f"{file_path} :: {msg}\n")

# Step 0: Skip symbolic links
if os.path.islink(file_path):
    debug("⏭️ symbolic link skipped")
    sys.exit(0)

# Step 1: Skip files that df can't resolve
try:
    subprocess.check_output(['df', file_path], stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    debug("❌ df failed")
    sys.exit(0)

# Step 2: Run filefrag and parse extent sizes (newer colon format)
try:
    result = subprocess.check_output(['filefrag', '-v', file_path], stderr=subprocess.DEVNULL).decode()
    extents = []

    for line in result.splitlines():
        line = line.strip()
        if re.match(r'^\d+:', line):  # 줄이 "0:", "1:" 등으로 시작하는지 확인
            parts = line.split(":")
            if len(parts) >= 4:
                try:
                    length_str = parts[3].strip()
                    length = int(length_str)
                    extents.append(length)
                except ValueError:
                    debug(f"⚠️ Failed to parse length: {parts}")

    if not extents:
        debug("⚠️ no extents")
    else:
        tag_hash = hashlib.md5(file_path.encode()).hexdigest()
        os.makedirs(out_dir, exist_ok=True)
        with open(f"{out_dir}/{tag_hash}.csv", "w") as f:
            for i, blocks in enumerate(extents):
                f.write(f"{file_path},{i},{blocks}\n")
        debug(f"✅ wrote {len(extents)} extents")

except Exception as e:
    debug(f"💥 error: {e} (file: {file_path})")
