var days, hours, minutes, seconds;

all_counters = document.querySelectorAll('.counter');
all_stop_counters = document.querySelectorAll('.counter_stop');
all_timepoint = document.querySelectorAll(".timepoint")
var diff_UTC_time = new Date().getTimezoneOffset() * 60
var a = new Date(value = new Date(all_timepoint[0].dataset.time).getTime())
Array.from(all_timepoint).forEach((element, index) => {
    var date = new Date(value = new Date(element.dataset.time).getTime())
    console.log(date.toDateString())
    if (element.classList[1] === "start") {
        element.innerHTML = "Время первого начала: " + date.toDateString() + " " + date.toLocaleTimeString()
    } else if (element.classList[1] === "end") {
        element.innerHTML = "Время конца: " + date.toDateString() + " " + date.toLocaleTimeString()
    } else if (element.classList[1] === "sub-start") {
        element.innerHTML = "Время начала: " + date.toLocaleTimeString()
    } else if (element.classList[1] === "sub-end") {
        element.innerHTML = "Время конца: " + date.toLocaleTimeString()
    }
});
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
