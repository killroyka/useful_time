var days, hours, minutes, seconds;

all_counters = document.querySelectorAll('.counter');
all_stop_counters = document.querySelectorAll('.counter_stop');
all_timepoint = document.querySelectorAll(".timepoint")
var diff_UTC_time = new Date().getTimezoneOffset() * 60
console.log(all_timepoint)

Array.from(all_timepoint).forEach((element, index) => {
    console.log(new Date(element.dataset.time).getTime())
    var time_with_timezone = new Date().setTime(new Date(element.dataset.time).valueOf() + (diff_UTC_time * 1000));
    console.log(time_with_timezone)
    element.innerHTML = String(new Date().setTime(time_with_timezone).toString());
});
console.log(all_timepoint)
Array.from(all_stop_counters).forEach((element, index) => {
    element.dataset.time = String(Number(element.dataset.time) + 1);
    element.innerHTML = getTime(element.dataset.time);
    localStorage.setItem(element.dataset.id, "0")
});
Array.from(all_counters).forEach((element, index) => {
    element.dataset.time = String(Number(element.dataset.time) +
        Number(localStorage.getItem(element.dataset.id)))
    element.innerHTML = getTime(element.dataset.time);
});

setInterval(function () {
    Array.from(all_counters).forEach((element, index) => {
        element.dataset.time = String(Number(element.dataset.time) + 1)
        element.innerHTML = getTime(element.dataset.time);
        localStorage.setItem(element.dataset.id, String(1 + Number(localStorage.getItem(element.dataset.id))))
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
