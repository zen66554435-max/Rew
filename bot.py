#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import string
import os
import time
import threading
import requests

# ============ الألوان ============
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
NC = '\033[0m'

# ============ متغيرات عامة ============
stop_flag = False
counter = 0
start_time = 0
generating = False

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    print(f"""
{CYAN}╔══════════════════════════════════════════════╗
║      🔐 DMARFOT Wordlist Generator v2.0        ║
║         توليد كلمات المرور وإرسالها للبوت      ║
╚══════════════════════════════════════════════╝{NC}
    """)

# ============ إدخال البيانات ============
clear_screen()
print_banner()

print(f"{YELLOW}[1/3] إعدادات البوت:{NC}")
print("-" * 45)
BOT_TOKEN = input(f"{WHITE}أدخل توكن البوت: {NC}").strip()
CHAT_ID = input(f"{WHITE}أدخل Chat ID (أو اتركه فاضي للتلقائي): {NC}").strip()

print("")
print(f"{YELLOW}[2/3] إعدادات التوليد:{NC}")
print("-" * 45)

while True:
    try:
        PASSWORD_LENGTH = int(input(f"{WHITE}طول كلمة المرور (1-15): {NC}").strip())
        if 1 <= PASSWORD_LENGTH <= 15:
            break
        print(f"{RED}❌ الطول بين 1 و 15{NC}")
    except:
        print(f"{RED}❌ رقم غير صحيح{NC}")

print("")
print(f"{CYAN}اختر نوع الحروف:{NC}")
print("  1) أرقام فقط (0-9)")
print("  2) أحرف صغيرة (a-z)")
print("  3) أحرف كبيرة (A-Z)")
print("  4) أحرف صغيرة + أرقام")
print("  5) أحرف كبيرة + أرقام")
print("  6) أحرف صغيرة + كبيرة")
print("  7) أحرف + أرقام (كامل)")
print("  8) أحرف + أرقام + رموز")
print("  9) حروف مخصصة")

while True:
    choice = input(f"{WHITE}اختيارك: {NC}").strip()
    
    options = {
        "1": (string.digits, "أرقام"),
        "2": (string.ascii_lowercase, "أحرف صغيرة"),
        "3": (string.ascii_uppercase, "أحرف كبيرة"),
        "4": (string.ascii_lowercase + string.digits, "أحرف صغيرة + أرقام"),
        "5": (string.ascii_uppercase + string.digits, "أحرف كبيرة + أرقام"),
        "6": (string.ascii_lowercase + string.ascii_uppercase, "أحرف صغيرة + كبيرة"),
        "7": (string.ascii_lowercase + string.ascii_uppercase + string.digits, "أحرف + أرقام"),
        "8": (string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*", "أحرف + أرقام + رموز"),
    }
    
    if choice in options:
        CHARSET, CHARSET_NAME = options[choice]
        break
    elif choice == "9":
        CHARSET = input(f"{WHITE}أدخل الحروف: {NC}").strip()
        CHARSET_NAME = f"مخصص: {CHARSET}"
        break
    else:
        print(f"{RED}❌ خيار خاطئ{NC}")

TOTAL = len(CHARSET) ** PASSWORD_LENGTH

print("")
print(f"{YELLOW}[3/3] خيارات إضافية:{NC}")
print("-" * 45)

# حجم الملف التقديري
est_size = TOTAL * (PASSWORD_LENGTH + 1) / (1024 * 1024)
print(f"{CYAN}📊 الحجم المتوقع للملف: {est_size:.2f} MB{NC}")

# تقسيم الملف
split_choice = input(f"{WHITE}تقسيم الملف لعدة أجزاء؟ (y/n): {NC}").strip().lower()
if split_choice == 'y':
    SPLIT_SIZE = int(input(f"{WHITE}حجم كل جزء (MB): {NC}").strip())
else:
    SPLIT_SIZE = 0

print("")
print("=" * 45)
print(f"{GREEN}📋 ملخص:{NC}")
print(f"   🔑 التوكن: {BOT_TOKEN[:15]}...")
if CHAT_ID:
    print(f"   🆔 Chat ID: {CHAT_ID}")
else:
    print(f"   🆔 Chat ID: تلقائي")
print(f"   📏 الطول: {PASSWORD_LENGTH}")
print(f"   🔤 الحروف: {CHARSET_NAME}")
print(f"   📊 العدد: {TOTAL:,}")
if SPLIT_SIZE:
    print(f"   📦 التقسيم: {SPLIT_SIZE} MB لكل جزء")
print("=" * 45)
print("")

confirm = input(f"{WHITE}ابدأ التوليد؟ (y/n): {NC}").strip().lower()
if confirm != 'y':
    print(f"{RED}❌ إلغاء{NC}")
    exit()

# ============ دوال البوت ============
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=10)
        return r.json()
    except:
        return None

def send_file(chat_id, file_path, caption=""):
    url = f"{BASE_URL}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            r = requests.post(url, data={"chat_id": chat_id, "caption": caption}, files={"document": f}, timeout=60)
        return r.json()
    except:
        return None

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        r = requests.get(url, timeout=15)
        return r.json()
    except:
        return None

def get_me():
    url = f"{BASE_URL}/getMe"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return None

def get_chat_id():
    # محاولة الحصول على chat_id من آخر رسالة
    updates = get_updates()
    if updates and updates.get("ok") and updates.get("result"):
        for update in reversed(updates["result"]):
            if "message" in update:
                return update["message"]["chat"]["id"]
            elif "callback_query" in update:
                return update["callback_query"]["message"]["chat"]["id"]
    return None

# ============ التحقق من البوت ============
print(f"{CYAN}📡 التحقق من البوت...{NC}")
bot_info = get_me()
if bot_info and bot_info.get("ok"):
    bot_name = bot_info["result"]["username"]
    print(f"{GREEN}✅ البوت متصل: @{bot_name}{NC}")
else:
    print(f"{RED}❌ فشل الاتصال بالبوت — تأكد من التوكن{NC}")
    exit(1)

# ============ الحصول على Chat ID ============
if not CHAT_ID:
    print(f"{YELLOW}📡 جاري الحصول على Chat ID تلقائياً...{NC}")
    print(f"{YELLOW}⚠️ أرسل أي رسالة للبوت الآن...{NC}")
    
    for i in range(30):
        CHAT_ID = get_chat_id()
        if CHAT_ID:
            print(f"{GREEN}✅ تم الحصول على Chat ID: {CHAT_ID}{NC}")
            break
        time.sleep(1)
    
    if not CHAT_ID:
        print(f"{RED}❌ لم يتم العثور على محادثة — أرسل /start للبوت أولاً{NC}")
        exit(1)

# ============ التوليد ============
OUTPUT_FILE = f"wordlist_{PASSWORD_LENGTH}_{int(time.time())}.txt"

def update_progress():
    global counter, start_time
    
    elapsed = time.time() - start_time
    speed = int(counter / elapsed) if elapsed > 0 else 0
    progress = (counter / TOTAL * 100) if TOTAL > 0 else 0
    
    eta = int((TOTAL - counter) / speed) if speed > 0 else 0
    
    sys_msg = f"\r{CYAN}📊 {counter:,}/{TOTAL:,} | ⚡ {speed:,}/ث | 📈 {progress:.2f}% | ⏱️ {int(elapsed)}ث | ⏳ متبقي: {eta}ث{NC}"
    
    sys.stdout.write(sys_msg)
    sys.stdout.flush()

def generate_words():
    global counter, start_time, generating
    
    generating = True
    counter = 0
    start_time = time.time()
    
    with open(OUTPUT_FILE, "w") as f:
        for combo in itertools.product(CHARSET, repeat=PASSWORD_LENGTH):
            if stop_flag:
                break
            
            f.write("".join(combo) + "\n")
            counter += 1
            
            if counter % 50000 == 0:
                update_progress()
    
    generating = False

print("")
print(f"{GREEN}🔑 بدء التوليد...{NC}")
print(f"{CYAN}📁 الملف: {OUTPUT_FILE}{NC}")
print("")

# تشغيل التوليد في خيط منفصل
gen_thread = threading.Thread(target=generate_words)
gen_thread.start()

# مراقبة
while gen_thread.is_alive():
    if counter % 50000 != 0:
        time.sleep(0.1)
    time.sleep(0.5)

elapsed = time.time() - start_time
speed = int(counter / elapsed) if elapsed > 0 else 0
file_size = os.path.getsize(OUTPUT_FILE)
file_size_mb = file_size / (1024 * 1024)

print("")
print("")
print(f"{GREEN}=" * 45)
print(f"✅ اكتمل التوليد!")
print(f"-" * 45)
print(f"   📊 العدد: {counter:,}")
print(f"   📦 الحجم: {file_size_mb:.2f} MB")
print(f"   ⏱️ الوقت: {int(elapsed)} ثانية")
print(f"   ⚡ السرعة: {speed:,} كلمة/ثانية")
print(f"=" * 45{NC}")
print("")

# ============ الإرسال ============
print(f"{CYAN}📤 جاري الإرسال إلى البوت...{NC}")

if SPLIT_SIZE > 0:
    # تقسيم الملف
    split_size_bytes = SPLIT_SIZE * 1024 * 1024
    part_num = 1
    
    with open(OUTPUT_FILE, "r") as f:
        while True:
            lines = f.readlines(split_size_bytes)
            if not lines:
                break
            
            part_file = f"{OUTPUT_FILE}.part{part_num}"
            with open(part_file, "w") as pf:
                pf.writelines(lines)
            
            part_size = os.path.getsize(part_file) / (1024 * 1024)
            caption = f"📦 جزء {part_num} | الحجم: {part_size:.2f} MB"
            
            print(f"{YELLOW}📤 إرسال الجزء {part_num}...{NC}")
            result = send_file(CHAT_ID, part_file, caption)
            
            if result and result.get("ok"):
                print(f"{GREEN}✅ تم إرسال الجزء {part_num}{NC}")
            else:
                print(f"{RED}❌ فشل إرسال الجزء {part_num}: {result}{NC}")
            
            os.remove(part_file)
            part_num += 1
else:
    # إرسال كامل
    caption = f"""
✅ <b>اكتمل التوليد</b>

📊 <b>العدد:</b> {counter:,}
📏 <b>الطول:</b> {PASSWORD_LENGTH}
🔤 <b>الحروف:</b> {CHARSET_NAME}
📦 <b>الحجم:</b> {file_size_mb:.2f} MB
⏱️ <b>الوقت:</b> {int(elapsed)} ثانية
⚡ <b>السرعة:</b> {speed:,}/ثانية
"""
    
    result = send_file(CHAT_ID, OUTPUT_FILE, caption)
    if result and result.get("ok"):
        print(f"{GREEN}✅ تم إرسال الملف بنجاح!{NC}")
    else:
        print(f"{RED}❌ فشل الإرسال: {result}{NC}")
        print(f"{YELLOW}💡 الملف محفوظ محلياً: {OUTPUT_FILE}{NC}")

print("")
print(f"{GREEN}🎉 تم كل شيء!{NC}")
print(f"{CYAN}📁 الملف: {OUTPUT_FILE}{NC}")
