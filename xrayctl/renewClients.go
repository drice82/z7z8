package main

import (
	"fmt"
	"time"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
	"encoding/json"
	"xrayctl/xapi"
	"encoding/base64"
)

type UserStruct struct {
	Id     int    `db:"id"`
	Email  string `db:"email"`
	Passwd string `db:"passwd"`
	Port   int    `db:"port"`
	Uuid   string `db:"uuid"`
}

type XtlsClientStruct struct {
	Email string `json:"email"`
	Id    string `json:"id"`
	Flow  string `json:"flow"`
}

type VmessClientStruct struct {
	Email string `json:"email"`
	Id    string `json:"id"`
}

type TrojanClientStruct struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type ShadowsocksClientStruct struct {
	Email	string `json:"email"`
	Password	string	`json:password"`
}

var Db *sqlx.DB
var User []UserStruct
var OldUserMd5 string

func renewClients() {
	initDB()
	var xtlsTemp XtlsClientStruct
	var xtlsClient []XtlsClientStruct
	var trojanTemp TrojanClientStruct
	var trojanClient []TrojanClientStruct
	var vmessTemp VmessClientStruct
	var vmessClient []VmessClientStruct
	var shadowsocksTemp ShadowsocksClientStruct
	var shadowsocksClient []ShadowsocksClientStruct
	var NewUserMd5 string

	err := Db.Select(&User, "select id, email, passwd, port, uuid from users where enable=1")
	if err != nil {
		fmt.Println("Exec select failed, ", err)
		return
	}
	defer Db.Close()

	for _, v := range User {
		xtlsTemp.Email = v.Email
		xtlsTemp.Id = v.Uuid
		xtlsTemp.Flow = "xtls-rprx-direct"

		trojanTemp.Email = v.Email
		trojanTemp.Password = v.Passwd + strconv.Itoa(v.Port)
		vmessTemp.Email = v.Email
		vmessTemp.Id = v.Uuid
		shadowsocksTemp.Email = v.Email
		shadowsocksTemp.Password = base64.StdEncoding.EncodeToString([]byte(Md5(v.Passwd + strconv.Itoa(v.Port))))

		xtlsClient = append(xtlsClient, xtlsTemp)
		trojanClient = append(trojanClient, trojanTemp)
		vmessClient = append(vmessClient, vmessTemp)
		shadowsocksClient = append(shadowsocksClient, shadowsocksTemp)
		NewUserMd5 = NewUserMd5 + v.Passwd
	}

	NewUserMd5 = Md5(NewUserMd5)
	if NewUserMd5 != OldUserMd5 {
		//read the json file
		var jsonPath string
		if os.Getenv("ENABLED_SS") == "1" {
			jsonPath = "/app/xtls_and_ss_inbounds.json"
		} else {
			jsonPath = "/app/xtls_inbounds.json"
		}
		jsonFile, err := os.Open(jsonPath)
		if err != nil {
			fmt.Println("Read json error, ", err)
			return
		}
		defer jsonFile.Close()
		byteValue, _ := ioutil.ReadAll(jsonFile)
		strValue := string(byteValue)

		//replace the Clients
		jsonByte, _:= json.MarshalIndent(xtlsClient, "", "	")
		strValue = strings.Replace(strValue, `"__replace__":"xtls"`, string(jsonByte), 1)

		jsonByte, _ = json.MarshalIndent(trojanClient, "", "	")
		strValue = strings.Replace(strValue, `"__replace__":"trojan"`, string(jsonByte), 1)

		jsonByte, _ = json.MarshalIndent(vmessClient, "", "	")
		strValue = strings.Replace(strValue, `"__replace__":"vmess_and_vless"`, string(jsonByte), 2)

		if os.Getenv("ENABLED_SS") == "1" {
			jsonByte, _ = json.MarshalIndent(shadowsocksClient, "", "	")
			strValue = strings.Replace(strValue, `"__replace__":"shadowsocks"`, string(jsonByte), 1)
		}

		//write the json file
		jsonFile, err = os.Create("/app/tmp_inbounds.json")
		if err != nil {
			fmt.Println("Write json erros, ", err)
			return
		}
		defer jsonFile.Close()
		jsonFile.WriteString(strValue)
		OldUserMd5 = NewUserMd5
		xapi.Rmi()
		xapi.Adi()
		fmt.Print("Renew Clients ")
		fmt.Println (time.Now())
	}
}
