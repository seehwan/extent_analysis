# analyze_by_storage.py

import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os
from tqdm import tqdm

# CSV 로딩
df = pd.read_csv("file_extent_details.csv")

# 고유 파일만 추출하여 디바이스 매핑
file_list = df["파일경로"].unique()
file_device_map = {}

def get_device(path):
    try:
        output = subprocess.check_output(["df", path], stderr=subprocess.DEVNULL).decode()
        return output.splitlines()[1].split()[0]
    except:
        return "unknown"

print("[*] 디바이스 정보 매핑 중...")
for path in tqdm(file_list):
    file_device_map[path] = get_device(path)

df["디바이스"] = df["파일경로"].map(file_device_map)

# 통계 집계
storage_stats = df.groupby("디바이스").agg(
    평균Extent크기=("Extent크기(Bytes)", "mean"),
    최대Extent크기=("Extent크기(Bytes)", "max"),
    총Extent수=("Extent크기(Bytes)", "count"),
    총용량=("Extent크기(Bytes)", "sum")
).reset_index()

# 출력
print("\n📦 디바이스별 Extent 통계:")
print(storage_stats.sort_values("총Extent수", ascending=False))

# 시각화
plt.figure(figsize=(12, 6))
plt.bar(storage_stats["디바이스"], storage_stats["평균Extent크기"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("평균 Extent 크기 (Bytes)")
plt.title("스토리지별 평균 Extent 크기")
plt.tight_layout()
plt.grid(True)
plt.show()
