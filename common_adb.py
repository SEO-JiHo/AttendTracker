import subprocess
import time
import xml.etree.ElementTree as ET

adb_path = r"C:\Users\jhseo\Downloads\platform-tools\adb.exe"
xml_path_phone = "/sdcard/ui_dump.xml"
xml_path_local = "./ui_dump.xml"


def run_adb(args, capture=False):
    cmd = [adb_path] + args
    if capture:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()
    else:
        subprocess.run(cmd, check=True)


def get_ui_dump():
    run_adb(["shell", "uiautomator", "dump", xml_path_phone])
    run_adb(["pull", xml_path_phone, xml_path_local])


def parse_ui_texts():
    tree = ET.parse(xml_path_local)
    root = tree.getroot()
    texts = []
    for node in root.iter("node"):
        text = node.attrib.get("text", "").strip()
        if text:
            texts.append(text)
    return texts


def scroll_down():
    run_adb(["shell", "input", "swipe", "500", "2000", "500", "1000", "280"])
    time.sleep(0.3)
