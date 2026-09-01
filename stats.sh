#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "======================================"
echo "         إحصائيات BT-SPAM"
echo "======================================"
echo ""

if [ -f /root/btspam/logs/stats.txt ]; then
    echo -e "${YELLOW}[*] سجل الإرسال:${NC}"
    echo ""
    echo "التاريخ | الإشعارات | الهدف"
    echo "--------------------------------------"
    cat /root/btspam/logs/stats.txt | tail -20
else
    echo -e "${RED}[!] لا توجد إحصائيات بعد${NC}"
fi

echo ""
echo -e "${YELLOW}[*] الأجهزة المكتشفة:${NC}"
if [ -f /root/btspam/targets/devices.txt ]; then
    sort -u /root/btspam/targets/devices.txt | nl
else
    echo "لا توجد أجهزة"
fi

echo ""

# إجمالي الإشعارات
total=$(awk -F'|' '{sum += $2} END {print sum}' /root/btspam/logs/stats.txt 2>/dev/null)
if [ -n "$total" ]; then
    echo -e "${GREEN}[+] إجمالي الإشعارات المرسلة: $total${NC}"
fi

echo ""
echo "======================================"
