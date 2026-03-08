#!/bin/bash

# --- 1. 环境清理与预设 ---
chattr -i /etc/resolv.conf || true
rm -rf /run/nordvpn/nordvpnd.sock /run/nordvpn/nordvpnd.pid /run/dbus/pid
rm -rf /var/run/dbus/*
mkdir -p /var/run/dbus /run/nordvpn

echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 1.1.1.1" >> /etc/resolv.conf
chattr -i /etc/resolv.conf || true

# --- 2. 启动核心守护进程 ---
dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address > /dev/null 2>&1

echo "Starting NordVPN daemon (logs suppressed)..."
# 将守护进程日志重定向到文件，避免污染 docker logs
/usr/sbin/nordvpnd > /var/log/nordvpnd.log 2>&1 &

for i in {1..10}; do
    [ -S /run/nordvpn/nordvpnd.sock ] && break
    sleep 1
done

# --- 3. 自动化配置与登录 ---
echo "Configuring NordVPN settings..."
yes y | nordvpn set analytics off > /dev/null
nordvpn set technology nordlynx > /dev/null
nordvpn set killswitch on > /dev/null
nordvpn set notify off > /dev/null

if ! nordvpn account | grep -q "Email"; then
    echo "Logging in with token..."
    nordvpn login --token "${NORDVPN_TOKEN}" > /dev/null
fi

echo "Setting whitelists for ports 18088, 18188, 18288..."
nordvpn whitelist add port 18088 > /dev/null
nordvpn whitelist add port 18188 > /dev/null
nordvpn whitelist add port 18288 > /dev/null

# --- 4. 建立连接 ---
echo "Connecting to ${CONNECT_TO}..."
nordvpn connect "${CONNECT_TO}" | grep -E "Connecting|Connected|Welcome"

# 等待网卡初始化并解除 resolv.conf 锁定
sleep 2
chattr -i /etc/resolv.conf || true

# 自动检测当前使用的 VPN 网卡名称 (nordlynx 或 tun0)
VPN_IFACE=$(ip addr | grep -E 'nordlynx|tun0' | awk -F': ' '{print $2}' | head -n 1 | cut -d'@' -f1)

echo "NordVPN setup complete. Interface: ${VPN_IFACE:-None}"
if [ -n "$VPN_IFACE" ]; then
    echo "Output IP:"
    curl -s --interface "$VPN_IFACE" ifconfig.me || echo "Failed to fetch IP via $VPN_IFACE"
fi

# --- 5. 增强型自愈监控循环 ---
(
    while true; do
        sleep 120 # 每2分钟检查一次
        
        # 检查 A: 守护进程进程是否存在
        if ! pgrep -x "nordvpnd" > /dev/null; then
            echo "[Health] Daemon crashed! Restarting..."
            /usr/sbin/nordvpnd > /var/log/nordvpnd.log 2>&1 &
            sleep 5
        fi

        # 检查 B: 逻辑连接状态
        STATUS=$(nordvpn status | grep "Status" | cut -d ':' -f 2 | xargs)
        if [ "$STATUS" != "Connected" ]; then
            echo "[Health] VPN disconnected (Status: $STATUS). Reconnecting..."
            nordvpn connect "${CONNECT_TO}" > /dev/null
            chattr -i /etc/resolv.conf || true
            continue
        fi

        # 重新确认网卡名（防止重连后网卡名变动）
        CURRENT_IFACE=$(ip addr | grep -E 'nordlynx|tun0' | awk -F': ' '{print $2}' | head -n 1 | cut -d'@' -f1)

        # 检查 C: 物理链路深度探测
        if [ -n "$CURRENT_IFACE" ]; then
            PROBE_SUCCESS=false
            for i in {1..3}; do
                # 使用 IP (1.1.1.1) 探测，避开 DNS 干扰
                if curl -s --interface "$CURRENT_IFACE" --connect-timeout 15 http://1.1.1.1 > /dev/null; then
                    PROBE_SUCCESS=true
                    break
                fi
                echo "[Health] Probe via $CURRENT_IFACE failed, retrying ($i/3)..."
                sleep 5
            done

            if [ "$PROBE_SUCCESS" = false ]; then
                echo "[Health] Tunnel $CURRENT_IFACE is unresponsive. Resetting..."
                nordvpn disconnect > /dev/null
                sleep 2
                nordvpn connect "${CONNECT_TO}" > /dev/null
                chattr -i /etc/resolv.conf || true
            fi
        else
            echo "[Health] Warning: No VPN interface detected. Attempting reconnect..."
            nordvpn connect "${CONNECT_TO}" > /dev/null
        fi
    done
) &

# --- 6. 阻塞主进程 ---
echo "Monitoring active. Container is ready."
while true; do
    sleep 1 & wait $!
done