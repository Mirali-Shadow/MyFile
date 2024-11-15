import json

# تابع برای ایجاد فایل JSON در صورت نبودن
def create_file_if_not_exists(file_path="file.json"):
    try:
        with open(file_path, "r") as f:
            json.load(f)
    except FileNotFoundError:
        print("Creating new JSON file...")
        with open(file_path, "w") as f:
            json.dump({"files": []}, f, indent=4)

# تابع برای گرفتن لینک فایل از فایل JSON
def get_file_link_from_json(command, file_path="file.json"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # بررسی اینکه داده‌ها یک دیکشنری و شامل لیست "files" هستند
        if isinstance(data, dict) and "files" in data:
            for item in data["files"]:
                if item.get("command") == command:
                    if "file_id" in item:
                        return item["file_id"]
                    else:
                        print(f"Warning: 'file_id' key not found for command: {command}")
                        return None
        return None
    except FileNotFoundError:
        print("JSON file not found!")
        return None
    
# تابع برای اضافه کردن فایل به فایل JSON
def add_file_to_json(command, url, file_path="file.json"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        data["files"].append({"command": command, "url": url})
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"File added: {command} -> {url}")
    except FileNotFoundError:
        print("JSON file not found, creating a new one...")
        with open(file_path, "w") as f:
            json.dump({"files": [{"command": command, "url": url}]}, f, indent=4)
        print(f"File added: {command} -> {url}")
