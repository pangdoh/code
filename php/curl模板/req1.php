<?php

function post($url,$post_data=null,$ua=''){
    //解析url
    $ss = explode("://",$url);
    $protocol = $ss[0];
    if(strpos($ss[1],"/")) {
        $host = substr($ss[1],0,strpos($ss[1],"/"));
        $path = substr($ss[1],strpos($ss[1],"/"));
        if(strpos($ss[1],"?")){
            if(strpos($ss[1],"/") > strpos($ss[1],"?")){
                $host = substr($ss[1],0,strpos($ss[1],"?"));
                $path = substr($ss[1],strpos($ss[1],"?"));
            }
        }
    }elseif(strpos($ss[1],"?")){
        $host = substr($ss[1],0,strpos($ss[1],"?"));
        $path = substr($ss[1],strpos($ss[1],"?"));
    }else {
        $host = $ss[1];
        $path = "/";
    }

    print_r("protocol:$protocol");
    print "\r\n";
    print_r("host:$host");
    print "\r\n";
    print_r("path:$path");
    print "\r\n";

    //配置默认信息
    if($ua == ''){
        $ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36';
    }

    //设置请求头
    $headers = array(
        'Host: '.$host,
        'Connection: '.'keep-alive',
        'Upgrade-Insecure-Requests: '.'1',
        'User-Agent: '.$ua,
        'Accept: '.'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language: '.'en-US,en;q=0.9',
        'Accept-Encoding: '.'gzip, deflate'
    );
    //初始化
    $curl = curl_init();
    //设置抓取的url
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    //设置获取的信息，如果设为0，则直接输出响应而不返回字符串内容。
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    //设置post方式提交
    curl_setopt($curl, CURLOPT_POST, 1);
    //设置post数据
//    $post_data = array(
//        "wd" => "杨幂"
//    );
    curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
    //设置超时时间
    curl_setopt($curl, CURLOPT_TIMEOUT, 10);
    //执行并接受响应
    $data = curl_exec($curl);
    //关闭URL连接
    curl_close($curl);
    //返回响应信息
    return $data;
}

function get($url,$ua=''){
    //解析url
    $ss = explode("://",$url);
    $protocol = $ss[0];
    if(strpos($ss[1],"/")) {
        $host = substr($ss[1],0,strpos($ss[1],"/"));
        $path = substr($ss[1],strpos($ss[1],"/"));
        if(strpos($ss[1],"?")){
            if(strpos($ss[1],"/") > strpos($ss[1],"?")){
                $host = substr($ss[1],0,strpos($ss[1],"?"));
                $path = substr($ss[1],strpos($ss[1],"?"));
            }
        }
    }elseif(strpos($ss[1],"?")){
        $host = substr($ss[1],0,strpos($ss[1],"?"));
        $path = substr($ss[1],strpos($ss[1],"?"));
    }else {
        $host = $ss[1];
        $path = "/";
    }

    print_r("protocol:$protocol");
    print "\r\n";
    print_r("host:$host");
    print "\r\n";
    print_r("path:$path");
    print "\r\n";

    //配置默认信息
    if($ua == ''){
        $ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36';
    }

    //设置请求头
    $headers = array(
        'Host: '.$host,
        'Connection: '.'keep-alive',
        'Upgrade-Insecure-Requests: '.'1',
        'User-Agent: '.$ua,
        'Accept: '.'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language: '.'en-US,en;q=0.9',
        'Accept-Encoding: '.'gzip, deflate'
    );

    //初始化
    $curl = curl_init();
    //设置抓取的url
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    //设置头文件的信息作为数据流输出
    curl_setopt($curl, CURLOPT_HEADER, 1);
    //设置获取的信息以文件流的形式返回，而不是直接输出。
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    //执行命令
    $data = curl_exec($curl);
    //关闭URL请求
    curl_close($curl);
    //返回响应信息
    return $data;
}

$url = "http://39.106.153.182";
$post_data = array(
    "wd" => "杨幂"
);
//post($url);
get($url);