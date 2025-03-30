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
  - sudo apt update
  - sudo apt install parallel e2fsprogs
  - sudo pip3 install pandas matplotlib seaborn tqdm

2. **권한 부여**
  - chmod +x collect_extents_by_device.sh

3. **nohup으로 실행**
  - sudo nohup ./collect_extents_by_device.sh > device_analysis_$(date +%Y%m%d_%H%M%S).log 2>&1 &
  - 백그라운드에서 실행되며, 터미널을 닫아도 계속 동작
  - 모든 디바이스 분석이 끝나면 자동으로 CSV를 병합하여 file_extent_by_device.csv 생성

4. **결과 확인**
  - 디바이스별 CSV: extent_output_by_device/*.csv
  - 병합 결과: file_extent_by_device.csv

5. **(선택) analyze_extents.py를 실행해 시각화/통계 확인**


---

## 📊 분석 예시

- 히스토그램: Extent 블록 수 분포
- 단편화 상위 파일: Extent 개수가 많은 파일 찾기
- 디바이스별 비교: 각 디바이스의 평균/최대/총 블록 수

---

## 📝 참고
   - extract_extents_by_dir.py는 로그를 남기지 않는 버전이므로, 오류나 제외된 파일 정보를 알고 싶다면 로깅 기능을 추가할 수 있음.
   - 심볼릭 링크, 접근 불가 파일, filefrag 실패 파일은 결과에 기록되지 않습니다.
   - 필요하면 analyze_by_storage.py 같은 고급 스크립트로 스토리지 단위 또는 디렉토리 단위 세분화 분석도 가능.


---

## 🙏 기여 / 문의

본 스크립트는 내부 디스크 단편화 분석용으로 제작되었습니다.
이슈나 개선 사항 있으면 언제든 알려주세요!

---

# Ext4 Directory-Based Extent Analysis

이 프로젝트는 **Ext4 파일시스템**에서 상위 디렉토리를 기준으로 모든 하위 파일을 병렬로 분석하고, 결과를 병합·시각화하기 위한 일련의 스크립트로 구성되어 있습니다. 특히 `collect_extents_by_dir.sh`를 통해 `/home`, `/var` 같은 **최상위 디렉토리**들을 병렬 분석하고, 각각의 파일에 대한 extent 정보를 CSV로 수집할 수 있습니다.

---

## 📂 구성 파일

1. **`collect_extents_by_dir.sh`**  
   - **디렉토리 단위** 병렬 분석을 자동화하는 핵심 스크립트입니다.  
   - 루트(`/`) 아래 1단계 디렉토리를 찾고, 각 디렉토리에 대해 `extract_extents_by_dir.py`를 병렬로 호출합니다.  
   - 기존 결과 폴더(`extent_output`)와 병합 결과(`file_extent_details.csv`)를 초기화한 뒤, 분석이 모두 끝나면 `merge_extents.py`로 CSV를 하나로 합칩니다.  
   - (선택) `analyze_extents.py`를 호출해 통계/시각화를 실행할 수도 있습니다.

2. **`extract_extents_by_dir.py`**  
   - 주어진 디렉토리(혹은 마운트 지점) 하위 **모든 파일**을 재귀적으로 순회합니다.  
   - 각 파일에 대해 `filefrag -v`를 실행하고, **extent 블록 수**를 파싱한 뒤  
     `파일경로,Extent번호,블록수` 형태의 CSV로 저장합니다.  
   - 권한 문제(`df` 실패), 심볼릭 링크, `filefrag` 오류 등은 자동으로 제외됩니다.

3. **`merge_extents.py`**  
   - 특정 폴더(예: `extent_output`) 내부의 CSV 파일들을 **단일 CSV**로 병합합니다.  
   - `pandas`를 이용해 `pd.concat`으로 합친 뒤, `file_extent_details.csv`(기본값)로 출력합니다.

4. **`analyze_extents.py`** (선택)  
   - 최종 병합 결과(`file_extent_details.csv`)를 로드해, **히스토그램**, **단편화 상위 파일**, **디렉토리별 평균** 등 다양한 통계를 시각화합니다.  
   - `matplotlib`, `seaborn` 등의 라이브러리 활용.

---

## 🚀 사용 방법

1. **의존성 설치**
   ```bash
   sudo apt update
   sudo apt install parallel e2fsprogs
   sudo pip3 install pandas matplotlib seaborn tqdm

2. **권한 설정**
   '''bash
   chmod +x collect_extents_by_dir.sh

3. **nohup으로 실행 (백그라운드에서 동작)**
   '''bash
   sudo nohup ./collect_extents_by_dir.sh > dir_analysis_$(date +%Y%m%d_%H%M%S).log 2>&1 &

   - 로그는 dir_analysis_YYYYMMDD_HHMMSS.log 형태로 저장
   - 병렬 분석 시 터미널을 닫아도 계속 진행됨

4. **결과 파일 확인**

   - 디렉토리별 CSV: extent_output/<hash>.csv
   - 디렉토리 경로를 MD5 해시로 변환한 파일명
   - 병합 결과: file_extent_details.csv

5. **(선택) analyze_extents.py로 분석/시각화**

---

## ⚙️ 스크립트 동작 흐름
   - 이전 결과 정리
   - extent_output 디렉토리와 file_extent_details.csv 파일 삭제
   - 최상위 디렉토리 목록 수집
     '''bash
     find / -mindepth 1 -maxdepth 1 -type d ...
     /home, /var, /usr 등 실제 디렉토리만 가져옴

   /proc, /sys, /dev, /run, /tmp 등은 제외 
   - 병렬 실행
      - parallel로 각 디렉토리에 대해 extract_extents_by_dir.py 호출
   - 디렉토리 경로 → MD5 해시화하여 CSV 이름 충돌 방지
   - CSV 병합
      - merge_extents.py 실행 → file_extent_details.csv 생성

6. **(선택) 분석/시각화**
   - analyze_extents.py로 결과를 그래프로 확인

## 📝 참고 사항
   - 권한: 루트 권한(sudo)이 없으면 일부 파일/디렉토리에 접근이 안 될 수 있습니다.
   - 파일 개수가 매우 많을 경우 분석 시간이 오래 걸 수 있습니다.
   - 심볼릭 링크, 접근 불가 파일, filefrag 오류 파일은 결과에서 제외됩니다.
   - 결과 CSV가 매우 커질 수 있으므로, 필요하면 압축이나 DB 저장을 검토하세요.

---

## 🙏 기여 및 문의
이 파이프라인은 디렉토리 단위 Ext4 extent 분석에 특화된 도구입니다.
추가 기능(조건 필터링, 로그 처리, DB 저장 등)이나 개선 사항이 있다면 언제든 알려주세요!

