# analyze_extents.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import subprocess

# CSV 로딩
df = pd.read_csv("file_extent_details.csv")
df["디렉토리"] = df["파일경로"].apply(lambda x: os.path.dirname(x))

# 파일별 통계
file_stats = df.groupby("파일경로").agg(
    Extent수=("Extent번호", "count"),
    총블록수=("블록수", "sum"),
    최대블록수=("블록수", "max"),
    평균블록수=("블록수", "mean")
).reset_index()

# 디렉토리별 평균
dir_stats = df.groupby("디렉토리").agg(
    평균Extent블록수=("블록수", "mean"),
    Extent총수=("Extent번호", "count")
).reset_index()

# 히스토그램
plt.figure(figsize=(10, 6))
sns.histplot(df["블록수"], bins=100, log_scale=(True, True))
plt.title("Extent 블록 수 분포 (log-log)")
plt.xlabel("Extent 블록 수")
plt.ylabel("개수")
plt.grid(True)
plt.tight_layout()
plt.show()

# 단편화 상위 파일
top_frag = file_stats.sort_values("Extent수", ascending=False).head(20)
print("\n📌 단편화 상위 20개 파일:")
print(top_frag[["파일경로", "Extent수", "총블록수", "평균블록수", "최대블록수"]])

# 평균 vs 최대 extent 산점도
plt.figure(figsize=(10, 6))
plt.scatter(file_stats["평균블록수"], file_stats["최대블록수"], alpha=0.5)
plt.xlabel("평균 Extent 블록 수")
plt.ylabel("최대 Extent 블록 수")
plt.title("파일별 평균 vs 최대 Extent 블록 수")
plt.grid(True)
plt.tight_layout()
plt.show()

# 디렉토리별 평균 extent 크기
top_dirs = dir_stats.sort_values("Extent총수", ascending=False).head(20)
plt.figure(figsize=(12, 6))
sns.barplot(data=top_dirs, x="디렉토리", y="평균Extent블록수")
plt.xticks(rotation=45, ha="right")
plt.title("디렉토리별 평균 Extent 블록 수 (상위 20개)")
plt.ylabel("평균 Extent 블록 수")
plt.tight_layout()
plt.show()