"""Завдання 3: хешування, CSV-база та JSON-логування."""

import hashlib
import csv
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import VARIANT_NUMBER

MIN_LEN = 10


class ValidationError(Exception):
    """Помилка коли пароль коротший за мінімальну довжину."""
    pass


def generate_hash(password, salt="00000"):
    """Робить хеш з пароля і солі."""
    if password is None or password == "" or salt is None or salt == "":
        raise ValueError("пусто")

    if len(password) < MIN_LEN:
        raise ValidationError("пароль короткий")

    text = password + salt
    h = hashlib.sha3_384(text.encode())
    return h.hexdigest()


salt = str(VARIANT_NUMBER)
while len(salt) < 5:
    salt = "0" + salt


def create_user(username, password):
    """Створює одного користувача (логін, хеш)."""
    hash_val = generate_hash(password, salt)
    return (username, hash_val)


users_to_register = [
    ("iot_specialist", "IoTSecureP@ss1"),
    ("mobile_analyst", "MobileD3fend!"),
    ("web_developer", "WebDevStr0ng#"),
    ("api_consumer", "ApiGateway@2023"),
    ("demo_account", "DemoAccessKey1"),
    ("network_admin", "NetAdminP@ss99"),
    ("security_auditor", "AuditTrail#456"),
    ("junior_dev", "JuniorC0de@Dev"),
    ("support_agent", "SupportDesk!12"),
    ("ops_engineer", "OpsEngine@r001")
]


def create_users(users_list):
    """Записує список користувачів у CSV-файл."""
    if not os.path.exists("data"):
        os.makedirs("data")

    with open("data/users.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for u in users_list:
            try:
                row = create_user(u[0], u[1])
                writer.writerow(row)
            except ValidationError as e:
                print("пропускаю", u[0], e)


def read_users():
    """Читає CSV-базу користувачів у словник."""
    result = {}
    try:
        with open("data/users.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    result[row[0]] = row[1]
    except FileNotFoundError:
        print("файл не найден")
    return result


def log_event(func):
    """Декоратор, що логує спроби входу у JSON-файл."""
    def wrapper(username, password):
        try:
            res = func(username, password)
            if res:
                result = "success"
            else:
                result = "failure"
        except (ValueError, ValidationError):
            result = "failure"
            res = None

        entry = {}
        entry["event"] = "login"
        entry["user"] = username
        entry["result"] = result
        entry["timestamp"] = str(datetime.now())
        entry["args"] = []
        entry["kwargs"] = {}

        if not os.path.exists("data"):
            os.makedirs("data")

        logs = []
        if os.path.exists("data/log.json"):
            with open("data/log.json", "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []

        logs.append(entry)

        with open("data/log.json", "w", encoding="utf-8") as f:
            json.dump(logs, f)

        return res
    return wrapper


@log_event
def login(username, password):
    """Перевіряє логін і пароль користувача."""
    if username == "" or password == "":
        raise ValueError("логін/пароль пусті")

    db = read_users()

    if username not in db:
        return False

    check_hash = generate_hash(password, salt)

    if db[username] == check_hash:
        return True
    else:
        return False


def main():
    """Запускає весь сценарій завдання 3."""
    create_users(users_to_register)

    db = read_users()
    print("База користувачів:")
    for login_name in db:
        print(login_name, db[login_name])

    print("")
    print("Логін тест:")

    r1 = login("iot_specialist", "IoTSecureP@ss1")
    print("iot_specialist правильний пароль:", r1)

    r2 = login("iot_specialist", "неправильний")
    print("iot_specialist неправильний пароль:", r2)


if __name__ == "__main__":
    main()