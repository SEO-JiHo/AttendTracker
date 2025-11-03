from common_adb import *
import pandas as pd
import re
from datetime import datetime

print("start extracting attendance data...")

members_df = pd.read_csv("members.csv")
members = list(members_df["Name"])

date_pattern = re.compile(r"(\d{1,2}/\d{1,2}|\d+월\s*\d+일)")

def format_date(date_str):
    try:
        if '/' in date_str:
            return datetime.strptime(f"{date_str}", "%m/%d").strftime("%m-%d")
        elif '월' in date_str and '일' in date_str:
            clean = date_str.replace('월', '').replace('일', '').strip()
            return datetime.strptime(f"{clean}", "%m %d").strftime("%m-%d")
    except ValueError:
        return None

attendance = {name: set() for name in members}
previous_texts = set()

while True:
    get_ui_dump()
    texts = parse_ui_texts()

    if set(texts) == previous_texts:
        print("done.")
        break
    previous_texts = set(texts)

    combined_text = " ".join(texts)
    split_segments = re.split(r"하셨습니다\.?", combined_text)

    for seg in split_segments:
        for name in members:
            if name in seg:
                date_match = date_pattern.search(seg)
                if not date_match:
                    continue
                date = format_date(date_match.group(0))
                if not date:
                    continue

                if "정모에" in seg or "참석하" in seg:
                    attendance[name].add(date)
                elif "취소" in seg:
                    if date in attendance[name]:
                        attendance[name].remove(date)

    scroll_down()

records = []
for name in members:
    dates = sorted(list(attendance.get(name, [])))
    count = len(dates)
    records.append((name, ", ".join(dates), count))

df = pd.DataFrame(records, columns=["Name", "Dates", "Count"])
df.to_csv("attendance_log.csv", index=False, encoding="utf-8-sig")

print(f"\ndone❗ → attendance_log.csv")
print(df)
