package xapi

import (
	"os/exec"
	"fmt"
	"os"
)

func Rmi() {
	if  os.Getenv("ENABLED_SS") == "1" {
		cmd := exec.Command("/usr/local/bin/xray", "api", "rmi", "--server=127.0.0.1:10085", "xtls", "vless", "vmess", "trojan", "shadowsocks")
		err := cmd.Run()
		if err != nil {
			fmt.Println("Rmi failed", err)
		}
	} else {
		cmd := exec.Command("/usr/local/bin/xray", "api", "rmi", "--server=127.0.0.1:10085", "xtls", "vless", "vmess", "trojan")
		err := cmd.Run()
		if err != nil {
			fmt.Println("Rmi failed", err)
		}
	}
}
