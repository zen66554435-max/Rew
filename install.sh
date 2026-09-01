#!/bin/bash

echo "[*] تثبيت BT-SPAM..."
echo ""

if command -v apt > /dev/null 2>&1; then
    apt update -y
    apt install -y bluez bluez-tools bluetooth hcitool l2ping obexftp
elif command -v apk > /dev/null 2>&1; then
    apk update
    apk add bluez bluez-deprecated bluez-tools
else
    echo "[!] نظام غير مدعوم"
    exit 1
fi

mkdir -p /root/btspam/logs
mkdir -p /root/btspam/targets

echo "[+] تم التثبيت"
