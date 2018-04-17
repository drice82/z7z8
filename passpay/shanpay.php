<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>支付跳转中...</title>
</head>
<?php
require_once("shanpayfunction.php");


$shan_config['key']			= '0f6397bc5553459786deb92b37f7';
/**************************请求参数**************************/
$partner = $_POST["partner"];
$user_seller = $_POST["user_seller"];
$out_order_no = $_POST["out_order_no"];
$subject = $_POST["subject"];
$total_fee = $_POST["total_fee"];
$body = $_POST["body"];
$notify_url = $_POST["notify_url"];
$return_url = $_POST["return_url"];


/************************************************************/

//构造要请求的参数数组，无需改动
$parameter = array(
		"partner" => $partner,
        "user_seller"  => $user_seller,
		"out_order_no"	=> $out_order_no,
		"subject"	=> $subject,
		"total_fee"	=> $total_fee,
		"body"	=> $body,
		"notify_url"	=> $notify_url,
		"return_url"	=> $return_url
);

//建立请求
$html_text = buildRequestFormShan($parameter, $shan_config['key']);
echo $html_text;


?>
</body>
</html>
