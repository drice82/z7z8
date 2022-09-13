package xapi

import (
	"fmt"
)

func RunQueryTraffic(email string) (u,d int64){
	var (
		xrayCtl *XrayController
		cfg     = &BaseConfig{
			APIAddress: "127.0.0.1",
			APIPort:    10085,
		}
	)
	xrayCtl = new(XrayController)
	err := xrayCtl.Init(cfg)
	defer xrayCtl.CmdConn.Close()
	if err != nil {
		fmt.Println("QueryTrafficFail, %s", err)
	}

	ptn := "user>>>" + email + ">>>traffic>>>uplink"
	u, err = queryTraffic(xrayCtl.SsClient, ptn, true)
	if err != nil {
		fmt.Println("QueryTrafficFail, %s", err)
	}
	ptn = "user>>>" + email + ">>>traffic>>>downlink"
	d, err = queryTraffic(xrayCtl.SsClient, ptn, true)
	if err != nil {
		fmt.Println("QueryTrafficFail, %s", err)
	}
	return u, d

}
