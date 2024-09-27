# 1. ADB를 이용하여 자동으로 화면 캡처
# 2. 캡처 이미지 OCR 처리 및 데이터 추출
#   2-1. OCR
#   2-2. 데이터 추출
#       'ㅇㅇㅇ님께서', '참석하셨습니다.', '참석을 취소하셨습니다.'
#       9/26 == 9월 26일
#       전체 멤버 -> pandas.Dataframe
import subprocess
import os
import time
from ocr import process_ocr

adb_path = r'C:\Users\jhseo\Downloads\platform-tools-latest-windows\platform-tools\adb.exe'
image_folder = "./screenshots-auto"

def capture_screenshot(counter):

    screenshot_name = f"screenshot_{counter}.png"
    screenshot_path = os.path.join(image_folder, screenshot_name)

    subprocess.run([adb_path, "shell", "screencap", "-p", f"/sdcard/screenshots_tmp/{screenshot_name}"])
    subprocess.run([adb_path, "pull", f"/sdcard/screenshots_tmp/{screenshot_name}", screenshot_path])

    return screenshot_path

def scroll_down():
    subprocess.run([adb_path, "shell", "input", "swipe", "500", "2300", "500", "400", "1100"])


for i in range(3):
    extrtacted_data = capture_screenshot(1)
    print(process_ocr(extrtacted_data))
    scroll_down()
    time.sleep(0.5)