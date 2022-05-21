var days, hours, minutes, seconds;

all_counters = document.querySelectorAll('.counter');

Array.from(all_counters).forEach((element, index) => {
    element.dataset.time = String(Number(element.dataset.time) + 1)
    element.innerHTML = getTime(element.dataset.time);
});

setInterval( function () {
    Array.from(all_counters).forEach((element, index) => {
        element.dataset.time = String(Number(element.dataset.time) + 1)
        element.innerHTML = getTime(element.dataset.time);
    });
}, 1000);

function getTime(start_date) {

    var seconds = Number(start_date);
    console.log(seconds);

    days = parseInt(seconds / 86400);
    seconds = seconds % 86400;

    hours = parseInt(seconds / 3600);
    seconds = seconds % 3600;

    minutes = parseInt(seconds / 60);
    seconds = parseInt(seconds % 60);

    return '<span class="days">' + days +
     ' <b>дн</b></span> <span class="hours">' + hours +
      ' <b>ч</b></span> <span class="minutes">' + minutes +
      ' <b>мин</b></span> <span class="seconds">' + seconds + ' <b>сек</b></span>';

};