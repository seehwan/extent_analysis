#!/bin/bash

set -e

echo "📂 [1] 분석 대상 파일 목록 수집 중..."

# 정제된 파일 수집: 일반 파일만 + 가상/장치 경로 제외
find / \
  -type f \
  -not -path "/proc/*" \
  -not -path "/sys/*" \
  -not -path "/dev/*" \
  -not -path "/run/*" \
  -not -path "/tmp/*" \
  -not -path "/snap/*" \
  -readable \
  2>/dev/null > all_files.txt

echo "📄 수집된 일반 파일 수: $(wc -l < all_files.txt)"

echo "📦 [2] 결과 디렉토리 초기화"
mkdir -p extent_output
rm -f extent_output/*.csv

echo "⚙️ [3] 병렬 실행 시작..."
cat all_files.txt | parallel -j $(nproc) python3 extract_extents.py {}

echo "✅ 파일별 extent 수집 완료!"
