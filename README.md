# extent_analysis
extent_analysis
지금부터 전체 파일시스템의 실제 extent 크기 리스트를 병렬로 수집해서 CSV로 분석하는 풀 파이프라인을 만들어줄게.

🧱 전체 구성 요소
구성 파일	역할 설명
collect_extents.sh	전체 파일을 대상으로 extent 추출 병렬 실행
extract_extents.py	개별 파일의 extent 크기 리스트 수집
merge_extents.py	모든 개별 CSV → 하나의 병합 CSV 생성
analyze_extents.py	히스토그램, 단편화 상위 파일, 디렉토리 분석
analyze_by_storage.py	스토리지(디바이스)별 extent 통계 및 시각화
extent_output/	개별 파일 결과 저장 폴더
file_extent_details.csv	병합된 전체 extent 데이터

🚀 실행 순서 요약
✅ 1. 전체 extent 수집 실행
bash
복사
편집
sudo ./collect_extents.sh
/ 전체 파일 대상

GNU parallel로 병렬 실행

extent_output/*.csv로 저장됨

✅ 2. 결과 병합
bash
복사
편집
python3 merge_extents.py
extent_output/*.csv → file_extent_details.csv

분석을 위한 통합 CSV 파일 생성

✅ 3. 분석 및 시각화 (선택적 개별 실행 가능)
📊 기본 분석 + 시각화
bash
복사
편집
python3 analyze_extents.py
Extent 크기 분포 (log-log 히스토그램)

단편화 상위 20개 파일

평균 vs 최대 extent 크기 산점도

디렉토리별 평균 extent 크기

💽 스토리지별 분석
bash
복사
편집
python3 analyze_by_storage.py
파일별로 df 명령으로 실제 마운트 디바이스 추출

디바이스별 평균, 최대, 총 extent 수/용량 출력

막대 그래프로 시각화

📁 최종 산출물
파일 / 폴더	내용
extent_output/	파일별 extent 리스트 개별 저장
file_extent_details.csv	모든 파일의 extent 정보 병합 결과
analyze_extents.py 그래프	분포, 단편화 파일, 디렉토리 분석
analyze_by_storage.py 결과	스토리지별 평균 extent 통계
