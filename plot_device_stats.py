import pandas as pd
import matplotlib.pyplot as plt

# CSV 로딩
df = pd.read_csv("device_stats.csv")
df["device"] = df["device"].str.replace("^_dev_", "/dev/", regex=True)

# 📊 Plotting
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.bar(df["device"], df["files"])
plt.title("Number of Files")
plt.ylabel("Count")
plt.xticks(rotation=45)

plt.subplot(2, 2, 2)
plt.bar(df["device"], df["avg_blocks_per_extent"])
plt.title("Avg. Blocks per Extent")
plt.ylabel("Blocks")
plt.xticks(rotation=45)

plt.subplot(2, 2, 3)
plt.bar(df["device"], df["avg_blocks_per_file"])
plt.title("Avg. Blocks per File")
plt.ylabel("Blocks")
plt.xticks(rotation=45)

plt.subplot(2, 2, 4)
plt.bar(df["device"], df["blocks"])
plt.title("Total Blocks")
plt.ylabel("Blocks")
plt.xticks(rotation=45)

plt.tight_layout()
plt.suptitle("Device-level Extent Analysis Summary", fontsize=16, y=1.02)
plt.show()
