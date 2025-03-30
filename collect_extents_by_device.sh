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

mkdir -p "$OUTPUT_DIR"
echo "device,mount_point" > "$OUTPUT_DIR/device_map.csv"

echo "🔎 디바이스 목록 수집 중..."
# - tmpfs/devtmpfs 제외
DEVICES=$(df --output=source,target -x tmpfs -x devtmpfs | tail -n +2 | grep '^/dev/')

# 디바이스별 병렬 실행 (GNU parallel)
# --jobs 0: 최대 병렬성
# --colsep ' +' : 공백 분리로 {1} {2} 매핑
# --line-buffer : 실시간 로그
echo "$DEVICES" | parallel --jobs 0 --colsep ' +' --line-buffer '
  safe_name=$(echo {1} | sed "s|/|_|g");   # /dev/sda1 -> _dev_sda1
  out_file="'$OUTPUT_DIR'/${safe_name}.csv";
  echo "{1},{2}" >> "'$OUTPUT_DIR'/device_map.csv";
  echo "🔍 {1} ({2}) -> $out_file";
  python3 extract_extents_by_dir.py "{2}" "$out_file"
'

echo "✅ 모든 디바이스 분석 완료: $OUTPUT_DIR/*.csv"

# 결과 병합
echo "📦 병합 중..."
python3 merge_extents.py "$OUTPUT_DIR" > "$MERGED_FILE"
echo "✅ 병합 파일 생성: $MERGED_FILE"