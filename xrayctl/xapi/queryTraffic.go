package xapi

import (
	"context"
	statsService "github.com/xtls/xray-core/app/stats/command"
)

func queryTraffic(c statsService.StatsServiceClient, ptn string, reset bool) (traffic int64, err error) {
	traffic = -1
	resp, err := c.QueryStats(context.Background(), &statsService.QueryStatsRequest{
		// 这里是查询语句，例如 “user>>>love@xray.com>>>traffic>>>uplink” 表示查询用户 email 为 love@xray.com 在所有入站中的上行流量
		Pattern: ptn,
		// 是否重置流量信息(true, false)，即完成查询后是否把流量统计归零
		Reset_: reset, // reset traffic data everytime
	})
	if err != nil {
		return
	}
	// Get traffic data
	stat := resp.GetStat()
	// 判断返回 是否成功
	// 返回样例，value 值是我们需要的: [name:"inbound>>>proxy0>>>traffic>>>downlink" value:348789]
	if len(stat) != 0 {
		// 返回流量数据 byte
		traffic = stat[0].Value
	}

	return
}
