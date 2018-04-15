<?php
$partner = $_POST["partner"];
$user_seller = $_POST["user_seller"];
$out_order_no = $_POST["out_order_no"];
$subject = $_POST["subject"];
$total_fee = $_POST["total_fee"];
$body = $_POST["body"];
$notify_url = $_POST["notify_url"];
$return_url = $_POST["return_url"];
$sign = $_POST["sign"];

$data = '{
    "partner": $partner,
    "user_seller": $user_seller,
    "out_order_no": $out_order_no,
    "subject": $subject,
    "total_fee": $total_fee,
    "body": $body,
    "notify_url": $notify_url,
    "return_url": $return_url,
    "sign": $sign
    }';
$url = "http://payment.passpay.net/PayOrder/payorder";

$res = http_request($url, $data);

var_dump($res);

//HTTP请求（支持HTTP/HTTPS，支持GET/POST）
function http_request($url, $data = null)
{
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, FALSE);
    if (!empty($data)){
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
    }
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, TRUE);
    $output = curl_exec($curl);
    curl_close($curl);
    return $output;
}

?>
