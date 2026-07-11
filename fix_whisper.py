import json

with open("karaoke_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

replacements = {
    "熟悉課程": "暑期課程",
    "光芒樓": "光芒喔",
    "碟碟撞撞": "跌跌撞撞",
    "經體之力": "晶體智力",
    "流體之力": "流體智力",
    "震散發著": "正散發著",
    "公幹": "共感",
    "微笑的": "微小的",
    "空調的中心": "那空掉的中心",
    "恩怒": "恩送",
    "未來的時代": "未來的世代",
    "轉遞": "傳遞"
}

for segment in data["segments"]:
    for old, new in replacements.items():
        segment["text"] = segment["text"].replace(old, new)

with open("karaoke_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON Fixed successfully")
