$("#start").click(function() {
  if (localMediaStream) {
    var canvas = document.getElementById('canvas');
    //canvasの描画モードを2sに
    var ctx = canvas.getContext('2d');
    var img = document.getElementById('img');

    //videoの縦幅横幅を取得
    // var w = video.offsetWidth;
    // var h = video.offsetHeight;

    var w = Webcam.width;
    var h = Webcam.height;

    //同じサイズをcanvasに指定
    canvas.setAttribute("width", w);
    canvas.setAttribute("height", h);

    //canvasにコピー
    ctx.drawImage(video, 0, 0, w, h);
    //imgにjpg形式で書き出し
    img.src = canvas.toDataURL('image/jpg');
  }
});
