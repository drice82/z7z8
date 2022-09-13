package main

import (
	"time"
	"fmt"
	"xrayctl/xapi"

	_ "github.com/go-sql-driver/mysql"
)

func updateTraffic() {
	t := time.Now().Unix()
	var u, d int64
	initDB()
	for _, v := range User {
		u, d = xapi.RunQueryTraffic(v.Email)
		if u+d >0 {
			_, err := Db.Exec("update user set u=u+?, d=d+?, t=? where id=?", u, d, t, v.Id)
			if err != nil {
				fmt.Println("Update traffic failed, ", err)
			}
		}
	}
	Db.Close()
}
