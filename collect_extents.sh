#!/bin/bash

echo "🔍 전체 파일 목록 수집 중..."
find / -type f 2>/dev/null > all_files.txt

echo "📂 출력 디렉토리 초기화 중..."
mkdir -p extent_output
rm -f extent_output/*.csv

echo "⚙️ 병렬 실행 시작..."
cat all_files.txt | parallel -j $(nproc) python3 extract_extents.py {}

echo "✅ 파일별 extent 리스트 수집 완료!"
