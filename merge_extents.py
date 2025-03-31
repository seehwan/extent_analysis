import os
import sys
import glob
import csv
import pandas as pd

input_dir = sys.argv[1] if len(sys.argv) > 1 else "extent_output"
rows = []

for f in glob.glob(os.path.join(input_dir, "*.csv")):
    with open(f, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            extent_num = row[-2]
            block_count = row[-1]
            file_path = ",".join(row[:-2])
            try:
                rows.append((file_path, int(extent_num), int(block_count)))
            except ValueError:
                continue

# DataFrame으로 변환
df = pd.DataFrame(rows, columns=["파일경로", "Extent번호", "블록수"])
df.to_csv("file_extent_details.csv", index=False)
print("✅ 병합 완료: file_extent_details.csv")
