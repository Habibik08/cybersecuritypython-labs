import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import STUDENT_NAME, GROUP_NAME, VARIANT_NUMBER

def anal_pass():
    passwords = [
        "S0cial@Engineer", "basic", "Phish1ng@D3tect", "client",
        "Ransomwar3@Protect", "general", "Zero@D4y", "generic", 
        "Bug@B0unty", "standard123"
    ]
    criteria = {
        "min_length": 11, 
        "require_digits": True, 
        "require_upper": True,
        "require_special": True
    }
    forbidden_passwords = {"basic", "client", "general", "generic", "standard123", "guest"}
    
    min_len = criteria["min_length"]

    indices = [random.randint(0, len(passwords) - 1) for _ in range(3)]
    for idx in indices:
        passwords.append(passwords[idx])
        
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("-" * 80)
    print(f"{'Пароль':<25} | {'Статус':<15} | {'Довжина':<7} | {'Унікальний'}")
    print("-" * 80)
    
    for p in passwords:
        has_lower = any(c.islower() for c in p)
        has_upper = any(c.isupper() for c in p)
        has_digit = any(c.isdigit() for c in p)
        has_special = any(not c.isalnum() for c in p)
        
        c_count = sum([has_lower, has_upper, has_digit, has_special])
        is_unique = passwords.count(p) == 1
        is_forbidden = p in forbidden_passwords or len(p) < min_len
        
        if is_forbidden:
            status = "Заборонений"
        elif c_count == 4:
            if len(p) >= min_len + 4 and is_unique:
                status = "Дуже сильний"
            else:
                status = "Сильний"
        elif c_count >= 2:
            status = "Середній"
        else:
            status = "Слабкий"
            
        print(f"{p:<25} | {status:<15} | {len(p):<7} | {str(is_unique):<10}")

if __name__ == "__main__":
    anal_pass()