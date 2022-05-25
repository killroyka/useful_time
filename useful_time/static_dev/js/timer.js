var days, hours, minutes, seconds;

// Собирает все элементы, храняшие данные о продолжительности обьектов, которые все еще продолжаются
all_counters = document.querySelectorAll('.counter');
// Собирает все элементы, храняшие данные о продолжительности остановившихся таймеров
all_stop_counters = document.querySelectorAll('.counter_stop');
// Собирает все элементы, храняшие данные о датах
all_timepoint = document.querySelectorAll(".timepoint")

// Метод получет длину промежутка времени в секундах и возвращает время в "красивом" виде
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

// Этот блок кода нужен, чтоб время по UTC переводилось во время пользователя
Array.from(all_timepoint).forEach((element, index) => {
    // Мы создаем обьект Date который переводит время с UTC на время пользователя
    var date = new Date(element.dataset.time)
    // меняем информацию о обьекто в зависимости от его классов
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
// присваивает всем остановленным таймерам красивую продолжительность
Array.from(all_stop_counters).forEach((element, index) => {
    element.dataset.time = String(Number(element.dataset.time) + 1);
    element.innerHTML = getTime(element.dataset.time);
});
// присваивает всем не остановленным таймерам красивую продолжительность
Array.from(all_counters).forEach((element, index) => {
    element.dataset.time = String((new Date().getTime() - new Date(element.dataset.startpoint_last_sub_record).getTime() + element.dataset.longitude * 1000) / 1000)
    element.innerHTML = getTime(element.dataset.time);
});
// обновляет данные таймеров каждую секунду
setInterval(function () {
    Array.from(all_counters).forEach((element, index) => {
        element.dataset.time = String(Number(element.dataset.time) + 1)
        element.innerHTML = getTime(element.dataset.time);
    });
}, 1000);

