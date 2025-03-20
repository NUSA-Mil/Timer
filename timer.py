import time
import threading
from utils import load_csv, save_csv, log_event


# Создание напоминания
def create_reminder(username):
    event = input("Введите событие для напоминания: ")
    duration = int(input("Введите время до напоминания (в секундах): "))

    def reminder():
        time.sleep(duration)
        print(f"Напоминание: {event}")
        log_event(username, f"Напоминание: {event}")

    threading.Thread(target=reminder).start()

    reminders = load_csv('reminders.csv')
    reminders.append({
        'username': username,
        'event': event,
        'duration': str(duration)
    })
    save_csv('reminders.csv', reminders, fieldnames=['username', 'event', 'duration'])
    print("Напоминание успешно создано!")


# Просмотр списка напоминаний
def view_reminders(username):
    reminders = load_csv('reminders.csv')
    user_reminders = [reminder for reminder in reminders if reminder['username'] == username]

    if not user_reminders:
        print("У вас нет активных напоминаний.")
        return

    print("Ваши напоминания:")
    for i, reminder in enumerate(user_reminders, 1):
        print(f"{i}. Событие: {reminder['event']}, Время до напоминания: {reminder['duration']} сек.")


# Удаление напоминания
def delete_reminder(username):
    reminders = load_csv('reminders.csv')
    user_reminders = [reminder for reminder in reminders if reminder['username'] == username]

    if not user_reminders:
        print("У вас нет активных напоминаний.")
        return

    view_reminders(username)
    try:
        index = int(input("Введите номер напоминания для удаления: ")) - 1
        if 0 <= index < len(user_reminders):
            reminders.remove(user_reminders[index])
            save_csv('reminders.csv', reminders, fieldnames=['username', 'event', 'duration'])
            print("Напоминание успешно удалено!")
        else:
            print("Неверный номер напоминания.")
    except ValueError:
        print("Введите корректный номер.")


# Меню управления напоминаниями
def reminder_menu(username):
    while True:
        print("\nМеню напоминаний:")
        print("1. Создать напоминание")
        print("2. Просмотреть напоминания")
        print("3. Удалить напоминание")
        print("4. Выйти из аккаунта")
        choice = input("Выберите действие: ")

        if choice == '1':
            create_reminder(username)
        elif choice == '2':
            view_reminders(username)
        elif choice == '3':
            delete_reminder(username)
        elif choice == '4':
            print("Выход из аккаунта...")
            break  # Выход из меню напоминаний
        else:
            print("Неверный выбор. Попробуйте снова.")