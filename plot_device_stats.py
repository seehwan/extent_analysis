import pandas as pd
import matplotlib.pyplot as plt

# CSV 로딩
df = pd.read_csv("device_stats.csv")
df["device"] = df["device"].str.replace("^_dev_", "/dev/", regex=True)

# 📊 시각화
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.bar(df["device"], df["files"])
plt.title("📁 파일 개수")
plt.ylabel("개수")
plt.xticks(rotation=45)

plt.subplot(2, 2, 2)
plt.bar(df["device"], df["avg_blocks_per_extent"])
plt.title("🧱 평균 블록 수 (Extent 기준)")
plt.ylabel("블록 수")
plt.xticks(rotation=45)

plt.subplot(2, 2, 3)
plt.bar(df["device"], df["avg_blocks_per_file"])
plt.title("📦 평균 블록 수 (File 기준)")
plt.ylabel("블록 수")
plt.xticks(rotation=45)

plt.subplot(2, 2, 4)
plt.bar(df["device"], df["blocks"])
plt.title("📊 총 블록 수")
plt.ylabel("블록 수")
plt.xticks(rotation=45)

plt.tight_layout()
plt.suptitle("디바이스별 Extent 분석 통계", fontsize=16, y=1.02)
plt.show()
