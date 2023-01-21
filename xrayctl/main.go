package main

import(
	"fmt"
	"time"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
	"crypto/md5"
	"encoding/hex"
	"os"
)


func main(){
	fmt.Println("Wait for 5s...")
	time.Sleep(time.Duration(5)*time.Second)
	fmt.Println("XrayCtl start")
	fmt.Println(time.Now())
	for {
		updateTraffic()
		renewClients()
		time.Sleep(time.Duration(150)*time.Second)
	}
}


func initDB() {
	ptn := os.Getenv("MYSQL_USERNAME") + ":" + os.Getenv("MYSQL_PWD") + "@tcp(" + os.Getenv("MYSQL_HOST") + ":" + os.Getenv("MYSQL_PORT") + ")/" + os.Getenv("MYSQL_DBNAME")
	database, err := sqlx.Open("mysql", ptn)
	if err != nil {
		fmt.Println("Open mysql failed,", err)
		return
	}

	Db = database
	//defer database.Close() // 注意这行代码要写在上面err判断的下面
}

func Md5(src string) string {
	m := md5.New()
	m.Write([]byte(src))
	res := hex.EncodeToString(m.Sum(nil))
	return res
}
