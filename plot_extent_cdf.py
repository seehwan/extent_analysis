import os
import csv
import glob
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

input_dir = "extent_output_by_device"
all_blocks = []
device_blocks = {}

# Load data
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

# Determine global 99.9 percentile cutoff
cutoff = np.percentile(all_blocks, 99.9)
print(f"📌 99.9th percentile extent size: {cutoff:.2f} blocks")

# CDF plotting helper
def plot_cdf(data, label=None):
    data = np.sort(data)
    y = np.linspace(0, 1, len(data))
    plt.plot(data, y, label=label)

# 🎯 1. Global CDF (cut at 99.9%)
filtered_all = [b for b in all_blocks if b <= cutoff]

plt.figure(figsize=(8, 5))
plot_cdf(filtered_all)
plt.title("CDF of Extent Sizes (All Devices, ≤ 99.9th %tile)")
plt.xlabel("Blocks per Extent")
plt.ylabel("Cumulative Probability")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🎯 2. Per-device CDFs (cut at 99.9%)
device_list = list(device_blocks.keys())
max_per_row = 3
rows = ceil(len(device_list) / max_per_row)
plt.figure(figsize=(5 * max_per_row, 4 * rows))

for idx, device in enumerate(device_list):
    plt.subplot(rows, max_per_row, idx + 1)
    filtered = [b for b in device_blocks[device] if b <= cutoff]
    if filtered:
        plot_cdf(filtered)
    plt.title(device.replace("_dev_", "/dev/"))
    plt.xlabel("Blocks")
    plt.ylabel("CDF")
    plt.grid(True)

plt.tight_layout()
plt.suptitle("Extent Size CDF by Device (≤ 99.9th %tile)", fontsize=16, y=1.02)
plt.show()
