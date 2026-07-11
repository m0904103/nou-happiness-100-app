import os

files_to_check = [f for f in os.listdir('.') if f.endswith('.html') or f.endswith('.js')]

for file in files_to_check:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    # Replace in order of longest first to avoid partial matches
    content = content.replace("牧野篤教授", "大師")
    content = content.replace("牧野教授", "大師")
    content = content.replace("牧野篤", "大師")
    
    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")

print("Replacement complete.")
