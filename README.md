📊 Ext4 Extent Analyzer

이 프로젝트는 Linux Ext4 파일시스템의 모든 파일에 대해 실제 extent 크기 리스트를 병렬로 수집하고 분석하는 고급 자동화 도구입니다. 디스크 단편화 정도, 스토리지 효율, 디바이스별 통계를 시각화할 수 있습니다.

🚀 주요 기능

전체 파일시스템의 extent 정보 수집 (filefrag 사용)

장치 파일, 가상 파일, 소켓 등 비분석 대상 자동 제외

디렉토리별 병렬 처리 (GNU parallel 활용)

안전한 해시 기반 결과 저장 (파일 이름 충돌 방지)

분석 결과 병합 및 시각화 (히스토그램, 산점도, 디바이스별 그래프)

실패 로그 및 디버깅 지원 (debug_extract.log)

📁 프로젝트 구성

.
├── extract_extents.py         # 단일 파일에 대해 extent 정보 수집
├── collect_extents.sh         # 전체 병렬 수집 실행 스크립트
├── merge_extents.py           # 결과 CSV 병합
├── analyze_extents.py         # 분석 + 시각화 (디렉토리/단편화 등)
├── analyze_by_storage.py      # 디바이스별 분석 및 그래프 출력
├── extent_output/             # 파일별 CSV 출력 디렉토리
├── file_extent_details.csv    # 최종 병합 결과
├── all_files.txt              # 분석 대상 파일 목록
├── debug_extract.log          # 실패/예외 기록 로그

⚙️ 실행 방법

1. 사전 준비

chmod +x collect_extents.sh

2. 전체 분석 실행

sudo ./collect_extents.sh

3. 병합 및 분석

python3 merge_extents.py
python3 analyze_extents.py
python3 analyze_by_storage.py

4. 백그라운드 실행 (선택)

nohup ./collect_extents.sh > log.txt 2>&1 &

📊 출력 예시

히스토그램: 전체 extent 크기 분포 (log-log)

산점도: 파일별 평균 vs 최대 extent 크기

바 차트: 디렉토리별, 디바이스별 평균 extent 크기

단편화 상위 파일 목록 출력

🛠 의존성

Python 3.x

Python packages:

pandas

matplotlib

seaborn

tqdm

시스템 명령어:

filefrag

df

parallel

설치 예시:

sudo apt install e2fsprogs coreutils parallel
python3 -m pip install pandas matplotlib seaborn tqdm

📌 참고사항

filefrag는 root 권한에서 더 많은 정보를 제공합니다.

df 실패하는 파일은 자동 제외됩니다.

파일명이 길거나 복잡할 수 있으므로 해시(md5) 기반 파일 저장을 사용합니다.

📬 문의 및 기여

이 프로젝트는 내부 분석 및 디스크 최적화 목적에 맞춰 설계되었습니다.
기여, 개선 제안, 이슈는 언제든 환영합니다!

