#!/bin/bash

set -e

OUTPUT_DIR="extent_output_by_device"
MERGED_FILE="file_extent_by_device.csv"
# 이전 결과 제거
if [ -d "$OUTPUT_DIR" ]; then
  echo "🧹 이전 디바이스별 결과 정리 중: $OUTPUT_DIR"
  rm -rf "$OUTPUT_DIR"
fi

if [ -f "$MERGED_FILE" ]; then
  echo "🧹 이전 병합 파일 제거: $MERGED_FILE"
  rm -f "$MERGED_FILE"
fi

rm -f device_analysis_*.log 2>/dev/null || true
# 디바이스별 결과 저장 디렉토리 생성
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