import pandas as pd
import glob

files = glob.glob("extent_output/*.csv")
dfs = []

for f in files:
    df = pd.read_csv(f, header=None, names=["파일경로", "Extent번호", "Extent크기(Bytes)"])
    dfs.append(df)

merged = pd.concat(dfs, ignore_index=True)
merged.to_csv("file_extent_details.csv", index=False)
print("✅ 병합 완료: file_extent_details.csv")
