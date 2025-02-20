import csv
from datetime import datetime
from collections import defaultdict


# CSV 파일에서 데이터를 읽고 처리하는 메서드
def process_csv(file_path):
    data = []

    # CSV 파일 읽기
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 'Dates' 필드를 리스트로 변환
            row['Dates'] = row['Dates'].strip('[]').replace("'", "").split(", ")
            data.append(row)

    return data

# 월별 참석 데이터를 계산하는 메서드
def calculate_monthly_data(data):
    monthly_data = defaultdict(lambda: defaultdict(list))  # 각 참석자의 월별 참석 날짜 저장
    all_months = set()  # 모든 월을 추적

    for row in data:
        name = row['Name']

        # 날짜 문자열을 datetime 객체로 변환
        try:
            date_list = [datetime.strptime(date, "%Y-%m-%d").date() for date in row['Dates'] if date]
        except ValueError as e:
            print(f"Error processing date: {e}")
            continue

        # 월별 참석 데이터 수집
        for date in date_list:
            month_key = f"{date.year}/{date.month}"  # 월별 키 (예: 2024년 7월)
            all_months.add(month_key)
            monthly_data[name][month_key].append(date.day)  # 참석 날짜(일)만 저장

    # 월별 데이터 정리
    sorted_month_keys = sorted(all_months, key=lambda x: (int(x.split('/')[0]), int(x.split('/')[1])))
    formatted_data = []

    for name, attendance in monthly_data.items():
        row = {'Name': name}
        for month in sorted_month_keys:
            dates = sorted(attendance.get(month, []))  # 날짜를 오름차순 정렬
            row[f"{month} 참석 횟수"] = len(dates)
            row[f"{month} 참석일"] = ', '.join(map(str, dates)) if dates else "-"
        formatted_data.append(row)

    return formatted_data, sorted_month_keys

# 결과를 CSV 파일로 저장하는 메서드
def save_to_csv(file_path, data, months):
    # 필드 정의
    fieldnames = ['Name']
    for month in months:
        fieldnames.append(f"{month} 참석 횟수")
        fieldnames.append(f"{month} 참석일")

    # 이름으로 정렬
    data.sort(key=lambda x: x['Name'])

    # CSV 파일에 쓰기
    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            writer.writerow(row)


# 메인 실행 메서드
def main():
    input_file = 'attendance_log.csv'  # 읽을 CSV 파일
    output_file = 'monthly_attendance_summary.csv'  # 저장할 CSV 파일

    data = process_csv(input_file)
    formatted_data, months = calculate_monthly_data(data)
    save_to_csv(output_file, formatted_data, months)


if __name__ == '__main__':
    main()
