import os
import csv
import glob
import matplotlib.pyplot as plt

input_dir = "extent_output_by_device"
all_blocks = []
device_blocks = {}

# CSV 파일 순회
for fpath in glob.glob(f"{input_dir}/*.csv"):
    device = os.path.basename(fpath).replace(".csv", "")
    blocks = []

    with open(fpath, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                block_count = int(row[-1])
                blocks.append(block_count)
                all_blocks.append(block_count)
            except:
                continue

    device_blocks[device] = blocks

# 🎯 1. 전체 장치 통합 히스토그램
plt.figure(figsize=(10, 4))
plt.hist(all_blocks, bins=100, log=True)
plt.title("Extent Size Distribution (All Devices)")
plt.xlabel("Blocks per Extent")
plt.ylabel("Frequency (log scale)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🎯 2. 장치별 히스토그램 (최대 6개까지 나눠서 보여줌)
from math import ceil

device_list = list(device_blocks.keys())
max_per_row = 3
rows = ceil(len(device_list) / max_per_row)
plt.figure(figsize=(5 * max_per_row, 4 * rows))

for idx, device in enumerate(device_list):
    plt.subplot(rows, max_per_row, idx + 1)
    plt.hist(device_blocks[device], bins=50, log=True)
    plt.title(device.replace("_dev_", "/dev/"))
    plt.xlabel("Blocks")
    plt.ylabel("Freq")
    plt.grid(True)

plt.tight_layout()
plt.suptitle("Extent Size Distribution by Device", fontsize=16, y=1.02)
plt.show()
