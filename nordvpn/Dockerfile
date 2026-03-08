FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl gnupg ca-certificates iproute2 iptables procps dbus \
    && rm -rf /var/lib/apt/lists/*

# 导入 NordVPN
RUN curl -sSf https://repo.nordvpn.com/gpg/nordvpn_public.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/nordvpn.gpg \
    && echo "deb https://repo.nordvpn.com/deb/nordvpn/debian stable main" > /etc/apt/sources.list.d/nordvpn.list \
    && apt-get update \
    && apt-get install -y nordvpn \
    && rm -rf /var/lib/apt/lists/*

# --- 关键修复：伪装 systemctl ---
RUN echo '#!/bin/bash\nexit 0' > /usr/local/bin/systemctl && chmod +x /usr/local/bin/systemctl

RUN mkdir -p /run/nordvpn /var/lib/nordvpn

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]