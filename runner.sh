#!/bin/bash

set -e

echo "────────────────────────────────────────────"
echo "🚀 Ext4 파일시스템 Extent 분석 자동 실행 시작"
echo "────────────────────────────────────────────"

# ✅ 1. 의존성 확인
echo "[*] 필수 명령어 확인 중..."
for cmd in filefrag parallel python3; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ '$cmd' 명령어가 설치되어 있지 않습니다. 설치 후 재실행하세요."
        exit 1
    fi
done

echo "[*] Python 패키지 확인 중..."
REQUIRED_PYTHON_PKGS=(pandas matplotlib tqdm seaborn)
for pkg in "${REQUIRED_PYTHON_PKGS[@]}"; do
    if ! python3 -c "import $pkg" &> /dev/null; then
        echo "📦 '$pkg' 패키지 설치 중..."
        python3 -m pip install --quiet "$pkg"
    fi
done

# ✅ 2. Extent 수집 시작
echo "📡 실제 스토리지 파일 대상만 골라서 extent 수집 시작..."
sudo ./collect_extents.sh

# ✅ 3. 결과 병합
echo "🧩 수집된 extent 데이터를 하나의 CSV로 병합..."
python3 merge_extents.py

# ✅ 4. 분석 및 시각화
echo "📊 분석 시작: 기본 통계, 시각화, 단편화 상위 파일..."
python3 analyze_extents.py

echo "💽 분석 시작: 스토리지(디바이스)별 Extent 통계 및 시각화..."
python3 analyze_by_storage.py

echo "✅ 전체 분석 완료!"
echo "📁 병합 CSV: file_extent_details.csv"
echo "📂 개별 CSV: extent_output/"
