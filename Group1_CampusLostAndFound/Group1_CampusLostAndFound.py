import re
from datetime import datetime

# User Format: [user_id, password, full_name, role]
users = [
    ["02-0000-000001", "pass123", "Sample Student", "Student"],
    ["00-0000-000001", "guard123", "Campus Guard", "Admin"],
    ["admin", "admin123", "System Administrator", "Admin"]
]

# Item Format: [item_id, type, title, category, found_location, claim_location, date, status, reporter_id, is_sensitive]
items = [
    [101, "Found", "Blue Water Bottle", "Personal Items", "Student Center", "Main Guard Post", "15-09-2026", "Unclaimed", "02-0000-000001", False],
    [102, "Found", "PRISAA ID Card (Student)", "Identification", "Engineering Bldg", "SEC Office", "17-09-2026", "Claim Pending", "00-0000-000001", True],
    [103, "Found", "Wallet", "Personal Items", "CL5", "CITE OFFICE", "29-10-2026", "Claim Pending", "00-0000-000001", True],
    [104, "Found", "Logitech Wireless Mouse", "Electronics", "Library 2nd Floor", "Main Guard Post", "18-09-2026", "Unclaimed", "02-0000-000001", False],
    [105, "Found", "Calculus Textbook", "Books", "Admin Building", "SEC Office", "20-09-2026", "Unclaimed", "00-0000-000001", False],
    [106, "Found", "Black USB Flash Drive 32GB", "Electronics", "Computer Lab 2", "CITE Office", "22-09-2026", "Unclaimed", "02-0000-000001", False],
    [107, "Found", "Keys with Red Lanyard", "Personal Items", "Campus Canteen", "Main Guard Post", "25-09-2026", "Returned", "00-0000-000001", False],
    [108, "Found", "Coc School ID Card", "Identification", "Gymnasium", "SEC Office", "28-09-2026", "Unclaimed", "02-0000-000001", True]
]

# System Configuration Settings (Admin Controllable)
system_config = {
    "masking_enabled": True,
    "allow_student_reports": True
}

current_user = None

CATEGORIES = {
    "1": "Electronics",
    "2": "Identification",
    "3": "Personal Items",
    "4": "Books"
}

# Standardized column width formatting string
TABLE_HEADER_FORMAT = "{:<5} | {:<6} | {:<30} | {:<16} | {:<20} | {:<18} | {:<10} | {:<14}"
SEPARATOR_LINE = "=" * 138


def validate_id_format(user_id):
    if user_id.lower() == "admin":
        return True
    if len(user_id) != 14 or user_id[2] != '-' or user_id[7] != '-':
        return False
    parts = user_id.split('-')
    if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        return len(parts[0]) == 2 and len(parts[1]) == 4 and len(parts[2]) == 6
    return False


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def select_category():
    while True:
        print("\nSelect Category:")
        print("[1] Electronics")
        print("[2] Identification")
        print("[3] Personal Items")
        print("[4] Books")
        cat_choice = input("Enter choice (1-4, or 'cancel'): ").strip()
        if cat_choice.lower() == 'cancel':
            return 'cancel'
        if cat_choice in CATEGORIES:
            return CATEGORIES[cat_choice]
        print("[ERROR] Invalid selection! Please select a number from 1 to 4.")


def register_user():
    print("\n--- CREATE NEW STUDENT ACCOUNT ---")
    print("(Type 'cancel' at any prompt to return to menu)")
    
    while True:
        user_id = input("\nEnter Student ID Number (XX-XXXX-XXXXXX): ").strip()
        if user_id.lower() == 'cancel':
            return
        if not validate_id_format(user_id):
            print("[ERROR] Invalid ID format! Example: 01-2345-678901")
            continue
        if any(u[0] == user_id for u in users):
            print("[ERROR] An account with this Student ID already exists!")
            continue
        break

    while True:
        full_name = input("Enter Full Name: ").strip()
        if full_name.lower() == 'cancel':
            return
        if not full_name:
            print("[ERROR] Name cannot be blank.")
            continue
        break

    while True:
        password = input("Enter Password: ").strip()
        if password.lower() == 'cancel':
            return
        if len(password) < 4:
            print("[ERROR] Password must be at least 4 characters long.")
            continue
        break

    users.append([user_id, password, full_name, "Student"])
    print(f"\n[SUCCESS] Account created successfully for {full_name} ({user_id})!")


def login():
    global current_user
    print("\n--- LOGIN ACCOUNT ---")
    print("(Type 'cancel' at any prompt to return to menu)")

    target_user = None
    while True:
        user_id = input("Enter Student/Staff ID Number: ").strip()
        if user_id.lower() == 'cancel':
            return False

        for u in users:
            if u[0] == user_id:
                target_user = u
                break

        if target_user:
            break
        else:
            print("[ERROR] ID Number not found in system! Please try again.\n")

    print(f"\n[ACCOUNT FOUND] Logging in for ID: {target_user[0]} ({target_user[2]})")
    attempts = 3
    
    while attempts > 0:
        password = input(f"Enter Password ({attempts} attempts remaining): ").strip()
        if password.lower() == 'cancel':
            return False

        if target_user[1] == password:
            current_user = target_user
            print(f"\n[SUCCESS] Welcome, {current_user[2]}! (ID: {current_user[0]} | Role: {current_user[3]})")
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"[ERROR] Incorrect password! Please try again.\n")
            else:
                print("\n[SECURITY LOCKOUT] Too many incorrect password attempts! Returning to main menu.")
                return False


def logout():
    global current_user
    if current_user:
        print(f"\n[SUCCESS] Logged out from {current_user[2]}. Goodbye!")
        current_user = None
    else:
        print("\n[INFO] No active user session.")


def report_item(item_type):
    if not current_user:
        print("\n[ERROR] You must be logged in to report an item.")
        return

    if not system_config["allow_student_reports"] and current_user[3] != "Admin":
        print("\n[BLOCKED] Item reporting is currently disabled for students by Administrator.")
        return

    print(f"\n--- REPORT {item_type.upper()} ITEM ---")
    print("(Type 'cancel' at any prompt to return to menu)")

    while True:
        title = input("Enter Item Title/Description: ").strip()
        if title.lower() == 'cancel':
            return
        if not title:
            print("[ERROR] Title cannot be empty.")
            continue
        break

    category = select_category()
    if category == 'cancel':
        return

    location_prompt = "Enter Location Where Item Was Found: " if item_type == "Found" else "Enter Location Where Item Was Lost: "
    while True:
        location = input(location_prompt).strip()
        if location.lower() == 'cancel':
            return
        if not location:
            print("[ERROR] Location cannot be empty.")
            continue
        break

    claim_location = "N/A"
    if item_type == "Found":
        while True:
            claim_location = input("Enter Claim Location (e.g., Guard Post 1 / SEC Office): ").strip()
            if claim_location.lower() == 'cancel':
                return
            if not claim_location:
                print("[ERROR] Claim location cannot be empty.")
                continue
            break

    date_prompt = "Enter Date Found (DD-MM-YYYY, e.g., 22-09-2026): " if item_type == "Found" else "Enter Date Lost (DD-MM-YYYY, e.g., 22-09-2026): "
    while True:
        date = input(date_prompt).strip()
        if date.lower() == 'cancel':
            return
        if not validate_date_format(date):
            print("[ERROR] Invalid date format or non-existent calendar date! Please use DD-MM-YYYY.")
            continue
        break

    while True:
        sensitive_input = input("Is this a sensitive item like an ID/Wallet? (y/n): ").strip().lower()
        if sensitive_input == 'cancel':
            return
        if sensitive_input in ['y', 'n']:
            is_sensitive = (sensitive_input == 'y')
            break
        print("[ERROR] Please answer 'y' or 'n'.")

    new_id = max([i[0] for i in items], default=100) + 1
    items.append([new_id, item_type, title, category, location, claim_location, date, "Unclaimed", current_user[0], is_sensitive])
    print(f"\n[SUCCESS] {item_type} item logged successfully with Item ID: {new_id}")


def print_item_table(item_list, mask_privacy=True):
    print("\n" + SEPARATOR_LINE)
    print(TABLE_HEADER_FORMAT.format("ID", "TYPE", "TITLE / ITEM", "CATEGORY", "LOCATION", "CLAIM AT", "DATE", "STATUS"))
    print(SEPARATOR_LINE)

    for item in item_list:
        item_id, item_type, title, category, location, claim_location, date, status, reporter, is_sensitive = item

        display_title = title
        if mask_privacy and is_sensitive and system_config["masking_enabled"]:
            if not current_user or current_user[3] != "Admin":
                display_title = title[:3] + "****** [PRIVACY]"

        print(TABLE_HEADER_FORMAT.format(item_id, item_type, display_title, category, location, claim_location, date, status))

    print(SEPARATOR_LINE)


def view_and_search_items():
    current_filter = ""
    
    while True:
        print("\n--- VIEW & SEARCH ITEMS ---")
        
        # Display table immediately based on current selected filter
        filtered_items = [i for i in items if not current_filter or current_filter in i[3].lower()]
        
        if filtered_items:
            filter_label = f" (Category: {current_filter.title()})" if current_filter else " (All Items)"
            print(f"CURRENT DATABASE ENTRIES{filter_label}:")
            print_item_table(filtered_items, mask_privacy=True)
        else:
            print("\nNo items matching your criteria were found.")

        # Submenu options right below the table
        print("\nFilter Options:")
        print("[1] Electronics")
        print("[2] Identification")
        print("[3] Personal Items")
        print("[4] Books")
        print("[5] View All Items (Reset Filter)")
        print("[6] Return to Main Menu")
        
        cat_choice = input("Select an option (1-6, or 'cancel'): ").strip()
        
        if cat_choice.lower() == 'cancel' or cat_choice == '6':
            break

        if cat_choice in CATEGORIES:
            current_filter = CATEGORIES[cat_choice].lower()
        elif cat_choice == '5':
            current_filter = ""
        else:
            print("\n[ERROR] Invalid choice! Please select 1-6.")


def update_item_status():
    if not current_user or current_user[3] != "Admin":
        print("\n[ACCESS DENIED] Restricted feature! Only Administrators can update recovery status.")
        return

    print("\n--- [ADMIN] UPDATE ITEM RECOVERY STATUS ---")
    
    if not items:
        print("\n[INFO] No items currently recorded in the system.")
        return

    print("\nCURRENT LOGGED ITEMS:")
    print_item_table(items, mask_privacy=False)

    print("\n(Type 'cancel' to return to main menu)")
    
    target_item = None
    while True:
        raw_input = input("Enter Item ID to update: ").strip()
        if raw_input.lower() == 'cancel':
            return
        
        if not raw_input.isdigit():
            print("[ERROR] Invalid ID! Please enter a numerical Item ID (e.g., 101).")
            continue
            
        target_id = int(raw_input)
        
        for item in items:
            if item[0] == target_id:
                target_item = item
                break
                
        if target_item:
            break
        else:
            print(f"[ERROR] Item ID {target_id} not found in system. Please try again.")

    print(f"\nTarget Item: {target_item[2]}")
    print(f"Current Status: {target_item[7]}")
    print("[1] Unclaimed")
    print("[2] Claim Pending")
    print("[3] Returned / Resolved")
    
    while True:
        choice = input("Select new status (1-3, or 'cancel'): ").strip()
        if choice.lower() == 'cancel':
            return
            
        if choice == '1':
            target_item[7] = "Unclaimed"
            break
        elif choice == '2':
            target_item[7] = "Claim Pending"
            break
        elif choice == '3':
            target_item[7] = "Returned"
            break
        else:
            print("[ERROR] Invalid selection! Please enter 1, 2, or 3.")

    print(f"\n[SUCCESS] Status for Item ID {target_item[0]} updated to '{target_item[7]}' by Admin {current_user[2]}.")

    claimed_items = [i for i in items if i[7] in ["Returned", "Claim Pending"]]
    if claimed_items:
        print("\n--- CLAIMED / RETURNED ITEMS SUMMARY ---")
        print_item_table(claimed_items, mask_privacy=False)


def admin_settings_menu():
    if not current_user or current_user[3] != "Admin":
        print("\n[ACCESS DENIED] Admin privileges required to access System Settings!")
        return

    while True:
        print("\n" + "=" * 45)
        print("     [ADMINISTRATOR CONTROL PANEL]")
        print("=" * 45)
        print(f"1. Toggle Privacy Masking [Current: {'ENABLED' if system_config['masking_enabled'] else 'DISABLED'}]")
        print(f"2. Toggle Student Item Reporting [Current: {'ALLOWED' if system_config['allow_student_reports'] else 'BLOCKED'}]")
        print("3. View Registered System Users")
        print("4. Return to Main Menu")

        choice = input("Select setting option (1-4): ").strip()

        if choice == '1':
            system_config["masking_enabled"] = not system_config["masking_enabled"]
            print(f"\n[CONFIG] Global Privacy Masking set to: {system_config['masking_enabled']}")
        elif choice == '2':
            system_config["allow_student_reports"] = not system_config["allow_student_reports"]
            print(f"\n[CONFIG] Student Item Reporting set to: {system_config['allow_student_reports']}")
        elif choice == '3':
            print("\n--- REGISTERED USERS LIST ---")
            print(f"{'STUDENT ID':<18} | {'FULL NAME':<22} | {'ROLE':<10}")
            print("-" * 58)
            for u in users:
                print(f"{u[0]:<18} | {u[2]:<22} | {u[3]:<10}")
        elif choice == '4':
            break
        else:
            print("\n[ERROR] Invalid choice. Select option 1-4.")


def main_menu():
    while True:
        print("\n" + "=" * 52)
        print("    CAMPUS LOST AND FOUND SYSTEM (PHINMA COC)")
        print("=" * 52)
        user_label = f"{current_user[2]} [{current_user[0]}] ({current_user[3]})" if current_user else "Guest"
        print(f"Logged in as: {user_label}")
        print("----------------------------------------------------")
        print("[1] Register New Student Account")
        print("[2] Login Account")
        print("[3] Report Found Item")
        print("[4] Report Lost Item")
        print("[5] View & Search All Items")
        print("[6] Update Item Status (Admin Only)")
        print("[7] System Settings (Admin Only)")
        print("[8] Logout Current User")
        print("[9] Exit System")

        choice = input("Select an option (1-9): ").strip()

        if choice == '1':
            register_user()
        elif choice == '2':
            login()
        elif choice == '3':
            report_item("Found")
        elif choice == '4':
            report_item("Lost")
        elif choice == '5':
            view_and_search_items()
        elif choice == '6':
            update_item_status()
        elif choice == '7':
            admin_settings_menu()
        elif choice == '8':
            logout()
        elif choice == '9':
            print("\nExiting Campus Lost and Found System. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid choice! Please select 1-9.")


if __name__ == "__main__":
    main_menu()