#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "[*] فحص أجهزة Bluetooth..."
echo ""

# تفعيل البلوتوث
hciconfig hci0 up 2>/dev/null
bluetoothctl power on 2>/dev/null

# فحص الأجهزة
echo "[*] جاري الفحص لمدة 15 ثانية..."
timeout 15 hcitool scan 2>/dev/null | while read line; do
    mac=$(echo "$line" | awk '{print $1}')
    name=$(echo "$line" | awk '{$1=""; print $0}' | sed 's/^ *//')
    
    if [ -n "$mac" ] && [ ${#mac} -eq 17 ]; then
        echo -e "${GREEN}[+] جهاز:${NC} $name"
        echo -e "    MAC: $mac"
        echo ""
        echo "$mac|$name" >> /root/btspam/targets/devices.txt
    fi
done

# عرض الأجهزة المحفوظة
if [ -f /root/btspam/targets/devices.txt ]; then
    echo -e "${YELLOW}[*] الأجهزة المكتشفة:${NC}"
    sort -u /root/btspam/targets/devices.txt | nl
fi

echo ""
echo "[+] الفحص اكتمل"
