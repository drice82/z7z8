package xapi

import (
	"os/exec"
	"fmt"
)

func Rmi() {
	cmd := exec.Command("/usr/local/bin/xray", "api", "rmi", "--server=127.0.0.1:10085", "xtls", "vless", "vmess", "trojan")
	err := cmd.Run()
	if err != nil {
		fmt.Println("Rmi failed with %s", err)
	}
}
