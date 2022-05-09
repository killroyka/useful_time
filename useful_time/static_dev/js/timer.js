var days, hours, minutes, seconds;

all_counters = document.querySelectorAll('.counter');

setInterval( function () {
    Array.from(all_counters).forEach((element, index) => {
        element.innerHTML = getTime(new Date((Number(element.dataset.start) - 3600 * 3) * 1000 ))
    });
}, 1000);

function getTime(start_date) {

    var current_date = new Date();
    var seconds = (current_date - start_date) / 1000;

    days = parseInt(seconds / 86400);
    seconds = seconds % 86400;

    hours = parseInt(seconds / 3600);
    seconds = seconds % 3600;

    minutes = parseInt(seconds / 60);
    seconds = parseInt(seconds % 60);

    return '<span class="days">' + days +
     ' <b>День</b></span> <span class="hours">' + hours +
      ' <b>Час</b></span> <span class="minutes">' + minutes +
      ' <b>Минута</b></span> <span class="seconds">' + seconds + ' <b>Секунда</b></span>';

};