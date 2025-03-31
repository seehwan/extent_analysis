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

# Compute 99th percentile
p99 = np.percentile(all_blocks, 99)
print(f"📌 99th percentile: {p99:.2f} blocks")

# Tail CDF plotting helper
def plot_tail_cdf(data, label=None):
    data = np.array([x for x in data if x > p99])
    if len(data) == 0:
        return
    data = np.sort(data)
    y = np.linspace(0.99, 1.0, len(data))
    plt.plot(data, y, label=label)

# 🎯 1. Global Tail CDF (>99th percentile)
filtered_all = [x for x in all_blocks if x > p99]
plt.figure(figsize=(8, 5))
plot_tail_cdf(filtered_all)
plt.title("Extent Size Tail CDF (All Devices, >99th percentile)")
plt.xlabel("Blocks per Extent")
plt.ylabel("Cumulative Probability (Tail)")
plt.ylim(0.99, 1.0)
plt.grid(True)
plt.tight_layout()
plt.show()

# 🎯 2. Per-device Tail CDFs
device_list = list(device_blocks.keys())
max_per_row = 3
rows = ceil(len(device_list) / max_per_row)
plt.figure(figsize=(5 * max_per_row, 4 * rows))

for idx, device in enumerate(device_list):
    plt.subplot(rows, max_per_row, idx + 1)
    tail_data = [x for x in device_blocks[device] if x > p99]
    if tail_data:
        plot_tail_cdf(tail_data)
    plt.title(device.replace("_dev_", "/dev/"))
    plt.xlabel("Blocks")
    plt.ylabel("CDF")
    plt.ylim(0.99, 1.0)
    plt.grid(True)

plt.tight_layout()
plt.suptitle("Extent Size Tail CDF by Device (>99th percentile)", fontsize=16, y=1.02)
plt.show()
