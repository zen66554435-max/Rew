#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import string
import os
import time
import sys
from telethon import TelegramClient

# ============ الواجهة العربية ============
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    print("""
╔══════════════════════════════════════════╗
║      🔐 أداة توليد كلمات المرور          ║
║         Telegram Wordlist Generator       ║
╚══════════════════════════════════════════╝
    """)

# ============ إدخال البيانات ============
clear_screen()
print_banner()

print("[1/3] إعدادات البوت:")
print("-" * 40)
BOT_TOKEN = input("أدخل توكن البوت: ").strip()
API_ID = int(input("أدخل API ID: ").strip())
API_HASH = input("أدخل API HASH: ").strip()

print("")
print("[2/3] إعدادات التوليد:")
print("-" * 40)

# طول كلمة المرور
while True:
    try:
        PASSWORD_LENGTH = int(input("أدخل طول كلمة المرور (1-12): ").strip())
        if 1 <= PASSWORD_LENGTH <= 12:
            break
        print("❌ الطول بين 1 و 12")
    except:
        print("❌ رقم غير صحيح")

print("")
print("اختر نوع الحروف:")
print("1) أحرف صغيرة فقط (a-z)")
print("2) أحرف كبيرة فقط (A-Z)")
print("3) أرقام فقط (0-9)")
print("4) أحرف صغيرة + أرقام")
print("5) أحرف كبيرة + أرقام")
print("6) أحرف صغيرة + كبيرة")
print("7) أحرف صغيرة + كبيرة + أرقام")
print("8) كل شيء + رموز")
print("9) حروف مخصصة")

while True:
    choice = input("اختيارك: ").strip()
    
    if choice == "1":
        CHARSET = string.ascii_lowercase
        CHARSET_NAME = "أحرف صغيرة"
        break
    elif choice == "2":
        CHARSET = string.ascii_uppercase
        CHARSET_NAME = "أحرف كبيرة"
        break
    elif choice == "3":
        CHARSET = string.digits
        CHARSET_NAME = "أرقام"
        break
    elif choice == "4":
        CHARSET = string.ascii_lowercase + string.digits
        CHARSET_NAME = "أحرف صغيرة + أرقام"
        break
    elif choice == "5":
        CHARSET = string.ascii_uppercase + string.digits
        CHARSET_NAME = "أحرف كبيرة + أرقام"
        break
    elif choice == "6":
        CHARSET = string.ascii_lowercase + string.ascii_uppercase
        CHARSET_NAME = "أحرف صغيرة + كبيرة"
        break
    elif choice == "7":
        CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits
        CHARSET_NAME = "أحرف صغيرة + كبيرة + أرقام"
        break
    elif choice == "8":
        CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        CHARSET_NAME = "كل شيء + رموز"
        break
    elif choice == "9":
        CHARSET = input("أدخل الحروف المخصصة: ").strip()
        CHARSET_NAME = f"مخصص: {CHARSET}"
        break
    else:
        print("❌ خيار خاطئ")

TOTAL_COMBINATIONS = len(CHARSET) ** PASSWORD_LENGTH

print("")
print("[3/3] إعدادات الإرسال:")
print("-" * 40)
print("سيتم إرسال الملف تلقائياً على البوت بعد الانتهاء")

print("")
print("=" * 40)
print("📋 ملخص الإعدادات:")
print("-" * 40)
print(f"🔑 التوكن: {BOT_TOKEN[:10]}...")
print(f"🆔 API ID: {API_ID}")
print(f"📏 طول الكلمة: {PASSWORD_LENGTH}")
print(f"🔤 الحروف: {CHARSET_NAME}")
print(f"📊 عدد التركيبات: {TOTAL_COMBINATIONS:,}")
print("=" * 40)
print("")

confirm = input("هل تريد البدء؟ (y/n): ").strip().lower()
if confirm != 'y':
    print("❌ تم الإلغاء")
    sys.exit(0)

# ============ الاتصال بالبوت ============
print("")
print("📡 الاتصال بالبوت...")

client = TelegramClient('wordlist_bot', API_ID, API_HASH)

# ============ التوليد ============
OUTPUT_FILE = f"wordlist_{PASSWORD_LENGTH}_{int(time.time())}.txt"
counter = 0
start_time = time.time()

print(f"🔑 بدء التوليد...")
print(f"📁 الملف: {OUTPUT_FILE}")
print("")

def update_status():
    global counter, start_time
    elapsed = time.time() - start_time
    speed = int(counter / elapsed) if elapsed > 0 else 0
    progress = (counter / TOTAL_COMBINATIONS * 100) if TOTAL_COMBINATIONS > 0 else 0
    
    sys.stdout.write(f"\r📊 العدد: {counter:,}/{TOTAL_COMBINATIONS:,} | ⚡ السرعة: {speed:,}/ث | 📈 التقدم: {progress:.2f}% | ⏱️ {int(elapsed)}ث")
    sys.stdout.flush()

# التوليد
with open(OUTPUT_FILE, 'w') as f:
    for combo in itertools.product(CHARSET, repeat=PASSWORD_LENGTH):
        password = ''.join(combo)
        f.write(password + '\n')
        counter += 1
        
        # تحديث كل 10 آلاف
        if counter % 10000 == 0:
            update_status()

# ============ النهاية ============
elapsed = time.time() - start_time
speed = int(counter / elapsed) if elapsed > 0 else 0
file_size = os.path.getsize(OUTPUT_FILE)
file_size_mb = file_size / (1024 * 1024)

print("")
print("")
print("=" * 40)
print("✅ اكتمل التوليد!")
print("-" * 40)
print(f"📊 العدد: {counter:,}")
print(f"📦 الحجم: {file_size_mb:.2f} MB")
print(f"⏱️ الوقت: {int(elapsed)} ثانية")
print(f"⚡ السرعة: {speed:,} كلمة/ثانية")
print("=" * 40)
print("")

# ============ إرسال للبوت ============
print("📤 جاري الإرسال إلى البوت...")

async def send_to_bot():
    await client.start(bot_token=BOT_TOKEN)
    
    # الحصول على آخر محادثة
    dialogs = await client.get_dialogs()
    if dialogs:
        chat = dialogs[0]
        
        await client.send_file(
            chat,
            OUTPUT_FILE,
            caption=f"""
✅ **اكتمل توليد كلمات المرور**

📊 **العدد:** {counter:,}
📏 **الطول:** {PASSWORD_LENGTH}
🔤 **الحروف:** {CHARSET_NAME}
📦 **الحجم:** {file_size_mb:.2f} MB
⏱️ **الوقت:** {int(elapsed)} ثانية
⚡ **السرعة:** {speed:,} كلمة/ثانية
"""
        )
        print(f"✅ تم إرسال الملف إلى: {chat.name}")
    else:
        print("❌ لا توجد محادثات — أرسل /start للبوت أولاً")

with client:
    client.loop.run_until_complete(send_to_bot())

print("")
print("🎉 تم كل شيء بنجاح!")
print(f"📁 الملف محفوظ أيضاً في: {OUTPUT_FILE}")
