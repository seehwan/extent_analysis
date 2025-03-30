import pandas as pd
import glob
import sys

input_dir = sys.argv[1] if len(sys.argv) > 1 else "extent_output_by_device"
csv_files = glob.glob(f"{input_dir}/*.csv")

if not csv_files:
    print(f"⚠️ No CSV files found in {input_dir}, skipping merge.")
    sys.exit(0)

dfs = []
for f in csv_files:
    df = pd.read_csv(f, header=None, names=["파일경로","Extent번호","블록수"])
    if not df.empty:
        dfs.append(df)

if not dfs:
    print("⚠️ All CSVs are empty! Nothing to concatenate.")
    sys.exit(0)

merged = pd.concat(dfs, ignore_index=True)
merged.to_csv("file_extent_details.csv", index=False)
print("✅ 병합 완료: file_extent_details.csv")