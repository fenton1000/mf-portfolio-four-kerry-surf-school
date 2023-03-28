$(function () {

    function setMinDate() {
        let minDate = new Date();
        let formattedMinDate = new Date(
            minDate.getTime() - (minDate.getTimezoneOffset() * 60000))
            .toISOString()
            .split("T")[0];
            $('#id_lesson_date').attr('min', formattedMinDate);
    }

    setMinDate();
});