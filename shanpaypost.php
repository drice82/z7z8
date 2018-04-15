$data = '{
    "id": "17999030",
    "method": "sayHello",
    "jsonrpc": "2.0",
    "params": 
        {
            "acmac": "00E0614CA7C6",
            "acconf_version": "2015-10-28-09-45"
        }
    }';
$url = "http://wifi.doucube.com/index.php/interface/device/ConfHeartbeat.html";

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
