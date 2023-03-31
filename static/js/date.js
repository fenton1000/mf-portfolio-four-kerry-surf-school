$(function () {

    function setMinDate() {
        let date = new Date();
        let today = date.getTime();
        let minDate = new Date(today+86400000);
        let formattedMinDate = new Date(
            minDate.getTime() - (minDate.getTimezoneOffset() * 60000))
            .toISOString()
            .split("T")[0];
            $('#id_lesson_date').attr('min', formattedMinDate);
    }

    setMinDate();
});