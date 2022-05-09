var days, hours, minutes, seconds;
var countdown = document.getElementById('counter');

setInterval(function (start_date) {

    // find the amount of "seconds" between now and target
    var current_date = new Date().getTime();
    var seconds = (current_date - start_date) / 1000;

    // do some time calculations
    days = parseInt(seconds / 86400);
    seconds = seconds % 86400;

    hours = parseInt(seconds / 3600);
    seconds = seconds % 3600;

    minutes = parseInt(seconds / 60);
    seconds = parseInt(seconds % 60);

    // format countdown string + set tag value
    countdown.innerHTML = '<span class="days">' + days +
     ' <b>День</b></span> <span class="hours">' + hours +
      ' <b>Час</b></span> <span class="minutes">' + minutes +
      ' <b>Минута</b></span> <span class="seconds">' + seconds + ' <b>Секунда</b></span>';

}, 1000);