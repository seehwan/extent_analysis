#!/bin/bash

set -e

OUTPUT_DIR="extent_output_by_device"
MERGED_FILE="file_extent_by_device.csv"
mkdir -p "$OUTPUT_DIR"
echo "device,mount_point" > "$OUTPUT_DIR/device_map.csv"

# 마운트된 디바이스 목록 추출 (tmpfs/devtmpfs 제외)
df --output=source,target -x tmpfs -x devtmpfs | tail -n +2 | while read dev mount; do
  if [[ "$dev" == /dev/* ]]; then
    safe_name=$(echo "$dev" | sed 's|/|_|g')
    out_file="$OUTPUT_DIR/${safe_name}.csv"
    echo "🔍 $dev ($mount) → $out_file"
    echo "$dev,$mount" >> "$OUTPUT_DIR/device_map.csv"
    python3 extract_extents_by_dir.py "$mount" "$out_file" &
  fi
done

wait

echo "✅ 모든 디바이스 분석 완료: $OUTPUT_DIR/*.csv"

# 결과 병합
echo "📦 병합 중..."
python3 merge_extents.py "$OUTPUT_DIR" > "$MERGED_FILE"
echo "✅ 병합 파일 생성: $MERGED_FILE"