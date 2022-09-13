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

var Db *sqlx.DB
var User []UserStruct
var OldUserMd5 string

func renewClients() {

	initDB()
	var xtlsTemp XtlsClientStruct
	var xtlsClient []XtlsClientStruct
	var TrojanTemp TrojanClientStruct
	var TrojanClient []TrojanClientStruct
	var VmessTemp VmessClientStruct
	var VmessClient []VmessClientStruct
	var NewUserMd5 string
	err := Db.Select(&User, "select id, email, passwd, port, uuid from user where enable=1 and u+d<transfer_enable")
	if err != nil {
		fmt.Println("Exec select failed, ", err)
	}
	defer Db.Close()

	for _, v := range User {
		xtlsTemp.Email = v.Email
		xtlsTemp.Id = v.Uuid
		xtlsTemp.Flow = "xtls-rprx-direct"

		TrojanTemp.Email = v.Email
		TrojanTemp.Password = v.Passwd + strconv.Itoa(v.Port)
		VmessTemp.Email = v.Email
		VmessTemp.Id = v.Uuid
		xtlsClient = append(xtlsClient, xtlsTemp)
		TrojanClient = append(TrojanClient, TrojanTemp)
		VmessClient = append(VmessClient, VmessTemp)
		NewUserMd5 = NewUserMd5 + v.Passwd
	}

	NewUserMd5 = Md5(NewUserMd5)
	if NewUserMd5 != OldUserMd5 {
		//read the json file
		jsonFile, err := os.Open("/app/xtls_inbounds.json")
		checkErr(err)
		defer jsonFile.Close()
		byteValue, _ := ioutil.ReadAll(jsonFile)
		strValue := string(byteValue)

		//replace the Clients
		jsonByte, err := json.MarshalIndent(xtlsClient, "", "	")
		strValue = strings.Replace(strValue, `"__replace__":"xtls"`, string(jsonByte), 1)

		jsonByte, err = json.MarshalIndent(TrojanClient, "", "	")
		strValue = strings.Replace(strValue, `"__replace__":"trojan"`, string(jsonByte), 1)

		jsonByte, err = json.MarshalIndent(VmessClient, "", "	")
		strValue = strings.Replace(strValue, `"__replace__":"vmess_and_vless"`, string(jsonByte), 2)

		//write the json file
		jsonFile, err = os.Create("/app/tmp_inbounds.json")
		checkErr(err)
		defer jsonFile.Close()
		jsonFile.WriteString(strValue)
		OldUserMd5 = NewUserMd5
		xapi.Rmi()
		xapi.Adi()
		fmt.Print("Renew Clients ")
		fmt.Println (time.Now())
	}
}
