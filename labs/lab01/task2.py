import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.student import STUDENT_NAME, GROUP_NAME, VARIANT_NUMBER

def check_access():
    users = {
        "iot_specialist": {"role": "iot_security", "clearance": 3, "department": "IoT", "active": True},
        "mobile_analyst": {"role": "mobile_security", "clearance": 3, "department": "Mobile", "active": True},
        "web_developer": {"role": "web_developer", "clearance": 2, "department": "Web", "active": True},
        "api_consumer": {"role": "api_user", "clearance": 2, "department": "Integration", "active": True},
        "demo_account": {"role": "demonstration", "clearance": 1, "department": "Demo", "active": False}
    }
    
    resources = [
        ("iot_firmware", 3), ("mobile_policies", 3), ("web_applications", 2),
        ("api_gateway", 2), ("device_certificates", 3), ("app_store", 1),
        ("vulnerability_database", 3), ("device_management", 3),
        ("integration_docs", 2), ("demo_content", 1)
    ]
    
    security_levels = ("Consumer", "Business", "Enterprise", "Critical Systems")
    blocked_users = {"demo_account", "compromised_device", "malicious_app"}

    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("-" * 80)
    print("Список ресурсів системи:")
    for res_name, res_level in resources:
        level_name = security_levels[res_level - 1]
        print(f"- {res_name}: {level_name}")
    
    print("-" * 80)
    print("Результати перевірки доступу:")
    
    test_users = list(users.keys()) + [u for u in blocked_users if u not in users] + ["unknown_hacker"]

    for user in test_users:
        for res_name, res_level in resources:
            if user not in users:
                print(f"user={user} resource={res_name} -> DENY (User not found)")
                continue
            
            if user in blocked_users:
                print(f"user={user} resource={res_name} -> DENY (User is blocked)")
                continue
            
            if not users[user].get("active", False):
                print(f"user={user} resource={res_name} -> DENY (Account inactive)")
                continue
            
            if users[user].get("clearance", 0) >= res_level:
                print(f"user={user} resource={res_name} -> ALLOW")
            else:
                print(f"user={user} resource={res_name} -> DENY (Insufficient clearance)")

if __name__ == "__main__":
    check_access()