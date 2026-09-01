#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

while true; do
    echo "======================================"
    echo -e "${CYAN}         BT-SPAM v1.0${NC}"
    echo -e "${CYAN}     أداة إرسال إشعارات Bluetooth${NC}"
    echo "======================================"
    echo ""
    echo "1) فحص الأجهزة القريبة"
    echo "2) استهداف جميع الأجهزة"
    echo "3) استهداف جهاز واحد"
    echo "4) عرض الإحصائيات"
    echo "5) إيقاف الإرسال"
    echo "6) خروج"
    echo ""
    echo -n "اختر: "
    read choice
    
    case $choice in
        1)
            bash /root/btspam/scan.sh
            ;;
        2)
            bash /root/btspam/spam.sh all
            ;;
        3)
            clear
            echo -e "${YELLOW}[*] الأجهزة المتاحة:${NC}"
            echo ""
            if [ -f /root/btspam/targets/devices.txt ]; then
                sort -u /root/btspam/targets/devices.txt | nl
                echo ""
                read -p "أدخل MAC Address: " mac
                bash /root/btspam/spam.sh "$mac"
            else
                echo -e "${RED}[!] لا توجد أجهزة — افحص أولاً${NC}"
            fi
            ;;
        4)
            bash /root/btspam/stats.sh
            ;;
        5)
            pkill -f "spam.sh" 2>/dev/null
            echo -e "${GREEN}[+] تم إيقاف الإرسال${NC}"
            ;;
        6)
            exit 0
            ;;
        *)
            echo -e "${RED}[!] خيار خاطئ${NC}"
            ;;
    esac
    
    echo ""
    read -p "اضغط Enter للمتابعة..."
    clear
done
