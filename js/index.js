// Loading画面
$('#Loading').fakeLoader({
  timeToHide:100000,
  zindex:999,
  spinner:'spinner7',
  bgColor:"#2bd9b4",
});


// Particleを出現させる
document.addEventListener('DOMContentLoaded', function () {
  particleground(document.getElementById('particles'), {
    dotColor: '#d9d1d1',
    lineColor: '#d9d1d1'
  });
  var intro = document.getElementById('intro');
  intro.style.marginTop = - intro.offsetHeight / 2 + 'px';
}, false);

function access_api(){
  $.ajax({
    url: 'http://172.21.39.178:5000/predict',
    dataType: 'json',

    success: function(responce) {
      if (responce.result = "OK") {
        console.log(responce.label);
        var label = responce.label;
        var name = responce.name;
        var probability = responce.probability;
        finish_loading();
        insert(label, name, probability);
      } else {
        console.log("API Mistake!!");
      }
    }
  })
}


function analysis(){
  $('#iterate').fadeIn("slow");

  // Ranking Effect
  var step = new TimelineMax();
  step.from('#three', 0.8, {'margin-left':'100%', autoAlpha:0});
  step.from('#three_img', 0.8, {autoAlpha:0});
  step.from('#three_name', 0.6, {autoAlpha:0});
  step.from('#three_sim', 0.6, {autoAlpha:0});

  step.from('#two', 0.8, {'margin-left':'100%', autoAlpha:0});
  step.from('#two_img', 0.8, {autoAlpha:0});
  step.from('#two_name', 0.6, {autoAlpha:0});
  step.from('#two_sim', 0.6, {autoAlpha:0});

  step.from('#one', 0.8, {'margin-left':'100%', autoAlpha:0});
  step.from('#one_img', 0.8, {autoAlpha:0});
  step.from('#one_name', 0.6, {autoAlpha:0});
  step.from('#one_sim', 0.6, {autoAlpha:0});

}


function insert(list, name, probability){
  $('#one_img').html("<img src=\"./img/" + list[0] + ".jpg\" height=\'150px\'>");
  $('#one_sim').text(probability[0] + ' %');
  $('#one_name').text(name[0]);
  $('#two_img').html("<img src=\"./img/" + list[1] + ".jpg\" height=\'150px\'>");
  $('#two_sim').text(probability[1] + ' %');
  $('#two_name').text(name[1]);
  $('#three_img').html("<img src=\"./img/" + list[2] + ".jpg\" height=\'150px\'>");
  $('#three_sim').text(probability[2] + ' %');
  $('#three_name').text(name[2]);
}


function finish_loading(){
  /*
  API読み取り完了後，fakeLoaderの実行時間を1に変更する
  */

  $('#Loading').fakeLoader({
    timeToHide:1,
  });
}


// Run function
access_api();
