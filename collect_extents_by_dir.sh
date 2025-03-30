#!/bin/bash
# sudo nohup ./collect_extents_by_dir.sh > analysis_$(date +%Y%m%d_%H%M%S).log 2>&1 &

set -e

OUTPUT_DIR="extent_output"
MERGED_FILE="file_extent_details.csv"
ANALYSIS_SCRIPT="analyze_extents.py"
mkdir -p "$OUTPUT_DIR"
echo "hash,original_path" > "$OUTPUT_DIR/directory_map.csv"

# 최상위 디렉토리 목록 (루트 제외)
DIRS=$(find / -mindepth 1 -maxdepth 1 -type d \
  ! -path "/proc" \
  ! -path "/sys" \
  ! -path "/dev" \
  ! -path "/run" \
  ! -path "/tmp" \
  ! -path "/snap" 2>/dev/null)

# 디렉토리별 병렬 실행 (GNU parallel 사용, 최대 병렬성)
echo "$DIRS" | parallel --jobs 0 --will-cite --line-buffer ' \
  hash=$(echo -n {} | md5sum | cut -d" " -f1); \
  out_file="$OUTPUT_DIR/${hash}.csv"; \
  echo "🔍 {} -> $out_file"; \
  echo "$hash,{}" >> "$OUTPUT_DIR/directory_map.csv"; \
  python3 extract_extents_by_dir.py "{}" "$out_file"'

echo "✅ 모든 디렉토리 분석 완료: $OUTPUT_DIR/*.csv"

# 결과 병합
echo "📦 병합 중..."
python3 merge_extents.py

# 분석 실행
echo "📊 분석 중..."
python3 analyze_extents.py

echo "✅ 통합 실행 완료: 결과 파일은 $MERGED_FILE, 시각화 완료"