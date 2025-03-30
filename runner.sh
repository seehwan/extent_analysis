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

# ✅ 2. 전체 extent 병렬 수집
echo "📡 전체 파일 시스템에서 extent 정보 수집 중..."
sudo ./collect_extents.sh

# ✅ 3. 결과 병합
echo "🧩 결과 병합 중..."
python3 merge_extents.py

# ✅ 4. 분석 및 시각화
echo "📊 기본 분석 및 시각화 실행 중..."
python3 analyze_extents.py

echo "💽 스토리지(디바이스)별 분석 실행 중..."
python3 analyze_by_storage.py

echo "✅ 전체 분석 완료!"
echo "📁 결과 CSV: file_extent_details.csv"
echo "📂 개별 결과: extent_output/"
