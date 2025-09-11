import csv
import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime


class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert(self, query, values):
        self.cursor.execute(query, values)

    def select_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def read_csv(file_path):
    records = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            mars_date = row[1]
            temp = float(row[2])
            storm = int(row[3])
            records.append((mars_date, temp, storm))
    return records


def save_plot_as_png(data):
    '''데이터를 기반으로 온도 & 폭풍 시각화를 저장합니다.'''
    dates = [row[0] for row in data]  # ✅ 이미 datetime 객체이므로 그대로 사용
    temps = [row[1] for row in data]
    storms = [row[2] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, label='Temperature (°C)', color='orange', marker='o')
    plt.bar(dates, storms, label='Storm Intensity', alpha=0.4, color='blue')
    plt.xlabel('Mars Date')
    plt.ylabel('Temp / Storm')
    plt.title('Mars Weather Overview')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('result.png')
    print('📸 시각화 이미지 저장 완료: result.png')

def main():
    try:
        db = MySQLHelper(
            host='localhost',
            user='root',
            password='dongyang',
            database='mars_db'
        )
        print('✅ DB 연결 성공')

        data = read_csv('mars_weathers_data.csv')
        print(f'📄 CSV 로드 완료: {len(data)}건')

        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )

        for record in data:
            db.insert(query, record)

        db.commit()

        print('✅ 데이터 삽입 완료')

        # 📌 삽입된 전체 데이터 가져오기
        rows = db.select_all('SELECT mars_date, temp, storm FROM mars_weather')
        save_plot_as_png(rows)

        db.close()

    except Exception as e:
        print('❌ 오류 발생:', e)


if __name__ == '__main__':
    main()
