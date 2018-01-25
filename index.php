<?php


$file = new SplFileObject('./result.csv');
$file->setFlags(SplFileObject::READ_CSV);
foreach ($file as $line) {
  $records[] = $line;
}


require('test.html');
?>
