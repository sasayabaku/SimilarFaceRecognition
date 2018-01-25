<?php
require('estimate.html');

//canvasデータがPOSTで送信されてきた場合
$canvas = $_POST["hidden_input"];

// ヘッダに「data:image/jpg;base64」がついているので，それは外す
$canvas = preg_replace("/data:[^,]+,/i","",$canvas);

// 残りのデータはbasa64エンコードされているので，デコードする
$canvas = base64_decode($canvas);

// まだ文字列の状態なので，画像リソース化
$image = imagecreatefromstring($canvas);

// 画像として保存
imagesavealpha($image, TRUE); // 透明色の有効
imagejpeg($image, './API/subject.jpg');
?>
