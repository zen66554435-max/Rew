#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import string
import os
import time
import threading
import requests
import sys
from pathlib import Path

# ============ الألوان والأنماط ============
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
MAGENTA = '\033[0;35m'
NC = '\033[0m'
BOLD = '\033[1m'

# ============ متغيرات عامة ============
stop_flag = False
counter = 0
start_time = 0
generating = False

def clear_screen():
    """تنظيف الشاشة"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    """طباعة البانر الرئيسي"""
    print(f"""{MAGENTA}{BOLD}
╔═══════════════════════════════════════════════════╗
║                                                   ║
║   🔐 DMARFOT Wordlist Generator v4.0 PRO 🚀      ║
║                                                   ║
║   توليد كلمات مرور فائقة السرعة مع البوت         ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
{NC}""")

def print_section_header(title, num):
    """طباعة رؤوس الأقسام"""
    print(f"\n{BOLD}{MAGENTA}[{num}]{NC} {BOLD}{CYAN}{title}{NC}")
    print(f"{MAGENTA}{'─' * 50}{NC}\n")

def divider():
    """خط فاصل"""
    print(f"{MAGENTA}{'═' * 50}{NC}")

def success(msg):
    """رسالة نجاح"""
    print(f"{GREEN}✅ {msg}{NC}")

def error(msg):
    """رسالة خطأ"""
    print(f"{RED}❌ {msg}{NC}")

def warning(msg):
    """رسالة تحذير"""
    print(f"{YELLOW}⚠️  {msg}{NC}")

def info(msg):
    """معلومة"""
    print(f"{CYAN}ℹ️  {msg}{NC}")

# ============ المدخلات ============
def get_bot_config():
    """الحصول على إعدادات البوت"""
    clear_screen()
    print_banner()
    print_section_header("إعدادات البوت", "1/4")
    
    BOT_TOKEN = input(f"{WHITE}🤖 أدخل توكن البوت: {NC}").strip()
    if not BOT_TOKEN:
        error("التوكن مطلوب!")
        return None, None
    
    CHAT_ID = input(f"{WHITE}💬 أدخل Chat ID (اترك فارغاً للتلقائي): {NC}").strip()
    
    clear_screen()
    return BOT_TOKEN, CHAT_ID

def get_password_settings():
    """الحصول على إعدادات كلمة المرور"""
    print_banner()
    print_section_header("إعدادات التوليد", "2/4")
    
    # طول كلمة المرور
    while True:
        try:
            pwd_length = int(input(f"{WHITE}📏 طول كلمة المرور (1-15): {NC}").strip())
            if 1 <= pwd_length <= 15:
                break
            error(f"الطول يجب أن يكون بين 1 و 15")
        except ValueError:
            error("أدخل رقماً صحيحاً")
    
    clear_screen()
    print_banner()
    print_section_header("اختر نوع الحروف", "2/4")
    
    # اختيار الحروف
    options = {
        "1": (string.digits, "أرقام فقط (0-9)"),
        "2": (string.ascii_lowercase, "أحرف صغيرة (a-z)"),
        "3": (string.ascii_uppercase, "أحرف كبيرة (A-Z)"),
        "4": (string.ascii_lowercase + string.digits, "أحرف صغيرة + أرقام"),
        "5": (string.ascii_uppercase + string.digits, "أحرف كبيرة + أرقام"),
        "6": (string.ascii_lowercase + string.ascii_uppercase, "أحرف صغيرة + كبيرة"),
        "7": (string.ascii_lowercase + string.ascii_uppercase + string.digits, "أحرف + أرقام (كامل)"),
        "8": (string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*", "أحرف + أرقام + رموز"),
        "9": ("custom", "حروف مخصصة"),
    }
    
    print(f"{CYAN}اختر من القائمة:{NC}")
    for key, (_, desc) in options.items():
        print(f"  {key}) {desc}")
    
    while True:
        choice = input(f"\n{WHITE}اختيارك: {NC}").strip()
        
        if choice == "9":
            charset = input(f"{WHITE}أدخل الحروف المخصصة: {NC}").strip()
            charset_name = f"مخصص: {charset}"
            if not charset:
                error("يجب إدخال حروف")
                continue
            break
        elif choice in options:
            charset, charset_name = options[choice]
            break
        else:
            error("خيار غير صحيح")
    
    clear_screen()
    return pwd_length, charset, charset_name

def get_limit_settings(total_possible):
    """الحصول على حد أقصى للكلمات"""
    print_banner()
    print_section_header("حد أقصى لعدد الكلمات", "3/4")
    
    est_size = total_possible * 12 / (1024 * 1024)
    info(f"الحجم المتوقع (بدون حد): {est_size:.2f} MB")
    info(f"عدد الكلمات المحتملة: {total_possible:,}")
    
    print(f"\n{CYAN}اختر الحد الأقصى:{NC}")
    print("  1) 10 مليون")
    print("  2) 100 مليون")
    print("  3) 500 مليون")
    print("  4) 1 مليار")
    print("  5) بدون حد (استخدم كل الاحتمالات)")
    print("  6) عدد مخصص")
    
    limits = {
        "1": 10_000_000,
        "2": 100_000_000,
        "3": 500_000_000,
        "4": 1_000_000_000,
        "5": total_possible,
    }
    
    while True:
        choice = input(f"\n{WHITE}اختيارك: {NC}").strip()
        
        if choice in limits:
            max_words = min(limits[choice], total_possible)
            break
        elif choice == "6":
            try:
                max_words = int(input(f"{WHITE}أدخل العدد: {NC}").strip())
                if max_words > 0 and max_words <= total_possible:
                    break
                error(f"الرقم يجب أن يكون بين 1 و {total_possible:,}")
            except ValueError:
                error("أدخل رقماً صحيحاً")
        else:
            error("خيار غير صحيح")
    
    clear_screen()
    return max_words

def get_split_settings():
    """الحصول على إعدادات التقسيم"""
    print_banner()
    print_section_header("تقسيم الملف", "3/4")
    
    split_choice = input(f"{WHITE}هل تريد تقسيم الملف؟ (y/n): {NC}").strip().lower()
    
    if split_choice == 'y':
        while True:
            try:
                split_size = int(input(f"{WHITE}حجم كل جزء (MB): {NC}").strip())
                if split_size > 0:
                    break
                error("الحجم يجب أن يكون أكبر من 0")
            except ValueError:
                error("أدخل رقماً صحيحاً")
    else:
        split_size = 0
    
    clear_screen()
    return split_size

def show_summary(bot_token, chat_id, pwd_length, charset_name, total, max_words, split_size):
    """عرض ملخص الإعدادات"""
    print_banner()
    print_section_header("ملخص الإعدادات", "4/4")
    
    divider()
    print(f"{BOLD}{GREEN}البوت والمحادثة:{NC}")
    print(f"  🤖 التوكن: {BOLD}{bot_token[:20]}...{NC}")
    if chat_id:
        print(f"  💬 Chat ID: {BOLD}{chat_id}{NC}")
    else:
        print(f"  💬 Chat ID: {YELLOW}سيتم الحصول عليه تلقائياً{NC}")
    
    print(f"\n{BOLD}{GREEN}إعدادات التوليد:{NC}")
    print(f"  📏 الطول: {BOLD}{pwd_length}{NC}")
    print(f"  🔤 الحروف: {BOLD}{charset_name}{NC}")
    print(f"  📊 الكلمات المتاحة: {BOLD}{total:,}{NC}")
    print(f"  📊 الكلمات المطلوبة: {BOLD}{max_words:,}{NC}")
    
    if split_size:
        print(f"\n{BOLD}{GREEN}التقسيم:{NC}")
        print(f"  📦 حجم كل جزء: {BOLD}{split_size} MB{NC}")
    
    divider()

# ============ دوال البوت ============
BASE_URL = None

def init_bot(token):
    """تهيئة البوت"""
    global BASE_URL
    BASE_URL = f"https://api.telegram.org/bot{token}"

def send_message(chat_id, text):
    """إرسال رسالة"""
    try:
        r = requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
        return r.json()
    except:
        return None

def send_file(chat_id, file_path, caption=""):
    """إرسال ملف"""
    try:
        with open(file_path, "rb") as f:
            r = requests.post(
                f"{BASE_URL}/sendDocument",
                data={"chat_id": chat_id, "caption": caption},
                files={"document": f},
                timeout=120
            )
        return r.json()
    except Exception as e:
        return None

def get_updates(offset=None):
    """الحصول على التحديثات"""
    try:
        url = f"{BASE_URL}/getUpdates"
        if offset:
            url += f"?offset={offset}"
        r = requests.get(url, timeout=15)
        return r.json()
    except:
        return None

def get_me():
    """التحقق من البوت"""
    try:
        r = requests.get(f"{BASE_URL}/getMe", timeout=10)
        return r.json()
    except:
        return None

def get_chat_id():
    """الحصول على Chat ID"""
    updates = get_updates()
    if updates and updates.get("ok") and updates.get("result"):
        for update in reversed(updates["result"]):
            if "message" in update:
                return update["message"]["chat"]["id"]
            elif "callback_query" in update:
                return update["callback_query"]["message"]["chat"]["id"]
    return None

def verify_bot(bot_token):
    """التحقق من البوت"""
    print(f"\n{CYAN}🔗 التحقق من البوت...{NC}")
    init_bot(bot_token)
    
    bot_info = get_me()
    if bot_info and bot_info.get("ok"):
        bot_name = bot_info["result"]["username"]
        success(f"البوت متصل: @{bot_name}")
        return True
    else:
        error("فشل الاتصال بالبوت - تأكد من التوكن")
        return False

def get_auto_chat_id():
    """الحصول على Chat ID تلقائياً"""
    print(f"\n{YELLOW}⏳ جاري الحصول على Chat ID...{NC}")
    warning("أرسل أي رسالة للبوت الآن!")
    
    for i in range(30):
        chat_id = get_chat_id()
        if chat_id:
            success(f"Chat ID: {chat_id}")
            return chat_id
        print(f"\r{CYAN}جاري الانتظار... ({30-i}ث){NC}", end="")
        sys.stdout.flush()
        time.sleep(1)
    
    print()
    error("لم يتم العثور على محادثة - أرسل رسالة للبوت أولاً")
    return None

# ============ التوليد ============
def generate_words_fast(charset, pwd_length, max_words, output_file):
    """توليد سريع جداً للكلمات"""
    global counter, start_time, generating, stop_flag
    
    generating = True
    counter = 0
    start_time = time.time()
    
    try:
        # استخدام write بكفاءة عالية
        with open(output_file, "w", buffering=1024*1024) as f:
            buffer = []
            buffer_size = 100000
            
            for combo in itertools.product(charset, repeat=pwd_length):
                if stop_flag or counter >= max_words:
                    break
                
                buffer.append("".join(combo) + "\n")
                counter += 1
                
                # كتابة كل 100 ألف كلمة
                if len(buffer) >= buffer_size:
                    f.writelines(buffer)
                    buffer = []
                
                if counter % 500000 == 0:
                    update_progress()
            
            # كتابة الباقي
            if buffer:
                f.writelines(buffer)
    except Exception as e:
        error(f"خطأ في التوليد: {e}")
    finally:
        generating = False

def update_progress():
    """تحديث شريط التقدم"""
    global counter, start_time
    
    elapsed = time.time() - start_time
    speed = int(counter / elapsed) if elapsed > 0 else 0
    progress = (counter / MAX_WORDS * 100) if MAX_WORDS > 0 else 0
    eta = int((MAX_WORDS - counter) / speed) if speed > 0 else 0
    
    bar_length = 30
    filled = int(bar_length * counter / MAX_WORDS) if MAX_WORDS > 0 else 0
    bar = "█" * filled + "░" * (bar_length - filled)
    
    sys.stdout.write(
        f"\r{CYAN}[{bar}] {progress:6.2f}% | "
        f"{counter:,}/{MAX_WORDS:,} | "
        f"⚡ {speed:,}/ث | "
        f"⏱️ {int(elapsed):,}ث{NC}"
    )
    sys.stdout.flush()

# ============ البرنامج الرئيسي ============
def main():
    global MAX_WORDS
    
    # جمع الإعدادات
    print("\n")
    bot_token, chat_id = get_bot_config()
    if not bot_token:
        return
    
    pwd_length, charset, charset_name = get_password_settings()
    
    total_possible = len(charset) ** pwd_length
    MAX_WORDS = get_limit_settings(total_possible)
    
    split_size = get_split_settings()
    
    show_summary(bot_token, chat_id or "تلقائي", pwd_length, charset_name, 
                 total_possible, MAX_WORDS, split_size)
    
    # التأكيد
    confirm = input(f"\n{WHITE}🚀 ابدأ التوليد والإرسال؟ (y/n): {NC}").strip().lower()
    if confirm != 'y':
        error("تم الإلغاء")
        return
    
    clear_screen()
    print_banner()
    print_section_header("عملية التوليد", "5/5")
    
    # التحقق من البوت
    if not verify_bot(bot_token):
        return
    
    # الحصول على Chat ID
    if not chat_id:
        chat_id = get_auto_chat_id()
        if not chat_id:
            return
    
    # التوليد
    output_file = f"wordlist_{pwd_length}_{int(time.time())}.txt"
    print(f"\n{CYAN}📁 الملف: {BOLD}{output_file}{NC}\n")
    
    gen_thread = threading.Thread(
        target=generate_words_fast,
        args=(charset, pwd_length, MAX_WORDS, output_file)
    )
    gen_thread.start()
    
    while gen_thread.is_alive():
        time.sleep(0.2)
    
    gen_thread.join()
    
    # معلومات الملف
    elapsed = time.time() - start_time
    speed = int(counter / elapsed) if elapsed > 0 else 0
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print("\n\n")
    divider()
    print(f"{BOLD}{GREEN}✅ اكتمل التوليد!{NC}")
    divider()
    print(f"  📊 عدد الكلمات: {BOLD}{counter:,}{NC}")
    print(f"  📦 حجم الملف: {BOLD}{file_size_mb:.2f} MB{NC}")
    print(f"  ⏱️  الوقت: {BOLD}{int(elapsed)} ثانية{NC}")
    print(f"  ⚡ السرعة: {BOLD}{speed:,} كلمة/ثانية{NC}")
    divider()
    
    # الإرسال
    print(f"\n{CYAN}📤 جاري الإرسال للبوت...{NC}\n")
    
    if split_size > 0:
        split_size_bytes = split_size * 1024 * 1024
        part_num = 1
        
        with open(output_file, "r", buffering=1024*1024) as f:
            while True:
                lines = f.readlines(split_size_bytes // (pwd_length + 1))
                if not lines:
                    break
                
                part_file = f"{output_file}.part{part_num}"
                with open(part_file, "w", buffering=1024*1024) as pf:
                    pf.writelines(lines)
                
                part_size = os.path.getsize(part_file) / (1024 * 1024)
                caption = (
                    f"<b>📦 جزء {part_num}</b>\n"
                    f"📊 الحجم: {part_size:.2f} MB\n"
                    f"🔐 DMARFOT v4.0"
                )
                
                print(f"{YELLOW}📤 إرسال الجزء {part_num} ({part_size:.2f} MB)...{NC}")
                result = send_file(chat_id, part_file, caption)
                
                if result and result.get("ok"):
                    success(f"تم إرسال الجزء {part_num}")
                else:
                    error(f"فشل إرسال الجزء {part_num}")
                
                os.remove(part_file)
                part_num += 1
    else:
        caption = (
            f"<b>✅ اكتمل توليد كلمات المرور</b>\n"
            f"<code>{'─' * 30}</code>\n"
            f"<b>📊 العدد:</b> <code>{counter:,}</code>\n"
            f"<b>📏 الطول:</b> <code>{pwd_length}</code>\n"
            f"<b>🔤 الحروف:</b> <code>{charset_name}</code>\n"
            f"<b>📦 الحجم:</b> <code>{file_size_mb:.2f} MB</code>\n"
            f"<b>⏱️  الوقت:</b> <code>{int(elapsed)}ث</code>\n"
            f"<b>⚡ السرعة:</b> <code>{speed:,} كلمة/ث</code>\n"
            f"<code>{'─' * 30}</code>\n"
            f"<b>🚀 DMARFOT v4.0 PRO</b>"
        )
        
        print(f"{YELLOW}📤 إرسال الملف ({file_size_mb:.2f} MB)...{NC}")
        result = send_file(chat_id, output_file, caption)
        
        if result and result.get("ok"):
            success("تم إرسال الملف بنجاح!")
        else:
            error("فشل الإرسال")
            warning(f"الملف محفوظ محلياً: {output_file}")
    
    # النهاية
    print("\n")
    divider()
    print(f"{BOLD}{GREEN}🎉 تم بنجاح!{NC}")
    divider()
    print(f"📁 الملف: {BOLD}{output_file}{NC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}⛔ تم الإيقاف من قبل المستخدم{NC}\n")
    except Exception as e:
        error(f"خطأ: {e}")
