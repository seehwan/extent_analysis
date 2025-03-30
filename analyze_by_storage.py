# analyze_by_storage.py

# 디바이스 매핑 함수
def get_device(path):
    try:
        output = subprocess.check_output(["df", path], stderr=subprocess.DEVNULL).decode()
        return output.splitlines()[1].split()[0]
    except:
        return "unknown"

# 디바이스 매핑 수행 (파일 수가 많을 경우 성능 이슈 유의)
file_list = df["파일경로"].unique()
file_device_map = {}
print("[*] 디바이스 정보 매핑 중...")
for path in tqdm(file_list):
    file_device_map[path] = get_device(path)

df["디바이스"] = df["파일경로"].map(file_device_map)

# 디바이스별 통계
storage_stats = df.groupby("디바이스").agg(
    평균Extent블록수=("블록수", "mean"),
    최대Extent블록수=("블록수", "max"),
    총Extent수=("Extent번호", "count"),
    총블록수=("블록수", "sum")
).reset_index()

# 출력
print("\n📦 디바이스별 Extent 통계:")
print(storage_stats.sort_values("총Extent수", ascending=False))

# 시각화
plt.figure(figsize=(12, 6))
plt.bar(storage_stats["디바이스"], storage_stats["평균Extent블록수"])
plt.xticks(rotation=90, ha="right")  # 긴 디바이스명 대응
plt.ylabel("평균 Extent 블록 수")
plt.title("스토리지별 평균 Extent 블록 수")
plt.tight_layout()
plt.grid(True)
plt.show()