import os
import csv
import glob
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

input_dir = "extent_output_by_device"
all_blocks = []
device_blocks = {}

# Read all extent sizes
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

# Compute 90th percentile cutoff
p90 = np.percentile(all_blocks, 90)
print(f"📌 90th percentile: {p90:.2f} blocks")

# CDF plot helper
def plot_tail_cdf(data, label=None):
    data = np.array([x for x in data if x > p90])
    if len(data) == 0:
        return
    data = np.sort(data)
    y = np.linspace(0, 1, len(data))
    plt.plot(data, y, label=label)

# 🎯 1. Global tail CDF
filtered_all = [x for x in all_blocks if x > p90]
plt.figure(figsize=(8, 5))
plot_tail_cdf(filtered_all)
plt.title("Extent Size Tail CDF (All Devices, >90th percentile)")
plt.xlabel("Blocks per Extent")
plt.ylabel("Cumulative Probability (Tail)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🎯 2. Per-device tail CDFs
device_list = list(device_blocks.keys())
max_per_row = 3
rows = ceil(len(device_list) / max_per_row)
plt.figure(figsize=(5 * max_per_row, 4 * rows))

for idx, device in enumerate(device_list):
    plt.subplot(rows, max_per_row, idx + 1)
    tail_data = [x for x in device_blocks[device] if x > p90]
    if tail_data:
        plot_tail_cdf(tail_data)
    plt.title(device.replace("_dev_", "/dev/"))
    plt.xlabel("Blocks")
    plt.ylabel("Tail CDF")
    plt.grid(True)

plt.tight_layout()
plt.suptitle("Extent Size Tail CDF by Device (>90th percentile)", fontsize=16, y=1.02)
plt.show()
