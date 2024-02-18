#!/bin/bash
IPTABLES="iptables"
INTERNET_IF="vmbr0"
INTRANET_IF="vmbr1"
PUBLIC_IP="37.187.75.17"
VM_NET="10.10.10.0/24"
WEB_SERVER1="10.10.10.100"
WIN_SERVER="10.10.10.101"
HAP_SERVER="10.10.10.102"

start()
{
### NAT out
  echo 1 > /proc/sys/net/ipv4/ip_forward
  $IPTABLES -t nat -A POSTROUTING -s $VM_NET -o $INTERNET_IF -j MASQUERADE
  $IPTABLES -t raw -I PREROUTING -i fwbr+ -j CT --zone 1

### Port forwarding
### Web
# Internet
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 10022 -j DNAT --to-destination $WEB_SERVER1:22
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 80 -j DNAT --to-destination $WEB_SERVER1:80
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 443 -j DNAT --to-destination $WEB_SERVER1:443
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 8082 -j DNAT --to-destination $WIN_SERVER:3389
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 10222 -j DNAT --to-destination $HAP_SERVER:22
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 9090 -j DNAT --to-destination $HAP_SERVER:9090
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 8088 -j DNAT --to-destination $HAP_SERVER:8088
  $IPTABLES -t nat -A PREROUTING -i $INTERNET_IF -p tcp -m tcp --dport 5555 -j DNAT --to-destination $HAP_SERVER:5555
# VMNET - specify dest otherwise all traffic is redirected to this VM which we don't want
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 10022 -j DNAT --to-destination $WEB_SERVER1:22
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 80 -j DNAT --to-destination $WEB_SERVER1:80
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 443 -j DNAT --to-destination $WEB_SERVER1:443
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 8082 -j DNAT --to-destination $WIN_SERVER:3389
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 10222 -j DNAT --to-destination $HAP_SERVER:22
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 9090 -j DNAT --to-destination $HAP_SERVER:9090
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 8088 -j DNAT --to-destination $HAP_SERVER:8088
  $IPTABLES -t nat -A PREROUTING -i $INTRANET_IF -d $PUBLIC_IP  -p tcp -m tcp --dport 5555 -j DNAT --to-destination $HAP_SERVER:5555
# Host
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 10022 -j DNAT --to-destination $WEB_SERVER1:22
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 80 -j DNAT --to-destination $WEB_SERVER1:80
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 443 -j DNAT --to-destination $WEB_SERVER1:443
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 8082 -j DNAT --to-destination $WIN_SERVER:3389
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 10222 -j DNAT --to-destination $HAP_SERVER:22
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 9090 -j DNAT --to-destination $HAP_SERVER:9090
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 8088 -j DNAT --to-destination $HAP_SERVER:8088
  $IPTABLES -t nat -A OUTPUT -d $PUBLIC_IP -p tcp -m tcp --dport 5555 -j DNAT --to-destination $HAP_SERVER:5555

}

stop()
{
### NAT out
 echo 0 > /proc/sys/net/ipv4/ip_forward
 $IPTABLES -t nat -F
 $IPTABLES -t nat -X
 $IPTABLES -t mangle -F
 $IPTABLES -t mangle -X
 $IPTABLES -t raw -F
 $IPTABLES -t raw -X
}


case "$1" in
  start)
   start
   exit $?
   ;;
  stop)
   stop
   exit $?
   ;;
  *)
   echo "Unrecognized input. Supported options: start, stop"
   exit 1
   ;;
esac
