from auth import login, register, generate_license_key
from timer import reminder_menu
from utils import start_license_checker

# Основной цикл программы
current_user = None

while True:
    if not current_user:
        print("\nГлавное меню:")
        print("1 - Вход")
        print("2 - Регистрация")
        print("3 - Генерация лицензионного ключа")
        print("4 - Выход")
        action = input("Выберите действие: ")

        if action == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            if login(username, password):
                current_user = username
                start_license_checker(current_user)
        elif action == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            if register(username, password):
                current_user = username
                start_license_checker(current_user)
        elif action == '3':
            duration = int(input("Введите срок действия лицензии (в минутах): "))
            key = generate_license_key(duration)
            print(f"Сгенерированный лицензионный ключ: {key}")
        elif action == '4':
            print("Выход из программы...")
            break  # Завершение программы
        else:
            print("Неверный выбор. Попробуйте снова.")
    else:
        reminder_menu(current_user)
        # После выхода из меню напоминаний сбрасываем текущего пользователя
        current_user = None
        print("Вы вышли из аккаунта.")