📦 Extent Analyzer by Directory (High Performance)

이 프로젝트는 Linux ext4 파일시스템에서 디렉토리 단위로 extent 정보를 병렬로 분석하고, 그 결과를 통합 및 시각화하는 도구입니다. 대규모 시스템에서도 효율적으로 동작할 수 있도록 설계되었습니다.

🚀 주요 기능

디렉토리 단위로 병렬 분석 (GNU parallel 사용)

최대 병렬성 지원 (--jobs 0)

결과 CSV 파일은 해시 기반 파일명으로 안전하게 저장

extent 정보는 블록 수 단위로 저장

병합 및 분석 자동화 통합 실행 스크립트 포함

📁 프로젝트 구성

.
├── extract_extents_by_dir.py       # 디렉토리 내 파일 분석 (단일 CSV 저장)
├── collect_extents_by_dir.sh       # 전체 병렬 분석 + 병합 + 분석 자동화
├── merge_extents.py                # CSV 파일 병합
├── analyze_extents.py              # 시각화 및 통계 출력
├── analyze_by_storage.py           # 디바이스별 통계 분석
├── extent_output/                  # 디렉토리 해시 기반 결과 파일 저장소
│   └── directory_map.csv           # 해시 ↔ 실제 경로 매핑 테이블
└── file_extent_details.csv         # 병합된 최종 결과

⚙️ 실행 방법

1. 의존성 설치

sudo apt install parallel e2fsprogs
pip3 install pandas matplotlib seaborn tqdm

2. 분석 스크립트 실행

sudo nohup ./collect_extents_by_dir.sh > analysis_$(date +%Y%m%d_%H%M%S).log 2>&1 &

디렉토리별로 병렬로 분석

결과 자동 병합 및 시각화

로그는 analysis_*.log에 저장됨

3. 분석 결과 확인

병합된 결과: file_extent_details.csv

디렉토리별 원본: extent_output/*.csv

디렉토리 맵: extent_output/directory_map.csv

📊 출력 예시

히스토그램: extent 블록 수 분포

산점도: 평균 vs 최대 블록 수

디렉토리별 평균 extent 블록 수

단편화 상위 파일 목록

🧠 참고사항

출력 CSV는 파일경로,Extent번호,블록수 형식

심볼릭 링크, 접근 불가 파일, 비정상 파일은 자동 제외됨

디렉토리 해시는 md5 기반으로 생성

📬 기여 및 개선 제안

추가 분석 포맷 (SQLite, Parquet)

스토리지별 리포트 자동 생성

대시보드 연동 등 확장 가능

필요한 기능이나 개선 아이디어가 있다면 언제든지 제안해 주세요!

Happy Analyzing 🚀
