#!/bin/bash

set -e

TARGET_FILE="all_files.txt"

echo "📂 [1] 분석 대상 파일 목록 준비 중..."

if [ -f "$TARGET_FILE" ]; then
    echo "✅ 기존 '$TARGET_FILE' 파일이 존재합니다. 재사용합니다."
else
    echo "🔍 파일 목록이 없으므로 새로 수집합니다..."
    find / \
      -type f \
      -not -path "/proc/*" \
      -not -path "/sys/*" \
      -not -path "/dev/*" \
      -not -path "/run/*" \
      -not -path "/tmp/*" \
      -not -path "/snap/*" \
      -readable \
      2>/dev/null > "$TARGET_FILE"
    echo "📄 수집된 일반 파일 수: $(wc -l < $TARGET_FILE)"
fi
echo "📄 수집된 일반 파일 수: $(wc -l < all_files.txt)"

echo "📦 [2] 결과 디렉토리 초기화"
mkdir -p extent_output
rm -f extent_output/*.csv

echo "⚙️ [3] 병렬 실행 시작..."
cat all_files.txt | parallel -j $(nproc) python3 extract_extents.py {}

echo "✅ 파일별 extent 수집 완료!"
