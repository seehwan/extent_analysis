import pandas as pd
import matplotlib.pyplot as plt

# CSV 불러오기
df = pd.read_csv("device_stats.csv")
df["device"] = df["device"].str.replace("^_dev_", "/dev/", regex=True)

# 공통: 바 위에 숫자 표시 함수
def annotate_bars(ax, fmt="{:.0f}"):
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(fmt.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 바 위에 3pt 띄우기
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9)

# 📊 그래프 시작
plt.figure(figsize=(12, 6))

# 1. 파일 개수
ax1 = plt.subplot(2, 2, 1)
bars = ax1.bar(df["device"], df["files"])
ax1.set_title("Number of Files")
ax1.set_ylabel("Count")
ax1.grid(True, axis='y')
plt.xticks(rotation=45)
annotate_bars(ax1)

# 2. 평균 블록 수 (Extent 기준)
ax2 = plt.subplot(2, 2, 2)
bars = ax2.bar(df["device"], df["avg_blocks_per_extent"])
ax2.set_title("Avg. Blocks per Extent")
ax2.set_ylabel("Blocks")
ax2.grid(True, axis='y')
plt.xticks(rotation=45)
annotate_bars(ax2, fmt="{:.2f}")

# 3. 평균 블록 수 (File 기준)
ax3 = plt.subplot(2, 2, 3)
bars = ax3.bar(df["device"], df["avg_blocks_per_file"])
ax3.set_title("Avg. Blocks per File")
ax3.set_ylabel("Blocks")
ax3.grid(True, axis='y')
plt.xticks(rotation=45)
annotate_bars(ax3, fmt="{:.2f}")

# 4. 총 블록 수
ax4 = plt.subplot(2, 2, 4)
bars = ax4.bar(df["device"], df["blocks"])
ax4.set_title("Total Blocks")
ax4.set_ylabel("Blocks")
ax4.grid(True, axis='y')
plt.xticks(rotation=45)
annotate_bars(ax4)

plt.tight_layout()
plt.suptitle("Device-level Extent Statistics", fontsize=16, y=1.02)
plt.show()
