# extent_analysis
extent_analysis
지금부터 전체 파일시스템의 실제 extent 크기 리스트를 병렬로 수집해서 CSV로 분석하는 풀 파이프라인을 만들어줄게.

✅ 구성 개요
단계	설명
1	전체 파일 목록 수집 (find / -type f)
2	extract_extents.py: 단일 파일의 extent 리스트 수집
3	GNU parallel로 병렬 실행
4	extent_output/에 개별 CSV 저장
5	병합 스크립트로 하나의 file_extent_details.csv 생성
6	시각화 및 통계 분석은 다음 단계에서 가능
📁 디렉토리 구조
복사
편집
extent_analysis/
├── extract_extents.py         ← 단일 파일 처리 스크립트
├── collect_extents.sh         ← 전체 병렬 수집 자동화
├── merge_extents.py           ← CSV 병합
├── extent_output/             ← 개별 결과 저장 폴더
├── file_extent_details.csv    ← 병합된 최종 결과
