from common_adb import *
import pandas as pd
import re

print("start extracting member names...")

members = set()
previous_texts = set()

while True:
    get_ui_dump()
    texts = parse_ui_texts()

    for i, t in enumerate(texts):
        if "가입" in t or "•" in t:
            if i > 0:
                name = texts[i - 1].strip()
                if re.match(r"^[가-힣]{2,4}$", name):
                    members.add(name)

    if set(texts) == previous_texts:
        print("done.")
        break

    previous_texts = set(texts)
    scroll_down()


df = pd.DataFrame(sorted(members), columns=["Name"])
# df.to_csv("members.csv", index=False, encoding="utf-8-sig")

# print(f"✅ 총 {len(members)}명 저장 완료 → members.csv")

df.to_csv("tmp.csv", index=False, encoding="utf-8-sig")
