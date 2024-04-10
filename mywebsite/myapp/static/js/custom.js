$("#accordion").on("hide.bs.collapse show.bs.collapse", e => {
	$(e.target)
	  .prev()
	  .find("i:last-child")
	  .toggleClass("fa-minus fa-plus");
});
$(".nav-link").click(function(){
	$(".dropdown__menu__box").toggle();
});
$('.trader-slider').owlCarousel({
    loop:true,
    margin:14,
    autoplay:true,
    autoplayTimeout:2500,
    autoplayHoverPause:true,
    responsive:{
        0:{
            items:1,
            nav:true
        },
        600:{
            items:1,
            nav:true
        },
        700:{
            items:1,
            nav:true
        },
        1000:{
            items:2,
            nav:true,
            loop:true
        }
    }
})


var barCount = 60;
var initialDateStr = '01 Apr 2017 00:00 Z';

var ctx = document.getElementById('chart').getContext('2d');
ctx.canvas.width = 800;
ctx.canvas.height = 400;

var barData = getRandomData(initialDateStr, barCount);
function lineData() { return barData.map(d => { return { x: d.x, y: d.c} }) };

var chart = new Chart(ctx, {
	type: 'candlestick',
	data: {
		datasets: [{
			label: 'CHRT - a random curve',
			data: barData
		}]
	}
});

var getRandomInt = function(max) {
	return Math.floor(Math.random() * Math.floor(max));
};

function randomNumber(min, max) {
	return Math.random() * (max - min) + min;
}

function randomBar(date, lastClose) {
	var open = +randomNumber(lastClose * 0.95, lastClose * 1.05).toFixed(2);
	var close = +randomNumber(open * 0.95, open * 1.05).toFixed(2);
	var high = +randomNumber(Math.max(open, close), Math.max(open, close) * 1.1).toFixed(2);
	var low = +randomNumber(Math.min(open, close) * 0.9, Math.min(open, close)).toFixed(2);
	return {
		x: date.valueOf(),
		o: open,
		h: high,
		l: low,
		c: close
	};

}

function getRandomData(dateStr, count) {
	var date = luxon.DateTime.fromRFC2822(dateStr);
	var data = [randomBar(date, 30)];
	while (data.length < count) {
		date = date.plus({days: 1});
		if (date.weekday <= 5) {
			data.push(randomBar(date, data[data.length - 1].c));
		}
	}
	return data;
}

var update = function() {
	var dataset = chart.config.data.datasets[0];
  
  // put datas in chart
	// mixed charts
	var mixed = document.getElementById('mixed').value;
	if(mixed === 'true') {
		chart.config.data.datasets = [
			{
				label: 'CHRT - a random curve',
				data: barData
			},
			{
				label: 'Close price',
				type: 'line',
				data: lineData()
			}	
		]
	}
  // not mixed charts
	else {
		chart.config.data.datasets = [
			{
				label: 'CHRT - a random curve',
				data: barData
			}	
		]
	}

	chart.update();
};

document.getElementById('update').addEventListener('click', update);

document.getElementById('randomizeData').addEventListener('click', function() {
	barData = getRandomData(initialDateStr, barCount);
	update();
});