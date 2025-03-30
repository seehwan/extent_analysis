import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 파일 로드
df = pd.read_csv("file_extent_details.csv")

# 디렉토리 경로 추출
df["디렉토리"] = df["파일경로"].apply(lambda x: os.path.dirname(x))

# 파일별 통계 계산
file_stats = df.groupby("파일경로").agg(
    Extent수=("Extent번호", "count"),
    총크기=("Extent크기(Bytes)", "sum"),
    최대Extent=("Extent크기(Bytes)", "max"),
    평균Extent=("Extent크기(Bytes)", "mean")
).reset_index()

# 디렉토리별 평균 extent 크기 계산
dir_stats = df.groupby("디렉토리").agg(
    평균Extent크기=("Extent크기(Bytes)", "mean"),
    Extent총수=("Extent번호", "count")
).reset_index()

# ------------------------------
# 📊 히스토그램: 전체 extent 크기 분포
# ------------------------------
plt.figure(figsize=(10, 6))
sns.histplot(df["Extent크기(Bytes)"], bins=100, log_scale=(True, True))
plt.title("Extent 크기 분포 (log-log)")
plt.xlabel("Extent 크기 (Bytes)")
plt.ylabel("개수")
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# 🔝 단편화 심한 파일 상위 20개
# ------------------------------
top_frag = file_stats.sort_values("Extent수", ascending=False).head(20)
print("\n📌 단편화 상위 20개 파일:")
print(top_frag[["파일경로", "Extent수", "총크기", "평균Extent", "최대Extent"]])

# ------------------------------
# 📉 평균 vs 최대 extent 산점도
# ------------------------------
plt.figure(figsize=(10, 6))
plt.scatter(file_stats["평균Extent"], file_stats["최대Extent"], alpha=0.5)
plt.xlabel("평균 Extent 크기 (Bytes)")
plt.ylabel("최대 Extent 크기 (Bytes)")
plt.title("파일별 평균 vs 최대 Extent 크기")
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# 📁 디렉토리별 평균 extent 크기 (상위 20개)
# ------------------------------
top_dirs = dir_stats.sort_values("Extent총수", ascending=False).head(20)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_dirs, x="디렉토리", y="평균Extent크기")
plt.xticks(rotation=45, ha="right")
plt.title("디렉토리별 평균 Extent 크기 (상위 20개)")
plt.ylabel("평균 Extent 크기 (Bytes)")
plt.tight_layout()
plt.show()
