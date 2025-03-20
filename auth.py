from datetime import datetime, timedelta
from utils import load_csv, save_csv, log_event

# Загрузка данных из CSV
def load_users():
    return load_csv('users.csv')

def load_licenses():
    return load_csv('licenses.csv')

# Сохранение данных в CSV
def save_users(users):
    save_csv('users.csv', users, fieldnames=['username', 'password', 'license_end'])

def save_licenses(licenses):
    save_csv('licenses.csv', licenses, fieldnames=['license_key', 'expiration_date', 'is_used', 'user'])

# Генерация лицензионного ключа
def generate_license_key(duration_minutes):
    import uuid
    license_key = str(uuid.uuid4())
    expiration_date = (datetime.now() + timedelta(minutes=duration_minutes)).strftime("%d.%m.%Y %H:%M:%S")
    licenses = load_licenses()
    licenses.append({
        'license_key': license_key,
        'expiration_date': expiration_date,
        'is_used': 'False',
        'user': ''
    })
    save_licenses(licenses)
    return license_key

# Активация лицензионного ключа
def activate_license_key(username, license_key):
    licenses = load_licenses()
    for license in licenses:
        if license['license_key'] == license_key and license['is_used'] == 'False':
            license['is_used'] = 'True'
            license['user'] = username
            save_licenses(licenses)
            return license['expiration_date']
    return None

# Проверка лицензии пользователя
def check_user_license(username):
    licenses = load_licenses()
    for license in licenses:
        if license['user'] == username:
            expiration_date = datetime.strptime(license['expiration_date'], "%d.%m.%Y %H:%M:%S")
            if datetime.now() < expiration_date:
                return True
    return False

# Регистрация пользователя
def register(username, password):
    users = load_users()
    if any(user['username'] == username for user in users):
        print("Пользователь уже существует.")
        return False
    users.append({
        'username': username,
        'password': password,
        'license_end': ''
    })
    save_users(users)
    log_event(username, "Зарегистрирован новый пользователь")
    return True

# Авторизация пользователя с возможностью продления лицензии
def login(username, password):
    users = load_users()
    user_data = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if user_data:
        if not check_user_license(username):
            print("Ваша лицензия не активирована или истекла.")
            license_key = input("Введите лицензионный ключ для активации или продления: ")
            expiration_date = activate_license_key(username, license_key)
            if expiration_date:
                user_data['license_end'] = expiration_date
                save_users(users)
                log_event(username, f"Лицензия активирована до {expiration_date}")
            else:
                print("Неверный или уже использованный лицензионный ключ.")
                return False
        log_event(username, "Успешный вход в систему")
        return True
    log_event(username, "Ошибка входа в систему", "Неверный логин или пароль")
    return False