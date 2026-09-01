#!/bin/bash

# ============================================
#   👻 THE GHOST - Samsung Galaxy A50 Session
# ============================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
BLACK='\033[0;30m'
BG_GREEN='\033[42m'
BG_RED='\033[41m'
BG_CYAN='\033[46m'
BG_PURPLE='\033[45m'
BOLD='\033[1m'
BLINK='\033[5m'
NC='\033[0m'

clear

# ============================================
#  BANNER
# ============================================
echo -e "${BG_PURPLE}${WHITE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     ████████╗██╗  ██╗███████╗                         ║"
echo "║        ██╔══╝██║  ██║██╔════╝                         ║"
echo "║        ██║   ███████║█████╗                           ║"
echo "║        ██║   ██╔══██║██╔══╝                           ║"
echo "║        ██║   ██║  ██║███████╗                         ║"
echo "║        ╚═╝   ╚═╝  ╚═╝╚══════╝                         ║"
echo "║                                                          ║"
echo "║     ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗        ║"
echo "║    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝        ║"
echo "║    ██║  ███╗███████║██║   ██║███████╗   ██║           ║"
echo "║    ██║   ██║██╔══██║██║   ██║╚════██║   ██║           ║"
echo "║    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║           ║"
echo "║     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝           ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}${BOLD}     👻 THE GHOST - Remote Control Session${NC}"
echo -e "${WHITE}     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================
#  Session Active
# ============================================
echo -e "${BG_GREEN}${BLACK}${BOLD}  ✅ تم فتح جلسة على جهاز Samsung Galaxy A50  ${NC}"
echo -e "${GREEN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${WHITE}  📱 الجهاز    : ${GREEN}Samsung Galaxy A50${NC}"
echo -e "${WHITE}  🔢 الموديل   : ${GREEN}SM-A505F${NC}"
echo -e "${WHITE}  🤖 النظام    : ${GREEN}Android 11${NC}"
echo -e "${WHITE}  📶 الاتصال   : ${GREEN}مستقر ✓${NC}"
echo -e "${WHITE}  🔴 الجلسة    : ${GREEN}نشطة ✓${NC}"
echo ""

# ============================================
#  قائمة التحكم
# ============================================
while true; do
    echo -e "${BG_PURPLE}${WHITE}${BOLD}  👻 لوحة تحكم الشبح — 20 خيار  ${NC}"
    echo -e "${PURPLE}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  [1]${WHITE}  📷 سحب صور الكاميرا"
    echo -e "${CYAN}  [2]${WHITE}  🖼️ سحب صور المعرض"
    echo -e "${CYAN}  [3]${WHITE}  📂 سحب جميع الملفات"
    echo -e "${CYAN}  [4]${WHITE}  📹 تسجيل فيديو"
    echo -e "${CYAN}  [5]${WHITE}  🎤 تسجيل صوت"
    echo -e "${CYAN}  [6]${WHITE}  📍 سحب الموقع"
    echo -e "${CYAN}  [7]${WHITE}  📞 سحب سجل المكالمات"
    echo -e "${CYAN}  [8]${WHITE}  💬 سحب الرسائل"
    echo -e "${CYAN}  [9]${WHITE}  📇 سحب جهات الاتصال"
    echo -e "${CYAN}  [10]${WHITE} 📱 سحب معلومات الجهاز"
    echo -e "${CYAN}  [11]${WHITE} 🔋 حالة البطارية"
    echo -e "${CYAN}  [12]${WHITE} 📶 الشبكة"
    echo -e "${CYAN}  [13]${WHITE} 🖥️ بث الشاشة"
    echo -e "${CYAN}  [14]${WHITE} 🎮 التحكم بالشاشة"
    echo -e "${CYAN}  [15]${WHITE} 📱 تثبيت تطبيق"
    echo -e "${CYAN}  [16]${WHITE} 🗑️ حذف تطبيق"
    echo -e "${CYAN}  [17]${WHITE} 🔒 قفل الجهاز"
    echo -e "${CYAN}  [18]${WHITE} 🔔 إرسال إشعار"
    echo -e "${CYAN}  [19]${WHITE} 📳 اهتزاز"
    echo -e "${CYAN}  [20]${WHITE} ⚙️ إعدادات متقدمة"
    echo -e "${PURPLE}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  [0]${WHITE} 🚪 إنهاء الجلسة"
    echo -e "${PURPLE}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -ne "${WHITE}  ${BOLD}اختر العملية: ${NC}"
    read choice
    
    case $choice in
        1)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  📷 سحب صور الكاميرا  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} فتح الكاميرا الخلفية..."
            sleep 1
            echo -e "${WHITE}  ${GREEN}✓${NC} التقاط صورة..."
            sleep 1
            echo -e "${WHITE}  ${GREEN}✓${NC} تم حفظ: ${CYAN}/sdcard/DCIM/ghost_cam_$(date +%H%M%S).jpg${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري الإرسال للخادم..."
            sleep 1
            echo -e "${WHITE}  ${GREEN}✓${NC} تم الإرسال بنجاح"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        2)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🖼️ سحب صور المعرض  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} فحص المجلدات..."
            sleep 1
            echo -e "${WHITE}  ${GREEN}✓${NC} تم العثور على ${CYAN}247${NC} صورة"
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري السحب..."
            sleep 2
            echo -e "${WHITE}  ${GREEN}✓${NC} تم سحب ${CYAN}247${NC} صورة"
            echo -e "${WHITE}  ${GREEN}✓${NC} الحجم: ${CYAN}1.2 GB${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم الإرسال"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        3)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📂 سحب جميع الملفات  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} فحص التخزين..."
            sleep 1
            echo -e "${WHITE}  📁 DCIM: ${CYAN}1.8 GB${NC}"
            echo -e "${WHITE}  📁 Download: ${CYAN}450 MB${NC}"
            echo -e "${WHITE}  📁 Documents: ${CYAN}120 MB${NC}"
            echo -e "${WHITE}  📁 WhatsApp: ${CYAN}890 MB${NC}"
            echo -e "${WHITE}  📁 Pictures: ${CYAN}1.2 GB${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري السحب الكامل..."
            sleep 3
            echo -e "${WHITE}  ${GREEN}✓${NC} تم سحب ${CYAN}4.4 GB${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        4)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  📹 تسجيل فيديو  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} بدء التسجيل..."
            sleep 3
            echo -e "${WHITE}  ${GREEN}✓${NC} تم التسجيل: ${CYAN}/sdcard/DCIM/ghost_vid_$(date +%H%M%S).mp4${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} المدة: ${CYAN}00:03:00${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم الإرسال"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        5)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🎤 تسجيل صوت  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} بدء التسجيل..."
            sleep 3
            echo -e "${WHITE}  ${GREEN}✓${NC} تم التسجيل: ${CYAN}/sdcard/Recordings/ghost_aud_$(date +%H%M%S).m4a${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} المدة: ${CYAN}00:05:00${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        6)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📍 سحب الموقع  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  🛰️ خط العرض: ${GREEN}24.7136° N${NC}"
            echo -e "${WHITE}  🛰️ خط الطول: ${GREEN}46.6753° E${NC}"
            echo -e "${WHITE}  📍 العنوان: ${GREEN}الرياض، السعودية${NC}"
            echo -e "${WHITE}  🗺️ ${GREEN}https://maps.google.com/?q=24.7136,46.6753${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        7)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📞 سجل المكالمات  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم العثور على ${CYAN}156${NC} مكالمة"
            echo -e "${WHITE}  📞 آخر مكالمة: ${GREEN}+9665xxxxxxxx${NC}"
            echo -e "${WHITE}  ⏱️ المدة: ${GREEN}00:15:23${NC}"
            echo -e "${WHITE}  📅 التاريخ: ${GREEN}$(date '+%Y-%m-%d')${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم السحب والإرسال"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        8)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  💬 الرسائل  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  📱 SMS: ${GREEN}89${NC} رسالة"
            echo -e "${WHITE}  💬 WhatsApp: ${GREEN}1,234${NC} رسالة"
            echo -e "${WHITE}  📩 Telegram: ${GREEN}567${NC} رسالة"
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري السحب..."
            sleep 2
            echo -e "${WHITE}  ${GREEN}✓${NC} تم سحب جميع الرسائل"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        9)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📇 جهات الاتصال  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم العثور على ${CYAN}345${NC} جهة اتصال"
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري السحب..."
            sleep 1
            echo -e "${WHITE}  ${GREEN}✓${NC} تم سحب ${CYAN}345${NC} جهة"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        10)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📱 معلومات الجهاز  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  📱 النوع: ${GREEN}Samsung Galaxy A50${NC}"
            echo -e "${WHITE}  🔢 الموديل: ${GREEN}SM-A505F${NC}"
            echo -e "${WHITE}  🔢 IMEI: ${GREEN}356789102345678${NC}"
            echo -e "${WHITE}  🔢 Serial: ${GREEN}R58M93XKZ2E${NC}"
            echo -e "${WHITE}  🤖 النظام: ${GREEN}Android 11${NC}"
            echo -e "${WHITE}  🖥️ المعالج: ${GREEN}Exynos 9610${NC}"
            echo -e "${WHITE}  💾 الذاكرة: ${GREEN}4GB / 64GB${NC}"
            echo -e "${WHITE}  📶 IP: ${GREEN}192.168.1.105${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        11)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  🔋 البطارية  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  🔋 النسبة: ${GREEN}78%${NC}"
            echo -e "${WHITE}  ⚡ الشحن: ${GREEN}غير متصل${NC}"
            echo -e "${WHITE}  🌡️ الحرارة: ${GREEN}34°C${NC}"
            echo -e "${WHITE}  ⏳ المتبقي: ${GREEN}18 ساعة و 25 دقيقة${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        12)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📶 الشبكة  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  📶 الإشارة: ${GREEN}ممتازة${NC}"
            echo -e "${WHITE}  📱 المشغل: ${GREEN}STC${NC}"
            echo -e "${WHITE}  📶 النوع: ${GREEN}4G LTE${NC}"
            echo -e "${WHITE}  📡 IP: ${GREEN}192.168.1.105${NC}"
            echo -e "${WHITE}  🌐 الوكيل: ${GREEN}غير موجود${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        13)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🖥️ بث الشاشة  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} بدء بث الشاشة..."
            sleep 2
            echo -e "${WHITE}  ${GREEN}✓${NC} البث نشط — معدل الإطارات: ${CYAN}30 FPS${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} الجودة: ${CYAN}1080p${NC}"
            echo ""
            read -p "  اضغط Enter لإيقاف..."
            clear
            ;;
        14)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🎮 التحكم بالشاشة  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} اللمس: ${CYAN}نشط${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} السحب: ${CYAN}نشط${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} الكتابة: ${CYAN}نشطة${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} التمرير: ${CYAN}نشط${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        15)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📱 تثبيت تطبيق  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -ne "${WHITE}  رابط APK: ${NC}"
            read apk_url
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري التثبيت..."
            sleep 2
            echo -e "${WHITE}  ${GREEN}✓${NC} تم تثبيت التطبيق بنجاح"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        16)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🗑️ حذف تطبيق  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -ne "${WHITE}  اسم الحزمة: ${NC}"
            read package_name
            echo -e "${WHITE}  ${GREEN}✓${NC} جاري الحذف..."
            sleep 1
            echo -e "${WHITE}  ${GREEN}✓${NC} تم حذف ${package_name}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        17)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🔒 قفل الجهاز  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم قفل الجهاز"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم تغيير كلمة السر"
            echo -e "${WHITE}  🔑 كلمة السر الجديدة: ${CYAN}ghost2024${NC}"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        18)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  🔔 إرسال إشعار  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -ne "${WHITE}  عنوان الإشعار: ${NC}"
            read notif_title
            echo -ne "${WHITE}  نص الإشعار: ${NC}"
            read notif_text
            echo -e "${WHITE}  ${GREEN}✓${NC} تم إرسال الإشعار"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        19)
            clear
            echo -e "${BG_CYAN}${BLACK}${BOLD}  📳 اهتزاز  ${NC}"
            echo -e "${CYAN}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${GREEN}✓${NC} اهتزاز مستمر..."
            sleep 2
            echo -e "${WHITE}  ${GREEN}✓${NC} تم الإيقاف"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        20)
            clear
            echo -e "${BG_PURPLE}${WHITE}${BOLD}  ⚙️ إعدادات متقدمة  ${NC}"
            echo -e "${PURPLE}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${CYAN}[1]${WHITE} تغيير IP"
            echo -e "${WHITE}  ${CYAN}[2]${WHITE} إخفاء الأثر"
            echo -e "${WHITE}  ${CYAN}[3]${WHITE} تدمير النظام"
            echo -e "${WHITE}  ${CYAN}[4]${WHITE} نسخ احتياطي"
            echo -e "${WHITE}  ${CYAN}[5]${WHITE} استعادة ضبط المصنع"
            echo ""
            read -p "  اضغط Enter..."
            clear
            ;;
        0)
            clear
            echo -e "${BG_RED}${WHITE}${BOLD}  🚪 إنهاء الجلسة  ${NC}"
            echo -e "${RED}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${WHITE}  ${YELLOW}⚠️${NC} جاري إغلاق الجلسة..."
            sleep 2
            echo -e "${WHITE}  ${GREEN}✓${NC} تم إغلاق الجلسة"
            echo -e "${WHITE}  ${GREEN}✓${NC} تم مسح الآثار"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}  ❌ خيار خاطئ${NC}"
            sleep 1
            clear
            ;;
    esac
done
