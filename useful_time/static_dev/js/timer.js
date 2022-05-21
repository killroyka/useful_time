var days, hours, minutes, seconds;

all_counters = document.querySelectorAll('.counter');
all_stop_counters = document.querySelectorAll('.counter_stop');
for (element of all_stop_counters) {
    element.dataset.time = String(Number(element.dataset.time) + 1);
    element.innerHTML = getTime(element.dataset.time);
}
Array.from(all_counters).forEach((element, index) => {
    element.dataset.time = String(Number(element.dataset.time) + 1)
    element.innerHTML = getTime(element.dataset.time);
});

setInterval(function () {
    Array.from(all_counters).forEach((element, index) => {
        element.dataset.time = String(Number(element.dataset.time) + 1)
        element.innerHTML = getTime(element.dataset.time);
    });
}, 1000);

function getTime(start_date) {

    var seconds = Number(start_date);

    days = parseInt(seconds / 86400);
    seconds = seconds % 86400;

    hours = parseInt(seconds / 3600);
    seconds = seconds % 3600;

    minutes = parseInt(seconds / 60);
    seconds = parseInt(seconds % 60);

    ans = ""
    if (days != 0) {
        ans += ' <span class="days">' + days + 'дн</span>'
    }
    if (hours != 0) {
        ans += ' <span class="hours">' + hours +
            ' ч</span>'
    }
    if (minutes != 0) {
        ans += ' <span class="minutes">' + minutes +
            ' мин</span>'
    }
    if (seconds != 0) {
        ans += ' <span class="seconds">' + seconds + ' сек</span>'
    }
    return ans;

};