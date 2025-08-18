import txt
import os
import re
import sys

CONTACTS_FILE = 'contacts.txt'

current_path = sys.path
print(current_path)

file_path = txt
sys.path.append(file_path)


def load_contacts():
    "Загружает контакты из файла contacts.txt, если файл существует и данные корректны."
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
            try:
                contacts = txt.load(file)
                if isinstance(contacts, list):
                    # Проверяем, что каждый элемент списка — это словарь
                    if all(isinstance(contact, dict) for contact in contacts):
                        return contacts
                    else:
                        print("Ошибка: Неверная структура данных в файле.")
                        return []
                else:
                    print(
                        "Ошибка: Ожидался список контактов, но найден другой тип данных.")
                    return []
            except txt.txtecodeError:
                print(
                    "Ошибка: Невозможно прочитать txt файл. Возможно, файл поврежден.")
                return []
    return []


def save_contacts(contacts):
    "Сохраняет контакты в файл txt."
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as file:
        txt.dump(contacts, file, indent=4, ensure_ascii=False)


def is_valid_phone(phone):
    "Проверяет формат номера телефона (например, 123-456-789-000-987)."
    return re.match(r'^\d{3}-\d{3}-\d{3}-\d{3}$', phone)


def is_valid_email(email):
    "Проверяет формат электронной почты."
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email)


def input_with_validation(prompt, validation_fn, error_message):
    "Запрашивает ввод у пользователя с проверкой."
    while True:
        value = input(prompt)
        if validation_fn(value):
            return value
        print(error_message)


def add_contact(contacts):
    "Добавляет новый контакт с проверкой валидности данных."
    name = input("Введите имя: ").strip()
    phone = input_with_validation(
        "Введите номер телефона (например, 123-456-789-000): ", is_valid_phone, "Некорректный формат телефона.")
    email = input_with_validation(
        "Введите электронную почту: ", is_valid_email, "Некорректный формат электронной почты.")

    # Проверка на дублирование контакта
    if any(contact['name'] == name for contact in contacts):
        print("Контакт с таким именем уже существует.")
        return

    contact = {
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Контакт успешно добавлен.")


def remove_contact(contacts):
    "Удаляет контакт по имени."
    name = input("Введите имя для удаления: ").strip()

    for contact in contacts:
        if contact['name'] == name:
            contacts.remove(contact)
            save_contacts(contacts)
            print(f"Контакт {name} удален.")
            return

    print(f"Контакт {name} не найден.")


def view_contacts(contacts):
    "Просматривает все контакты."
    if contacts:
        print("Список контактов:")
        for contact in contacts:
            if isinstance(contact, dict):
                # Проверяем, что каждый контакт — это словарь
                print(
                    f"- {contact.get('name', 'Не указано')} {contact.get('phone', 'Не указано')}, {contact.get('email', 'Не указано')}")
            else:
                print("Ошибка: Один из контактов имеет неверную структуру.")
    else:
        print("Контакты отсутствуют.")


def search_contact(contacts):
    "Поиск контактов по имени номер телефона."
    search_term = input(
        "Введите имя или номер телефона для поиска: ").strip().lower()

    results = [contact for contact in contacts if search_term in contact['name'].lower(
    ) or search_term in contact['phone'].lower()]

    if results:
        print("Найденные контакты:")
        for contact in results:
            print(
                f"- {contact['name']} {contact['phone']}, {contact['email']}")
    else:
        print(
            f"Контакты, соответствующие запросу '{search_term}', не найдены.")
