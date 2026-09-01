#!/bin/bash
# ============================================
# DMAR - أداة فحص الروابط والمواقع
# الإصدار: 2.0
# المطور: The Ghost
# متوافقة مع: Linux / Termux / iSH
# ============================================

# ============ الألوان ============
R='\033[0;31m'
G='\033[0;32m'
Y='\033[0;33m'
B='\033[0;34m'
P='\033[0;35m'
C='\033[0;36m'
W='\033[0;37m'
NC='\033[0m'
BOLD='\033[1m'

# ============ المتغيرات ============
VERSION="2.0"
TARGET_URL=""
TIMEOUT=10
USER_AGENT="Mozilla/5.0 (Linux; Android 12; DMAR Scanner) AppleWebKit/537.36"

# ============ دالة البانر ============
show_banner() {
    clear
    echo -e "${R}${BOLD}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║                                                  ║"
    echo "║        ██████╗ ███╗   ███╗ █████╗ ██████╗        ║"
    echo "║        ██╔══██╗████╗ ████║██╔══██╗██╔══██╗       ║"
    echo "║        ██║  ██║██╔████╔██║███████║██████╔╝       ║"
    echo "║        ██║  ██║██║╚██╔╝██║██╔══██║██╔══██╗       ║"
    echo "║        ██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║       ║"
    echo "║        ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝       ║"
    echo "║                                                  ║"
    echo "╠══════════════════════════════════════════════════╣"
    echo "║     أداة فحص الروابط والمواقع المتكاملة           ║"
    echo "║     الإصدار: ${VERSION}                              ║"
    echo "║     المطور: The Ghost                             ║"
    echo "║     المنصة: Linux / Termux / iSH                  ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ============ دالة التثبيت التلقائي ============
install_deps() {
    echo -e "${Y}[+] جاري فحص وتثبيت المتطلبات...${NC}"
    
    # التحقق من curl
    if ! command -v curl > /dev/null 2>&1; then
        echo -e "${Y}[!] تثبيت curl...${NC}"
        if command -v apt > /dev/null 2>&1; then
            apt install -y curl > /dev/null 2>&1
        elif command -v pkg > /dev/null 2>&1; then
            pkg install -y curl > /dev/null 2>&1
        elif command -v apk > /dev/null 2>&1; then
            apk add curl > /dev/null 2>&1
        elif command -v yum > /dev/null 2>&1; then
            yum install -y curl > /dev/null 2>&1
        elif command -v dnf > /dev/null 2>&1; then
            dnf install -y curl > /dev/null 2>&1
        fi
    fi
    
    # التحقق من dig
    if ! command -v dig > /dev/null 2>&1; then
        echo -e "${Y}[!] تثبيت dnsutils...${NC}"
        if command -v apt > /dev/null 2>&1; then
            apt install -y dnsutils > /dev/null 2>&1
        elif command -v pkg > /dev/null 2>&1; then
            pkg install -y dnsutils > /dev/null 2>&1
        elif command -v apk > /dev/null 2>&1; then
            apk add bind-tools > /dev/null 2>&1
        fi
    fi
    
    # التحقق من whois
    if ! command -v whois > /dev/null 2>&1; then
        echo -e "${Y}[!] تثبيت whois...${NC}"
        if command -v apt > /dev/null 2>&1; then
            apt install -y whois > /dev/null 2>&1
        elif command -v pkg > /dev/null 2>&1; then
            pkg install -y whois > /dev/null 2>&1
        fi
    fi
    
    echo -e "${G}[✓] اكتمل فحص المتطلبات${NC}"
    echo ""
}

# ============ دالة إدخال الرابط ============
get_url() {
    echo -e "${Y}[?] أدخل الرابط أو الموقع المراد فحصه:${NC}"
    echo -e "${W}مثال: example.com${NC}"
    echo ""
    printf "${C}❯ ${NC}"
    read TARGET_URL
    
    # تنظيف الرابط
    TARGET_URL=$(echo "$TARGET_URL" | sed 's|^https\?://||' | sed 's|^www\.||' | sed 's|/$||')
    
    if [ -z "$TARGET_URL" ]; then
        echo -e "${R}[!] خطأ: الرابط فارغ${NC}"
        sleep 1
        get_url
    fi
    echo ""
}

# ============ دالة فحص DNS ============
check_dns() {
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${C}${BOLD}  [1] فحص سجلات DNS${NC}"
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if command -v dig > /dev/null 2>&1; then
        echo -e "${Y}[→] سجلات A (IPv4):${NC}"
        dig +short A "$TARGET_URL" 2>/dev/null | grep -E '^[0-9]' | while read line; do
            echo -e "   ${G}└─ ${W}$line${NC}"
        done
        echo ""
        
        echo -e "${Y}[→] سجلات NS:${NC}"
        dig +short NS "$TARGET_URL" 2>/dev/null | grep -v '^$' | while read line; do
            echo -e "   ${G}└─ ${W}$line${NC}"
        done
        echo ""
        
        echo -e "${Y}[→] سجلات MX:${NC}"
        dig +short MX "$TARGET_URL" 2>/dev/null | grep -v '^$' | while read line; do
            echo -e "   ${G}└─ ${W}$line${NC}"
        done
        echo ""
    else
        # استخدام nslookup كبديل
        echo -e "${Y}[→] استخدام nslookup:${NC}"
        nslookup "$TARGET_URL" 2>/dev/null | grep -A5 "Name:" | while read line; do
            echo -e "   ${G}└─ ${W}$line${NC}"
        done
        echo ""
    fi
}

# ============ دالة فحص HTTP ============
check_http() {
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${C}${BOLD}  [2] فحص HTTP/HTTPS${NC}"
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if command -v curl > /dev/null 2>&1; then
        # فحص HTTPS
        echo -e "${Y}[→] فحص HTTPS:${NC}"
        HTTPS_CODE=$(curl -sk -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" "https://$TARGET_URL" 2>/dev/null)
        
        if [ "$HTTPS_CODE" != "000" ] && [ -n "$HTTPS_CODE" ]; then
            echo -e "   ${G}✓ HTTPS متاح - رمز الحالة: $HTTPS_CODE${NC}"
            
            # جلب الترويسات
            echo -e "   ${Y}الترويسات الرئيسية:${NC}"
            curl -skI --max-time "$TIMEOUT" "https://$TARGET_URL" 2>/dev/null | head -8 | while read line; do
                [ -n "$line" ] && echo -e "      ${C}• ${W}$line${NC}"
            done
        else
            echo -e "   ${R}✗ HTTPS غير متاح${NC}"
        fi
        echo ""
        
        # فحص HTTP
        echo -e "${Y}[→] فحص HTTP:${NC}"
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" "http://$TARGET_URL" 2>/dev/null)
        
        if [ "$HTTP_CODE" != "000" ] && [ -n "$HTTP_CODE" ]; then
            echo -e "   ${G}✓ HTTP متاح - رمز الحالة: $HTTP_CODE${NC}"
        else
            echo -e "   ${R}✗ HTTP غير متاح${NC}"
        fi
        echo ""
    else
        # استخدام wget كبديل
        if command -v wget > /dev/null 2>&1; then
            echo -e "${Y}[→] فحص بواسطة wget:${NC}"
            wget --spider --timeout="$TIMEOUT" "https://$TARGET_URL" 2>&1 | grep -E "HTTP|Length" | head -5
            echo ""
        else
            echo -e "${R}[!] لا يوجد curl أو wget متاح${NC}"
            echo ""
        fi
    fi
}

# ============ دالة فحص المنافذ ============
check_ports() {
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${C}${BOLD}  [3] فحص المنافذ الشائعة${NC}"
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # حل النطاق إلى IP
    IP_ADDR=""
    if command -v dig > /dev/null 2>&1; then
        IP_ADDR=$(dig +short A "$TARGET_URL" 2>/dev/null | head -1)
    fi
    
    if [ -z "$IP_ADDR" ]; then
        IP_ADDR="$TARGET_URL"
    fi
    
    echo -e "${Y}[→] فحص المنافذ على: $IP_ADDR${NC}"
    echo ""
    
    PORTS="21 22 25 53 80 110 143 443 465 587 993 995 3306 5432 8080 8443"
    PORT_NAMES="FTP SSH SMTP DNS HTTP POP3 IMAP HTTPS SMTPS SMTP-Sub IMAPS POP3S MySQL PostgreSQL HTTP-Alt HTTPS-Alt"
    
    for PORT in $PORTS; do
        NAME=$(echo "$PORT_NAMES" | cut -d' ' -f1)
        PORT_NAMES=$(echo "$PORT_NAMES" | cut -d' ' -f2-)
        
        if command -v nc > /dev/null 2>&1; then
            # استخدام netcat
            if nc -z -w 3 "$IP_ADDR" "$PORT" 2>/dev/null; then
                echo -e "   ${G}[✓] المنفذ $PORT ($NAME): مفتوح${NC}"
            else
                echo -e "   ${R}[✗] المنفذ $PORT ($NAME): مغلق${NC}"
            fi
        elif command -v bash > /dev/null 2>&1; then
            # استخدام bash /dev/tcp
            if timeout 3 bash -c "echo > /dev/tcp/$IP_ADDR/$PORT" 2>/dev/null; then
                echo -e "   ${G}[✓] المنفذ $PORT ($NAME): مفتوح${NC}"
            else
                echo -e "   ${R}[✗] المنفذ $PORT ($NAME): مغلق${NC}"
            fi
        else
            echo -e "   ${Y}[?] لا يمكن فحص المنفذ $PORT${NC}"
        fi
    done
    echo ""
}

# ============ دالة فحص الأمان ============
check_security() {
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${C}${BOLD}  [4] فحص ترويسات الأمان${NC}"
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if command -v curl > /dev/null 2>&1; then
        HEADERS=$(curl -skI --max-time "$TIMEOUT" "https://$TARGET_URL" 2>/dev/null)
        
        # فحص كل ترويسة
        check_header() {
            HEADER_NAME="$1"
            DISPLAY_NAME="$2"
            if echo "$HEADERS" | grep -qi "^$HEADER_NAME:"; then
                echo -e "   ${G}[✓] $DISPLAY_NAME: موجود${NC}"
            else
                echo -e "   ${R}[✗] $DISPLAY_NAME: غائب${NC}"
            fi
        }
        
        check_header "x-frame-options" "X-Frame-Options"
        check_header "x-content-type-options" "X-Content-Type-Options"
        check_header "strict-transport-security" "HSTS"
        check_header "content-security-policy" "CSP"
        check_header "referrer-policy" "Referrer-Policy"
        check_header "permissions-policy" "Permissions-Policy"
    else
        echo -e "${R}[!] curl غير متاح لفحص الأمان${NC}"
    fi
    echo ""
}

# ============ دالة فحص التقنيات ============
check_tech() {
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${C}${BOLD}  [5] فحص التقنيات المستخدمة${NC}"
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if command -v curl > /dev/null 2>&1; then
        HEADERS=$(curl -skI --max-time "$TIMEOUT" "https://$TARGET_URL" 2>/dev/null)
        
        # استخراج معلومات الخادم
        SERVER=$(echo "$HEADERS" | grep -i "^server:" | sed 's/^[Ss]erver: //' | tr -d '\r')
        if [ -n "$SERVER" ]; then
            echo -e "${Y}[→] الخادم:${W} $SERVER${NC}"
        fi
        
        # استخراج X-Powered-By
        POWERED=$(echo "$HEADERS" | grep -i "^x-powered-by:" | sed 's/^[Xx]-[Pp]owered-[Bb]y: //' | tr -d '\r')
        if [ -n "$POWERED" ]; then
            echo -e "${Y}[→] تقنية التشغيل:${W} $POWERED${NC}"
        fi
        
        # فحص الملفات الشائعة
        echo ""
        echo -e "${Y}[→] فحص الملفات الشائعة:${NC}"
        
        check_file() {
            FILE_PATH="$1"
            FILE_NAME="$2"
            CODE=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 5 "https://$TARGET_URL/$FILE_PATH" 2>/dev/null)
            if [ "$CODE" = "200" ]; then
                echo -e "   ${G}[✓] $FILE_NAME: موجود${NC}"
            else
                echo -e "   ${R}[✗] $FILE_NAME: غير موجود${NC}"
            fi
        }
        
        check_file "robots.txt" "robots.txt"
        check_file "sitemap.xml" "sitemap.xml"
        check_file ".well-known/security.txt" "security.txt"
    else
        echo -e "${R}[!] curl غير متاح${NC}"
    fi
    echo ""
}

# ============ دالة توليد التقرير ============
generate_report() {
    REPORT_FILE="DMAR_Report_$(date +%Y%m%d_%H%M%S).txt"
    
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${C}${BOLD}  [6] توليد التقرير${NC}"
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    {
        echo "============================================"
        echo "DMAR - تقرير فحص شامل"
        echo "============================================"
        echo "الهدف: $TARGET_URL"
        echo "التاريخ: $(date)"
        echo ""
        echo "--------------------------------------------"
        echo "[1] معلومات DNS:"
        echo "--------------------------------------------"
        if command -v dig > /dev/null 2>&1; then
            dig +short A "$TARGET_URL" 2>/dev/null
            echo ""
            dig +short NS "$TARGET_URL" 2>/dev/null
        fi
        echo ""
        echo "--------------------------------------------"
        echo "[2] حالة HTTP/HTTPS:"
        echo "--------------------------------------------"
        if command -v curl > /dev/null 2>&1; then
            HTTPS_CODE=$(curl -sk -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" "https://$TARGET_URL" 2>/dev/null)
            echo "HTTPS: $HTTPS_CODE"
        fi
        echo ""
        echo "--------------------------------------------"
        echo "[3] ترويسات الأمان:"
        echo "--------------------------------------------"
        if command -v curl > /dev/null 2>&1; then
            curl -skI --max-time "$TIMEOUT" "https://$TARGET_URL" 2>/dev/null | grep -iE "^(x-frame-options|x-content-type-options|strict-transport-security|content-security-policy|referrer-policy|permissions-policy):" || echo "لا توجد ترويسات أمان"
        fi
        echo ""
        echo "============================================"
        echo "نهاية التقرير - DMAR v$VERSION"
        echo "============================================"
    } > "$REPORT_FILE"
    
    echo -e "${G}[✓] تم حفظ التقرير في: $REPORT_FILE${NC}"
    echo ""
}

# ============ دالة الفحص الشامل ============
full_scan() {
    get_url
    echo -e "${Y}[+] بدء الفحص الشامل على: $TARGET_URL${NC}"
    echo ""
    sleep 1
    
    check_dns
    check_http
    check_ports
    check_security
    check_tech
    generate_report
    
    echo -e "${G}[✓] اكتمل الفحص الشامل${NC}"
    echo ""
    read -p "اضغط Enter للعودة..."
    main_menu
}

# ============ دالة الفحص السريع ============
quick_scan() {
    get_url
    echo -e "${Y}[+] بدء الفحص السريع...${NC}"
    echo ""
    sleep 1
    
    check_http
    
    echo -e "${G}[✓] اكتمل الفحص السريع${NC}"
    echo ""
    read -p "اضغط Enter للعودة..."
    main_menu
}

# ============ القائمة الرئيسية ============
main_menu() {
    show_banner
    echo -e "${Y}[${C}1${Y}] ${B}فحص شامل${NC}"
    echo -e "${Y}[${C}2${Y}] ${B}فحص سريع (HTTP/HTTPS فقط)${NC}"
    echo -e "${Y}[${C}3${Y}] ${B}فحص DNS فقط${NC}"
    echo -e "${Y}[${C}4${Y}] ${B}فحص المنافذ فقط${NC}"
    echo -e "${Y}[${C}5${Y}] ${B}معلومات الأداة${NC}"
    echo -e "${Y}[${C}0${Y}] ${B}خروج${NC}"
    echo ""
    echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    printf "${C}❯ اختر العملية: ${NC}"
    read CHOICE
    
    case $CHOICE in
        1)
            full_scan
            ;;
        2)
            quick_scan
            ;;
        3)
            get_url
            check_dns
            read -p "اضغط Enter للعودة..."
            main_menu
            ;;
        4)
            get_url
            check_ports
            read -p "اضغط Enter للعودة..."
            main_menu
            ;;
        5)
            show_banner
            echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${C}${BOLD}  معلومات الأداة${NC}"
            echo -e "${B}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo ""
            echo -e "${Y}الأداة:${W} DMAR${NC}"
            echo -e "${Y}الإصدار:${W} $VERSION${NC}"
            echo -e "${Y}المطور:${W} The Ghost${NC}"
            echo -e "${Y}المميزات:${NC}"
            echo -e "   ${G}• ${W}فحص DNS شامل${NC}"
            echo -e "   ${G}• ${W}فحص HTTP/HTTPS${NC}"
            echo -e "   ${G}• ${W}فحص المنافذ${NC}"
            echo -e "   ${G}• ${W}فحص الأمان${NC}"
            echo -e "   ${G}• ${W}فحص التقنيات${NC}"
            echo -e "   ${G}• ${W}توليد تقرير${NC}"
            echo ""
            read -p "اضغط Enter للعودة..."
            main_menu
            ;;
        0)
            clear
            echo -e "${G}${BOLD}شكراً لاستخدامك DMAR${NC}"
            exit 0
            ;;
        *)
            echo -e "${R}[!] اختيار غير صالح${NC}"
            sleep 1
            main_menu
            ;;
    esac
}

# ============ التشغيل ============
install_deps
main_menu
