import subprocess
import os


adb_path = r'C:\Users\jhseo\Downloads\platform-tools-latest-windows\platform-tools\adb.exe'
image_folder = "./screenshots-auto"

def capture_screenshot():

    screenshot_name = f"screenshot_tmp.png"
    screenshot_path = os.path.join(image_folder, screenshot_name)

    subprocess.run([adb_path, "shell", "screencap", "-p", f"/sdcard/screenshots_tmp/{screenshot_name}"])
    subprocess.run([adb_path, "pull", f"/sdcard/screenshots_tmp/{screenshot_name}", screenshot_path])

    return screenshot_path

def scroll_down():
    subprocess.run([adb_path, "shell", "input", "swipe", "500", "2300", "500", "400", "1300"])