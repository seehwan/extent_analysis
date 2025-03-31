import os
import csv
import glob
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

input_dir = "extent_output_by_device"
all_blocks = []
device_blocks = {}

# Read extent sizes from CSVs
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

def plot_cdf(data, label=None):
    data = np.sort(data)
    y = np.linspace(0, 1, len(data))
    plt.plot(data, y, label=label)

# 🎯 1. Overall CDF
plt.figure(figsize=(8, 5))
plot_cdf(all_blocks)
plt.title("CDF of Extent Sizes (All Devices)")
plt.xlabel("Blocks per Extent")
plt.ylabel("Cumulative Probability")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🎯 2. Per-device CDFs
device_list = list(device_blocks.keys())
max_per_row = 3
rows = ceil(len(device_list) / max_per_row)
plt.figure(figsize=(5 * max_per_row, 4 * rows))

for idx, device in enumerate(device_list):
    plt.subplot(rows, max_per_row, idx + 1)
    plot_cdf(device_blocks[device])
    plt.title(device.replace("_dev_", "/dev/"))
    plt.xlabel("Blocks")
    plt.ylabel("CDF")
    plt.grid(True)

plt.tight_layout()
plt.suptitle("Extent Size CDF by Device", fontsize=16, y=1.02)
plt.show()
