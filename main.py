from autocapture import *
from ocr import process_ocr
import time
import re
from datetime import datetime
import pandas as pd


date_pattern = re.compile(r"(\d{1,2}/\d{1,2}|\d+월 \d+일)")

def format_date(date_str):
    try:
        if '/' in date_str:
            return datetime.strptime(f"2024-{date_str}", "%Y-%m/%d").strftime("%Y-%m-%d")

        elif '월' in date_str and '일' in date_str:
            date_tmp = date_str.replace('월', '').replace('일', '').strip()
            return datetime.strptime(f"2024-{date_tmp}", "%Y-%m %d").strftime("%Y-%m-%d")

    except ValueError:
        return "날짜 오류"

data_dict = {}
previous_text = ""

while True:
    capture_img = capture_screenshot()
    text = process_ocr(capture_img).replace('\n', ' ')

    if text == previous_text:
        print("완료")
        break

    split_text = text.split("하셨습니다.")
    print(split_text)

    for individual_data in split_text:
        # 이름
        index = individual_data.find("님께서")
        if index != -1:
            name = individual_data[:index].strip().split()[-1]
        else:
            continue
        print(name)

        # 날짜
        date_match = date_pattern.search(individual_data)
        if date_match:
            date = format_date(date_match.group(0))
            print(date)
        else:
            continue

        # 참석/취소
        if "정모에" in individual_data:
            if name in data_dict:
                if date not in data_dict[name]:
                    data_dict[name].append(date)
            else:
                data_dict[name] = [date]

        elif "취소" in individual_data:
            if name in data_dict and date in data_dict[name]:
                data_dict[name].remove(date)
            else:
                continue

    previous_text = text

    print(data_dict)

    scroll_down()
    time.sleep(0.5)

df = pd.DataFrame([(name, dates) for name, dates in data_dict.items()], columns=['Name', 'Dates'])
print(df)
df.to_csv("attendance_log.csv", index=False)