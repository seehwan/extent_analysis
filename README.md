# Ext4 Device-Based Extent Analysis

이 프로젝트는 **Ext4 파일시스템**의 **디바이스 단위** 마운트 지점에 대해, 모든 파일의 extent 정보를 병렬로 수집·병합·분석하기 위한 스크립트와 코드 모음입니다. 터미널을 닫아도 계속 실행될 수 있도록 `nohup` 방식을 지원하며, 최종적으로 CSV 형태의 결과를 생성해 다양한 통계와 시각화를 제공합니다.

---

## 📂 파일 목록

1. **collect_extents_by_device.sh**  
   - 디바이스별 병렬 분석을 총괄하는 스크립트입니다.  
   - 실행 전 이전 결과 디렉토리(`extent_output_by_device`)와 병합 파일(`file_extent_by_device.csv`)을 정리(삭제)합니다.  
   - `df --output=source,target -x tmpfs -x devtmpfs` 명령으로 디바이스를 탐색한 뒤, 각 마운트 포인트를 대상으로 `extract_extents_by_dir.py`를 병렬로 실행합니다.  
   - 모든 병렬 작업이 끝나면 `merge_extents.py`를 통해 CSV를 병합한 뒤, 최종 결과(`file_extent_by_device.csv`)를 생성합니다.

2. **extract_extents_by_dir.py**  
   - 특정 디렉토리(마운트 지점 포함) 하위의 모든 파일을 재귀적으로 순회하며, `filefrag -v`를 사용해 extent 정보를 수집합니다.  
   - 파일별로 `파일경로,Extent번호,블록수` 형식으로 CSV에 기록합니다.  
   - 심볼릭 링크나 권한 실패, `filefrag` 오류 등은 자동으로 제외되며, 로그 파일(`debug_extract.log`)도 생성하지 않는 버전으로 구성되었습니다.

3. **merge_extents.py**  
   - 하나의 디렉토리에 존재하는 여러 CSV 파일을 **단일 CSV**로 병합합니다.  
   - `pandas`의 `pd.concat`을 활용해 결과를 통합하고, `file_extent_by_device.csv` (또는 지정된 파일명)으로 내보냅니다.

4. **analyze_extents.py** (선택)  
   - 최종 병합된 CSV 파일(`file_extent_by_device.csv`)을 읽어, **통계/시각화**를 수행합니다.  
   - 예: Extent 블록 수 분포 히스토그램, 단편화 상위 파일 목록, 디렉토리별/디바이스별 평균 블록 수 등의 통계.

---

## 🚀 사용 방법

1. **의존성 설치**

```bash
sudo apt update
sudo apt install parallel e2fsprogs
sudo pip3 install pandas matplotlib seaborn tqdm

2. **권한 부여**
```bash
chmod +x collect_extents_by_device.sh

3. **nohup으로 실행**
```bash
sudo nohup ./collect_extents_by_device.sh > device_analysis_$(date +%Y%m%d_%H%M%S).log 2>&1 &

백그라운드에서 실행되며, 터미널을 닫아도 계속 동작

모든 디바이스 분석이 끝나면 자동으로 CSV를 병합하여 file_extent_by_device.csv 생성

4. **결과 확인**

디바이스별 CSV: extent_output_by_device/*.csv

병합 결과: file_extent_by_device.csv

5. **(선택) analyze_extents.py를 실행해 시각화/통계 확인**

---

## 📊 분석 예시
히스토그램: Extent 블록 수 분포

단편화 상위 파일: Extent 개수가 많은 파일 찾기

디바이스별 비교:

각 디바이스의 평균/최대/총 블록 수


---

## 📝 참고
extract_extents_by_dir.py는 로그를 남기지 않는 버전이므로, 오류나 제외된 파일 정보를 알고 싶다면 로깅 기능을 추가할 수 있음.

심볼릭 링크, 접근 불가 파일, filefrag 실패 파일은 결과에 기록되지 않습니다.

필요하면 analyze_by_storage.py 같은 고급 스크립트로 스토리지 단위 또는 디렉토리 단위 세분화 분석도 가능.


---

## 🙏 기여 / 문의
본 스크립트는 내부 디스크 단편화 분석용으로 제작되었습니다.
이슈나 개선 사항 있으면 언제든 알려주세요!
