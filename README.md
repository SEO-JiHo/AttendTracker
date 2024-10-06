# 소모임 앱 참석 로그 추출 도구 for Android

소모임 앱에서 정모 참석 로그(운영진만 전체 채팅에서 확인 가능)를 자동으로 캡처하고, OCR을 통해 텍스트를 추출한 후, 해당 텍스트를 처리하여 정모 참석 기록을 CSV 파일로 저장하는 도구입니다.

**Android Debug Bridge**를 사용하여 Android 기기의 스크린샷을 캡처하고, **Tesseract OCR**을 이용해 스크린샷 이미지에서 텍스트를 추출하며, **Pandas**를 사용하여 출석 데이터를 저장하고 처리합니다.

## 목차
1. [설치](#설치)
2. [프로젝트 구조](#프로젝트-구조)
3. [사용법](#사용법)
4. [설정](#설정)
5. [출력 결과](#출력-결과)
6. [발생한 문제와 해결 방법](#발생한-문제와-해결-방법)

---

## 설치

### 사전 요구사항

- **Python 3.8+**
- **Tesseract OCR**
- **ADB (Android Debug Bridge)**

### Python 패키지 설치:

```bash
pip install pytesseract pillow numpy opencv-python pandas
```

### Tesseract OCR 설치:

- [Tesseract installer for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- [그 외 OS](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)

### ADB 설치:
https://source.android.com/docs/setup/build/adb?hl=ko

---

## 프로젝트 구조

```bash
AttendTracker/
│
├── main.py             # 참석 로그 추출을 실행하는 메인 스크립트
├── autocapture.py      # ADB를 사용하여 스크린샷을 캡처하고 스크롤하는 모듈
├── ocr.py              # Tesseract OCR을 사용하여 이미지에서 텍스트를 추출하는 모듈
├── screenshots-auto/   # 스크린샷 파일이 저장되는 폴더
└── attendance_log.csv  # 출석 기록이 저장되는 CSV 파일
```

---

## 사용법

1. **Android 기기 USB 디버그 모드 사용**
   1. 설정 > 휴대전화 정보 > 소프트웨어 정보 > 빌드번호 7회 탭
   2. 설정 > 개발자 옵션 > USB 디버깅 [ON]

2. **Android 기기 연결**: Android 기기를 USB로 PC에 연결한 후 ADB가 연결된 상태인지 확인합니다.
   1. adb.exe 파일이 설치된 경로로 이동 후
   2. "adb devices" 명령어를 입력하여 기기가 올바르게 연결되었는지 확인합니다. (아래 사진에서 "R3CR...(기기명) device"가 떠야합니다.)<br>

  ![image](https://github.com/user-attachments/assets/56a73305-ed86-4ef3-b5c0-a349b9975763)

3. **프로그램 실행**:

```bash
python main.py
```

정상적으로 작동한 경우 `attendance_log.csv` 파일로 저장합니다.

---

## 설정

### 스크린샷 캡처 영역 설정
`ocr.py` 파일에서 스크린샷의 OCR 분석 영역을 조정할 수 있습니다. 아래 코드에서 좌표를 수정하여 원하는 영역을 지정합니다.

```
x_start, y_start, width, height = 200, 450, 800, 2400
```

### 스크롤 동작 설정
`autocapture.py` 파일에서 스크롤 동작을 수행하는 `scroll_down` 함수의 swipe 명령에 있는 숫자는 스크롤할 때의 시작점과 끝점을 나타냅니다.

```
subprocess.run([adb_path, "shell", "input", "swipe", "500", "2300", "500", "400", "1300"])
```
- 첫 번째와 세 번째 숫자: **x 좌표** (500 → 500, 이동하지 않음)
- 두 번와 네 번째 숫자: **y 좌표** (2300 → 1300, 아래에서 위로 swipe, 화면은 아래로 스크롤)
- 다섯 번째 숫자: swipe 속도 (1300ms 동안 스크롤)

---

## 출력 결과

출석 기록은 `attendance_log.csv` 파일에 저장되며, 다음과 같은 형식으로 기록됩니다:

```csv
Name,Dates
멤버1, "['2024-07-05', '2024-08-12']"
멤버2, "['2024-07-01', '2024-09-03']"
...
```

---

## 발생한 문제와 해결 방법

Tesseract와 ADB의 설치 경로를 환경 변수에 추가해도 아래와 같이 에러가 나는 경우

### /system/bin/sh: adb: inaccessible or not found
`ocr.py` 파일의 `process_ocr` 함수에서 Tesseract 실행 파일의 경로를 직접 설정해야 합니다.

```ocr.py
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.
`autocapture.py` 파일에서 adb_path 경로를 직접 설정해야 합니다.

```autocapture.py
adb_path = r'C:\Users\jhseo\Downloads\platform-tools-latest-windows\platform-tools\adb.exe'
```

만약 경로가 정상적으로 설정되었다면 `capture_screenshot` 함수에서 adb_path를 "adb"로 수정하면 됩니다.
