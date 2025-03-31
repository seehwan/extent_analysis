import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

input_dir = "extent_output_by_device"
output_csv = "device_stats.csv"
rows = []

# 디바이스별 통계 수집
for filename in os.listdir(input_dir):
    if not filename.endswith(".csv"):
        continue

    device = filename.replace(".csv", "")
    file_path = os.path.join(input_dir, filename)

    try:
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            lines = list(reader)
    except Exception as e:
        print(f"⚠️ {file_path} 읽기 실패: {e}")
        continue

    if not lines:
        rows.append([device, 0, 0, 0, 0, 0])
        continue

    # 파일 개수
    file_paths = set(row[0] for row in lines if len(row) >= 3)
    file_count = len(file_paths)

    # extent 수
    extent_count = len(lines)

    # 블록 수
    block_sum = 0
    for row in lines:
        try:
            block_sum += int(row[-1])
        except:
            continue

    avg_blocks_per_extent = block_sum / extent_count if extent_count else 0
    avg_blocks_per_file = block_sum / file_count if file_count else 0

    rows.append([
        device, file_count, extent_count, block_sum,
        round(avg_blocks_per_extent, 2),
        round(avg_blocks_per_file, 2)
    ])

# CSV 저장
df = pd.DataFrame(rows, columns=[
    "device", "files", "extents", "blocks",
    "avg_blocks_per_extent", "avg_blocks_per_file"
])
df["device"] = df["device"].str.replace("^_dev_", "/dev/", regex=True)
df.to_csv(output_csv, index=False)
print(f"✅ 통계 저장 완료: {output_csv}")

# 📊 시각화
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.bar(df["device"], df["files"])
plt.title("📁 파일 개수")
plt.xticks(rotation=45)

plt.subplot(2, 2, 2)
plt.bar(df["device"], df["avg_blocks_per_extent"])
plt.title("🧱 평균 블록 수 (Extent 기준)")
plt.xticks(rotation=45)

plt.subplot(2, 2, 3)
plt.bar(df["device"], df["avg_blocks_per_file"])
plt.title("📦 평균 블록 수 (File 기준)")
plt.xticks(rotation=45)

plt.subplot(2, 2, 4)
plt.bar(df["device"], df["blocks"])
plt.title("📊 총 블록 수")
plt.xticks(rotation=45)

plt.tight_layout()
plt.suptitle("디바이스별 Extent 분석 통계", fontsize=16, y=1.02)
plt.show()
