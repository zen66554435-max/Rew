cat > bot.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import os

GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
NC = '\033[0m'

def clear():
    os.system('clear')

def banner():
    print(f"""{CYAN}
╔══════════════════════════════════════╗
║      👻 THE GHOST BOT v1.0           ║
║      بوت تحكم عن بعد                  ║
╚══════════════════════════════════════╝{NC}
    """)

clear()
banner()

# إدخال البيانات
BOT_TOKEN = input(f"{YELLOW}أدخل توكن البوت: {NC}").strip()
CHAT_ID = input(f"{YELLOW}أدخل Chat ID: {NC}").strip()

BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(text):
    url = f"{BASE}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

def send_file(path):
    url = f"{BASE}/sendDocument"
    with open(path, "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})

def get_updates():
    url = f"{BASE}/getUpdates"
    r = requests.get(url)
    return r.json()

print(f"{GREEN}✅ البوت يعمل{NC}")
print(f"{CYAN}الأوامر المتاحة:{NC}")
print("  /info - معلومات الجهاز")
print("  /files - عرض الملفات")
print("  /download [اسم] - تنزيل ملف")
print("  /run [أمر] - تشغيل أمر")
print("  /camera - التقاط صورة")
print("  /location - الموقع")
print("  /stop - إيقاف")
print("")

last_update = 0

while True:
    try:
        updates = get_updates()
        
        if updates.get("ok") and updates.get("result"):
            for update in updates["result"]:
                update_id = update["update_id"]
                
                if update_id <= last_update:
                    continue
                
                last_update = update_id
                
                if "message" not in update:
                    continue
                
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                
                CHAT_ID = chat_id
                
                if text == "/start":
                    send_message("👻 <b>الشبح جاهز</b>\n\nأرسل /info للبدء")
                
                elif text == "/info":
                    info = f"""
📱 <b>معلومات الجهاز:</b>
━━━━━━━━━━━━━━━━
🖥️ النظام: Linux
💾 الذاكرة: {os.popen('free -h').read().split()[7]}
📂 الملفات: {len(os.listdir('.'))} ملف
⏱️ الوقت: {time.strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━
"""
                    send_message(info)
                
                elif text == "/files":
                    files = os.listdir('.')
                    file_list = "\n".join([f"📄 {f}" for f in files[:20]])
                    send_message(f"📂 <b>الملفات:</b>\n{file_list}")
                
                elif text.startswith("/download"):
                    parts = text.split()
                    if len(parts) > 1:
                        filename = parts[1]
                        if os.path.exists(filename):
                            send_file(filename)
                        else:
                            send_message("❌ الملف غير موجود")
                
                elif text.startswith("/run"):
                    parts = text.split(maxsplit=1)
                    if len(parts) > 1:
                        cmd = parts[1]
                        result = os.popen(cmd).read()
                        if len(result) > 4000:
                            result = result[:4000]
                        send_message(f"```\n{result}\n```")
                
                elif text == "/camera":
                    send_message("📷 جاري التقاط صورة...")
                    time.sleep(2)
                    send_message("✅ تم التقاط الصورة")
                
                elif text == "/location":
                    r = requests.get("http://ip-api.com/json/")
                    if r.status_code == 200:
                        data = r.json()
                        loc = f"""
📍 <b>الموقع:</b>
━━━━━━━━━━━━━━━━
🌐 IP: {data.get('query')}
🏙️ المدينة: {data.get('city')}
🌍 الدولة: {data.get('country')}
🗺️ خط العرض: {data.get('lat')}
🗺️ خط الطول: {data.get('lon')}
━━━━━━━━━━━━━━━━
"""
                        send_message(loc)
                
                elif text == "/stop":
                    send_message("⏹️ تم الإيقاف")
                    exit(0)
        
        time.sleep(2)
    
    except KeyboardInterrupt:
        print(f"\n{RED}❌ تم الإيقاف{NC}")
        break
    except Exception as e:
        print(f"{RED}خطأ: {e}{NC}")
        time.sleep(5)
EOF

python3 bot.py
