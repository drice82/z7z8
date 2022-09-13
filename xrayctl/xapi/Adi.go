package xapi

import (
	"os/exec"
	"fmt"
)

func Adi() {
	cmd := exec.Command("/usr/local/bin/xray", "api", "adi", "--server=127.0.0.1:10085", "/app/tmp_inbounds.json")
	err := cmd.Run()
	if err != nil {
		fmt.Println("Adi failed with %s", err)
	}
}
