
代理机放本文件夹的程序，并配置id，密钥等
whmcs正常安装，编辑shanpay.php,修改提交地址：
####
$sHtml = "<form id='paysubmit' name='paysubmit' action='http://www.xxx.net/whmcs/shanpay.php' accept-charset='utf-8' method='POST'>";
