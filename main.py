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
    "Проверяет формат номера телефона (например, 123-456-789-000)."
    return re.match(r'^\d{3}-\d{3}-\d{3}-\d{3}$', phone)
