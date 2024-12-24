#!/bin/bash

interface="eth0"

while true; do
    # Arayüzü kapat
    ifconfig $interface down > /dev/null 2>&1

    # MAC adresini rastgele değiştir
    macchanger --random $interface >/dev/null 2>&1

    # Arayüzü tekrar aç
    ifconfig $interface up >/dev/null 2>&1

    # DHCP sunucusundan IP al
    dhclient $interface >/dev/null 2>&1

    sleep 5
done
