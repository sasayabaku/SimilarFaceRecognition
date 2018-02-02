// Loading
$('#Loading').fakeLoader({
  timeToHide:1000000,
  zindex:999,
  spinner:'spinner7',
  bgColor:"#2bd9b4",
});

$(function(){
  $.ajax({
    url: 'http://172.21.39.178:5000/age_gender_predict',
    dataType: 'json',

    success: function(responce) {
      if (responce.result = "OK") {
        console.log(responce.men);
        var age = responce.age;
        var man = responce.men;
        var woman = responce.women;
        finish_loading();
        insert(age, man, woman);
      } else {
        console.log("API Mistake!");
      }
    }
  });
});

function insert(age, man, woman){
  $('#estimate_age').text(age);
  shuffle_num();
  draw_gender_graph(man, woman);
}

function finish_loading(){
  /*
  API読み取り完了後，fakeLoaderの実行時間を1に変更する
  */
  
  $('#Loading').fakeLoader({
    timeToHide:1,
  });
}

// 数字に　シャッフルするエフェクトをかける (class shuffle)
function shuffle_num(){

    var shuffleElm = $('.shuffle'),
    shuffleSpeed = 10,
    shuffleAnimation = 20,
    shuffleDelay = 100;

    shuffleElm.each(function(){
        var self = $(this);

        self.wrapInner('<span class="shuffleWrap"></span>');

        var shuffleWrap = self.find('.shuffleWrap');
        shuffleWrap.replaceWith(shuffleWrap.text().replace(/(\S)/g, '<span class="shuffleNum">$&</span>'));

        var shuffleNum = self.find('.shuffleNum'),
        numLength = shuffleNum.length;

        shuffleNum.each(function(i){
            var selfNum = $(this),
            thisNum = selfNum.text(),
            shuffleTimer;

            function timer(){
                shuffleTimer = setInterval(function(){
                    rdm = Math.floor(Math.random()*(9))+1;
                    selfNum.text(rdm);
                },shuffleSpeed);
            }
            timer();

            var i = -i + numLength;

            setTimeout(function(){
                clearInterval(shuffleTimer);
                selfNum.text(thisNum);
            },shuffleAnimation + (i*shuffleDelay));
        });
        self.css({visibility:'visible'});
    });
  };

// 性別のグラフ描画 by Chart.JS
function draw_gender_graph(man, woman){

  data = {
    datasets: [{
      data: [man * 100, woman * 100],
      backgroundColor: ['#5aace3', '#f07f1c']
    }],

    labels:['Men', 'Women']
  }

  var ctx = document.getElementById("doughnutChart").getContext('2d');

  var myDoughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: {
      legend: {
        display: false,
        onHover: true,
        borderWidth: 0
      }
    }
  });

};
