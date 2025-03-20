import csv
import os
import time
import threading
from datetime import datetime


# Загрузка данных из CSV
def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


# Сохранение данных в CSV
def save_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Логирование
def log_event(username, action, error=None):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    if error:
        log_entry = f"[ERROR] [{timestamp}] [{username}] – {action}, {error}"
    else:
        log_entry = f"[INFO] [{timestamp}] [{username}] – {action}"
    with open('log.log', 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')


# Проверка лицензии (фоновый поток)
def start_license_checker(username):
    def check_license():
        users = load_csv('users.csv')
        user_data = next((user for user in users if user['username'] == username), None)

        if not user_data or not user_data['license_end']:
            print("Лицензия не активирована.")
            os._exit(0)

        license_end_time = datetime.strptime(user_data['license_end'], "%d.%m.%Y %H:%M:%S")
        while True:
            if datetime.now() > license_end_time:
                print("Лицензия истекла. Чтобы продолжить работу, приобретите новую лицензию.")
                os._exit(0)
            time.sleep(60)

    threading.Thread(target=check_license).start()